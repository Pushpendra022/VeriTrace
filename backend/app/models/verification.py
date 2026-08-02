import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Verification(Base):
    __tablename__ = "verifications"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id: Mapped[str] = mapped_column(ForeignKey("claims.id", ondelete="CASCADE"), index=True)
    verdict: Mapped[str] = mapped_column(String(20), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    quote: Mapped[str] = mapped_column(Text, default="")
    explanation: Mapped[str] = mapped_column(Text)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    chunk_id: Mapped[str | None] = mapped_column(ForeignKey("document_chunks.id", ondelete="SET NULL"), nullable=True)
    start_char: Mapped[int | None] = mapped_column(Integer, nullable=True)
    end_char: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quote_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    numbers_consistent: Mapped[bool] = mapped_column(Boolean, default=True)
    percentages_consistent: Mapped[bool] = mapped_column(Boolean, default=True)
    dates_consistent: Mapped[bool] = mapped_column(Boolean, default=True)
    currency_consistent: Mapped[bool] = mapped_column(Boolean, default=True)
    latency_ms: Mapped[int] = mapped_column(Integer)
    chunks_searched: Mapped[int] = mapped_column(Integer, default=0)
    chunks_retrieved: Mapped[int] = mapped_column(Integer, default=0)
    context_characters: Mapped[int] = mapped_column(Integer, default=0)
    provider: Mapped[str] = mapped_column(String(30))
    model: Mapped[str] = mapped_column(String(100))
    prompt_version: Mapped[str] = mapped_column(String(30), default="verification-v1")
    raw_model_response: Mapped[str] = mapped_column(Text, default="")
    claim_fingerprint: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    claim: Mapped["Claim"] = relationship(back_populates="verifications")  # noqa: F821

