import uuid
from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename: Mapped[str] = mapped_column(String(255))
    original_filename: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(100))
    file_size: Mapped[int] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(String(30), default="processing", index=True)
    page_count: Mapped[int] = mapped_column(Integer, default=0)
    character_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    pages: Mapped[list["DocumentPage"]] = relationship(back_populates="document", cascade="all, delete-orphan")
    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")
    claims: Mapped[list["Claim"]] = relationship(back_populates="document", cascade="all, delete-orphan")  # noqa: F821


class DocumentPage(Base):
    __tablename__ = "document_pages"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    page_number: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    start_char: Mapped[int] = mapped_column(Integer)
    end_char: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    document: Mapped[Document] = relationship(back_populates="pages")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    page_number: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    start_char: Mapped[int] = mapped_column(Integer)
    end_char: Mapped[int] = mapped_column(Integer)
    token_estimate: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    document: Mapped[Document] = relationship(back_populates="chunks")

