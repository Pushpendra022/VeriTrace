from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.db.session import get_db
from app.models.claim import Claim
from app.models.document import Document
from app.models.verification import Verification
from app.schemas.verification import VerificationResponse
from app.services.verification_service import serialize_verification

router = APIRouter(tags=["verification"])


@router.get("/verifications/{verification_id}", response_model=VerificationResponse)
def get_verification(verification_id: str, db: Session = Depends(get_db)) -> VerificationResponse:
    item = db.get(Verification, verification_id)
    if not item: raise AppError("VERIFICATION_NOT_FOUND", "The requested verification was not found.", 404)
    claim = db.get(Claim, item.claim_id); document = db.get(Document, claim.document_id)
    return serialize_verification(item, claim, document)

