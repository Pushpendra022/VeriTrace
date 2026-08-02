from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Verdict = Literal["SUPPORTED", "CONTRADICTED", "NOT_FOUND", "NEEDS_REVIEW"]


class ModelVerification(BaseModel):
    verdict: Verdict
    confidence: float = Field(ge=0, le=1)
    quote: str
    explanation: str = Field(min_length=3, max_length=1000)
    page_number: int | None = None
    chunk_id: str | None = None


class SourceResponse(BaseModel):
    document_id: str
    document_name: str
    page_number: int | None
    chunk_id: str | None
    start_char: int | None
    end_char: int | None


class ChecksResponse(BaseModel):
    quote_verified: bool
    numbers_consistent: bool
    percentages_consistent: bool
    dates_consistent: bool
    currency_consistent: bool


class MetricsResponse(BaseModel):
    latency_ms: int
    chunks_searched: int
    chunks_retrieved: int
    context_characters: int
    provider: str
    model: str
    prompt_version: str


class VerificationResponse(BaseModel):
    verification_id: str
    claim_id: str
    verdict: Verdict
    confidence: float
    quote: str
    explanation: str
    source: SourceResponse
    checks: ChecksResponse
    metrics: MetricsResponse
    created_at: datetime


class BulkVerifyRequest(BaseModel):
    claim_ids: list[str] | None = None

