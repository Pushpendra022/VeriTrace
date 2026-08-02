import tempfile
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.exceptions import AppError
from app.core.security import sanitize_filename
from app.models.document import Document, DocumentChunk, DocumentPage
from app.services.chunking_service import create_chunks
from app.services.extraction_service import extract_document

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}
ALLOWED_MIMES = {"application/pdf", "text/plain", "text/markdown", "text/x-markdown", "application/octet-stream"}


async def create_document(db: Session, upload: UploadFile, settings: Settings) -> Document:
    original = sanitize_filename(upload.filename or "document")
    extension = Path(original).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS or (upload.content_type or "") not in ALLOWED_MIMES:
        raise AppError("INVALID_FILE_TYPE", "Upload a PDF, TXT, or Markdown document.", 415)
    size = 0
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temporary:
            temporary_path = Path(temporary.name)
            while content := await upload.read(1024 * 1024):
                size += len(content)
                if size > settings.max_upload_mb * 1024 * 1024:
                    raise AppError("FILE_TOO_LARGE", f"Documents must be {settings.max_upload_mb} MB or smaller.", 413)
                temporary.write(content)
        if size == 0:
            raise AppError("EMPTY_FILE", "The selected file is empty.")
        pages = extract_document(temporary_path, extension)
        character_count = sum(len(page.text) for page in pages)
        if character_count > settings.max_document_characters:
            raise AppError("DOCUMENT_TOO_LONG", "The extracted document exceeds the processing limit.", 413)
        document = Document(filename=original, original_filename=original, mime_type=upload.content_type or "application/octet-stream", file_size=size, status="ready", page_count=len(pages), character_count=character_count)
        db.add(document)
        db.flush()
        for page in pages:
            db.add(DocumentPage(document_id=document.id, page_number=page.page_number, text=page.text, start_char=page.start_char, end_char=page.end_char))
        for chunk in create_chunks(pages):
            db.add(DocumentChunk(document_id=document.id, page_number=chunk.page_number, text=chunk.text, start_char=chunk.start_char, end_char=chunk.end_char, token_estimate=chunk.token_estimate))
        db.commit(); db.refresh(document)
        return document
    except Exception:
        db.rollback()
        raise
    finally:
        await upload.close()
        if temporary_path:
            temporary_path.unlink(missing_ok=True)

