from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    document_id: str
    page_number: int
    text: str
    start_char: int
    end_char: int


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    filename: str
    original_filename: str
    mime_type: str
    file_size: int
    status: str
    page_count: int
    character_count: int
    created_at: datetime
    updated_at: datetime


class UploadResponse(DocumentResponse):
    pages: list[PageResponse]

