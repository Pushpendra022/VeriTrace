from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.routes.documents import find_document
from app.db.session import get_db
from app.models.claim import Claim
from app.models.document import Document, DocumentPage
from app.models.verification import Verification
from app.schemas.claims import ClaimResponse
from app.schemas.documents import DocumentResponse, PageResponse
from app.schemas.reviews import ReviewDetail, ReviewSummary
from app.services.verification_service import serialize_verification

router = APIRouter(tags=["reviews"])


@router.get("/reviews", response_model=list[ReviewSummary])
def list_reviews(db: Session = Depends(get_db)) -> list[ReviewSummary]:
    documents = db.scalars(select(Document).order_by(Document.updated_at.desc())).all()
    results = []
    for document in documents:
        claims = list(db.scalars(select(Claim).where(Claim.document_id == document.id)).all())
        latest = []
        for claim in claims:
            item = db.scalar(select(Verification).where(Verification.claim_id == claim.id).order_by(Verification.created_at.desc()))
            if item: latest.append(item)
        counts = {name: sum(item.verdict == name for item in latest) for name in ("SUPPORTED", "CONTRADICTED", "NOT_FOUND", "NEEDS_REVIEW")}
        results.append(ReviewSummary(document_id=document.id, document_name=document.original_filename, upload_date=document.created_at, claim_count=len(claims), supported_count=counts["SUPPORTED"], contradicted_count=counts["CONTRADICTED"], not_found_count=counts["NOT_FOUND"], needs_review_count=counts["NEEDS_REVIEW"], last_updated=document.updated_at))
    return results


@router.get("/reviews/{document_id}", response_model=ReviewDetail)
def get_review(document_id: str, db: Session = Depends(get_db)) -> ReviewDetail:
    document = find_document(db, document_id)
    pages = list(db.scalars(select(DocumentPage).where(DocumentPage.document_id == document_id).order_by(DocumentPage.page_number)).all())
    claims = list(db.scalars(select(Claim).where(Claim.document_id == document_id).order_by(Claim.created_at)).all())
    verifications = []
    for claim in claims:
        item = db.scalar(select(Verification).where(Verification.claim_id == claim.id).order_by(Verification.created_at.desc()))
        if item: verifications.append(serialize_verification(item, claim, document))
    return ReviewDetail(document=DocumentResponse.model_validate(document), pages=[PageResponse.model_validate(page) for page in pages], claims=[ClaimResponse.model_validate(claim) for claim in claims], verifications=verifications)

