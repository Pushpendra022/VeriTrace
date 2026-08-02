import asyncio

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.routes.documents import find_document
from app.core.config import Settings, get_settings
from app.core.exceptions import AppError
from app.db.session import SessionLocal, get_db
from app.llm.factory import create_provider
from app.models.claim import Claim
from app.models.document import DocumentPage
from app.schemas.claims import ClaimCreate, ClaimResponse, ClaimUpdate, ExtractedClaims
from app.schemas.verification import BulkVerifyRequest, VerificationResponse
from app.services.verification_service import verify_claim

router = APIRouter(tags=["claims"])


def find_claim(db: Session, claim_id: str) -> Claim:
    claim = db.get(Claim, claim_id)
    if not claim:
        raise AppError("CLAIM_NOT_FOUND", "The requested claim was not found.", 404)
    return claim


@router.post("/documents/{document_id}/claims", response_model=ClaimResponse, status_code=201)
def create_claim(document_id: str, payload: ClaimCreate, db: Session = Depends(get_db)) -> Claim:
    find_document(db, document_id)
    claim = Claim(document_id=document_id, **payload.model_dump()); db.add(claim); db.commit(); db.refresh(claim); return claim


@router.get("/documents/{document_id}/claims", response_model=list[ClaimResponse])
def list_claims(document_id: str, db: Session = Depends(get_db)) -> list[Claim]:
    find_document(db, document_id); return list(db.scalars(select(Claim).where(Claim.document_id == document_id).order_by(Claim.created_at)).all())


@router.post("/documents/{document_id}/claims/extract", response_model=list[ClaimResponse])
async def extract_claims(document_id: str, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)) -> list[Claim]:
    find_document(db, document_id)
    text = "\n".join(db.scalars(select(DocumentPage.text).where(DocumentPage.document_id == document_id).order_by(DocumentPage.page_number)).all())
    data = ExtractedClaims.model_validate(await create_provider(settings).extract_claims(text))
    claims = [Claim(document_id=document_id, source_type="extracted", **item.model_dump()) for item in data.claims[:settings.max_extracted_claims]]
    db.add_all(claims); db.commit()
    for claim in claims: db.refresh(claim)
    return claims


@router.patch("/claims/{claim_id}", response_model=ClaimResponse)
def update_claim(claim_id: str, payload: ClaimUpdate, db: Session = Depends(get_db)) -> Claim:
    claim = find_claim(db, claim_id)
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(claim, key, value)
    claim.status = "pending"; db.commit(); db.refresh(claim); return claim


@router.delete("/claims/{claim_id}", status_code=204)
def delete_claim(claim_id: str, db: Session = Depends(get_db)) -> Response:
    db.delete(find_claim(db, claim_id)); db.commit(); return Response(status_code=204)


@router.post("/claims/{claim_id}/verify", response_model=VerificationResponse)
async def verify_one(claim_id: str, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)) -> VerificationResponse:
    return await verify_claim(db, find_claim(db, claim_id), settings)


async def _verify_isolated(claim_id: str, settings: Settings, semaphore: asyncio.Semaphore) -> VerificationResponse:
    async with semaphore:
        with SessionLocal() as db:
            return await verify_claim(db, find_claim(db, claim_id), settings)


@router.post("/documents/{document_id}/verify", response_model=list[VerificationResponse])
async def verify_many(document_id: str, payload: BulkVerifyRequest, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)) -> list[VerificationResponse]:
    find_document(db, document_id)
    available = list(db.scalars(select(Claim.id).where(Claim.document_id == document_id)).all())
    ids = payload.claim_ids or available
    if len(ids) > settings.max_bulk_verification: raise AppError("BULK_LIMIT_EXCEEDED", f"Verify no more than {settings.max_bulk_verification} claims at once.", 422)
    if any(item not in available for item in ids): raise AppError("CLAIM_DOCUMENT_MISMATCH", "One or more claims do not belong to this document.", 422)
    semaphore = asyncio.Semaphore(settings.verification_concurrency)
    return list(await asyncio.gather(*[_verify_isolated(item, settings, semaphore) for item in ids]))

