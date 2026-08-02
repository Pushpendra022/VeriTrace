from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.exceptions import AppError
from app.db.session import get_db
from app.models.document import Document, DocumentPage
from app.schemas.documents import DocumentResponse, PageResponse, UploadResponse
from app.services.document_service import create_document

router = APIRouter(tags=["documents"])


def find_document(db: Session, document_id: str) -> Document:
    document = db.get(Document, document_id)
    if not document:
        raise AppError("DOCUMENT_NOT_FOUND", "The requested document was not found.", 404)
    return document


@router.post("/documents", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), settings: Settings = Depends(get_settings)) -> UploadResponse:
    document = await create_document(db, file, settings)
    pages = db.scalars(select(DocumentPage).where(DocumentPage.document_id == document.id).order_by(DocumentPage.page_number)).all()
    return UploadResponse(**DocumentResponse.model_validate(document).model_dump(), pages=[PageResponse.model_validate(page) for page in pages])


@router.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)) -> Document:
    return find_document(db, document_id)


@router.get("/documents/{document_id}/pages", response_model=list[PageResponse])
def get_pages(document_id: str, db: Session = Depends(get_db)) -> list[DocumentPage]:
    find_document(db, document_id)
    return list(db.scalars(select(DocumentPage).where(DocumentPage.document_id == document_id).order_by(DocumentPage.page_number)).all())


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, db: Session = Depends(get_db)) -> Response:
    db.delete(find_document(db, document_id)); db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

