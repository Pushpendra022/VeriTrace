import hashlib
import json
import time

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.exceptions import AppError
from app.llm.factory import create_provider
from app.llm.mock_provider import MockProvider
from app.models.claim import Claim
from app.models.document import Document, DocumentChunk, DocumentPage
from app.models.verification import Verification
from app.schemas.verification import ChecksResponse, MetricsResponse, ModelVerification, SourceResponse, VerificationResponse
from app.services.deterministic_validator import validate_facts
from app.services.evidence_locator import locate_quote
from app.services.retrieval_service import retrieve_chunks


def serialize_verification(item: Verification, claim: Claim, document: Document) -> VerificationResponse:
    return VerificationResponse(
        verification_id=item.id, claim_id=claim.id, verdict=item.verdict, confidence=item.confidence, quote=item.quote, explanation=item.explanation,
        source=SourceResponse(document_id=document.id, document_name=document.original_filename, page_number=item.page_number, chunk_id=item.chunk_id, start_char=item.start_char, end_char=item.end_char),
        checks=ChecksResponse(quote_verified=item.quote_verified, numbers_consistent=item.numbers_consistent, percentages_consistent=item.percentages_consistent, dates_consistent=item.dates_consistent, currency_consistent=item.currency_consistent),
        metrics=MetricsResponse(latency_ms=item.latency_ms, chunks_searched=item.chunks_searched, chunks_retrieved=item.chunks_retrieved, context_characters=item.context_characters, provider=item.provider, model=item.model, prompt_version=item.prompt_version), created_at=item.created_at,
    )


async def verify_claim(db: Session, claim: Claim, settings: Settings) -> VerificationResponse:
    started = time.perf_counter()
    document = db.get(Document, claim.document_id)
    chunks = list(db.scalars(select(DocumentChunk).where(DocumentChunk.document_id == claim.document_id)).all())
    retrieval = retrieve_chunks(claim.claim_text, chunks)
    if not retrieval.chunks:
        raise AppError("NO_RELEVANT_CHUNKS", "No searchable source content was found for this document.", 422)
    fingerprint = hashlib.sha256((claim.claim_text + "\n" + "\n".join(chunk.text for chunk in retrieval.chunks)).encode()).hexdigest()
    cached = db.scalar(select(Verification).where(Verification.claim_id == claim.id, Verification.claim_fingerprint == fingerprint).order_by(Verification.created_at.desc()))
    if cached:
        return serialize_verification(cached, claim, document)
    provider = MockProvider() if claim.source_type == "sample" else create_provider(settings)
    context = [{"id": chunk.id, "page_number": chunk.page_number, "text": chunk.text} for chunk in retrieval.chunks]
    raw: dict[str, object] | None = None
    for attempt in range(2):
        try:
            raw = await provider.verify_claim(claim.claim_text, context[:1] if attempt else context)
            model_result = ModelVerification.model_validate(raw)
            break
        except ValidationError as exc:
            if attempt == 1:
                raise AppError("MODEL_INVALID_RESPONSE", "The verification response could not be validated.", 502) from exc
    assert raw is not None
    page = db.scalar(select(DocumentPage).where(DocumentPage.document_id == document.id, DocumentPage.page_number == model_result.page_number)) if model_result.page_number else None
    location = locate_quote(page.text, model_result.quote) if page else locate_quote("", model_result.quote)
    checks = validate_facts(claim.claim_text, model_result.quote)
    verdict = model_result.verdict
    explanation = model_result.explanation
    if verdict == "SUPPORTED" and not all((checks.numbers_consistent, checks.percentages_consistent, checks.dates_consistent, checks.currency_consistent)):
        verdict, explanation = "CONTRADICTED", "The retrieved evidence conflicts with one or more material facts in the claim."
    if model_result.quote and not location.verified:
        verdict, explanation = "NEEDS_REVIEW", "Relevant evidence was found, but the exact quote could not be confirmed in the source."
    if verdict in ("SUPPORTED", "CONTRADICTED") and not model_result.quote:
        verdict, explanation = "NEEDS_REVIEW", "The conclusion did not include verifiable exact evidence."
    confidence = min(model_result.confidence * .1 + retrieval.top_similarity_score * .2 + (.3 if location.verified else 0) + (.25 if all((checks.numbers_consistent, checks.percentages_consistent, checks.dates_consistent, checks.currency_consistent)) else .1) + (.15 if model_result.quote else 0), 1)
    item = Verification(claim_id=claim.id, verdict=verdict, confidence=round(confidence, 2), quote=model_result.quote if location.verified else "", explanation=explanation, page_number=model_result.page_number if location.verified else None, chunk_id=model_result.chunk_id if location.verified else None, start_char=location.start_char, end_char=location.end_char, quote_verified=location.verified, numbers_consistent=checks.numbers_consistent, percentages_consistent=checks.percentages_consistent, dates_consistent=checks.dates_consistent, currency_consistent=checks.currency_consistent, latency_ms=round((time.perf_counter() - started) * 1000), chunks_searched=retrieval.chunks_searched, chunks_retrieved=len(retrieval.chunks), context_characters=retrieval.context_characters, provider=provider.name, model=provider.model, raw_model_response=json.dumps(raw), prompt_version="verification-v1", claim_fingerprint=fingerprint)
    claim.status = "completed"; db.add(item); db.commit(); db.refresh(item)
    return serialize_verification(item, claim, document)
