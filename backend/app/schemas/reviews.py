from datetime import datetime

from pydantic import BaseModel

from app.schemas.claims import ClaimResponse
from app.schemas.documents import DocumentResponse, PageResponse
from app.schemas.verification import VerificationResponse


class ReviewSummary(BaseModel):
    document_id: str
    document_name: str
    upload_date: datetime
    claim_count: int
    supported_count: int
    contradicted_count: int
    not_found_count: int
    needs_review_count: int
    last_updated: datetime


class ReviewDetail(BaseModel):
    document: DocumentResponse
    pages: list[PageResponse]
    claims: list[ClaimResponse]
    verifications: list[VerificationResponse]

