import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Claim(Base):
    __tablename__ = "claims"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    claim_text: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), default="general")
    importance: Mapped[str] = mapped_column(String(20), default="medium")
    source_type: Mapped[str] = mapped_column(String(20), default="manual")
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    document: Mapped["Document"] = relationship(back_populates="claims")  # noqa: F821
    verifications: Mapped[list["Verification"]] = relationship(back_populates="claim", cascade="all, delete-orphan")  # noqa: F821

