from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.db.session import get_db
from app.models.claim import Claim
from app.models.document import Document, DocumentChunk, DocumentPage
from app.schemas.claims import ClaimResponse
from app.schemas.documents import DocumentResponse, PageResponse
from app.schemas.reviews import ReviewDetail

router = APIRouter(tags=["samples"])
SOURCE = "Total revenue reached $11.4 million, representing 18% year-over-year growth.\n\nThe company entered three new European markets during 2025."
SAMPLES = {
    "supported": "Revenue reached $11.4 million and increased 18% year over year.",
    "contradicted": "Revenue reached $14.2 million and increased 22% year over year.",
    "not-found": "The company serves 340 enterprise customers.",
    "needs-review": "The company expanded internationally.",
}


@router.post("/samples/{sample_id}/load", response_model=ReviewDetail, status_code=201)
def load_sample(sample_id: str, db: Session = Depends(get_db)) -> ReviewDetail:
    if sample_id not in SAMPLES: raise AppError("SAMPLE_NOT_FOUND", "The requested sample review was not found.", 404)
    document = Document(filename=f"sample-{sample_id}.txt", original_filename=f"VeriTrace {sample_id.replace('-', ' ').title()} Sample.txt", mime_type="text/plain", file_size=len(SOURCE.encode()), status="ready", page_count=1, character_count=len(SOURCE))
    db.add(document); db.flush()
    page = DocumentPage(document_id=document.id, page_number=1, text=SOURCE, start_char=0, end_char=len(SOURCE)); chunk = DocumentChunk(document_id=document.id, page_number=1, text=SOURCE, start_char=0, end_char=len(SOURCE), token_estimate=round(len(SOURCE)/4)); claim = Claim(document_id=document.id, claim_text=SAMPLES[sample_id], category="financial" if sample_id != "needs-review" else "business", importance="high", source_type="sample")
    db.add_all([page, chunk, claim]); db.commit(); db.refresh(document); db.refresh(page); db.refresh(claim)
    return ReviewDetail(document=DocumentResponse.model_validate(document), pages=[PageResponse.model_validate(page)], claims=[ClaimResponse.model_validate(claim)], verifications=[])

