from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ClaimCreate(BaseModel):
    claim_text: str = Field(min_length=3, max_length=2000)
    category: str = Field(default="general", min_length=2, max_length=50)
    importance: Literal["low", "medium", "high"] = "medium"


class ClaimUpdate(BaseModel):
    claim_text: str | None = Field(default=None, min_length=3, max_length=2000)
    category: str | None = Field(default=None, min_length=2, max_length=50)
    importance: Literal["low", "medium", "high"] | None = None


class ClaimResponse(ClaimCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str
    document_id: str
    source_type: str
    status: str
    created_at: datetime
    updated_at: datetime


class ExtractedClaim(BaseModel):
    claim_text: str = Field(min_length=3, max_length=2000)
    category: str = Field(min_length=2, max_length=50)
    importance: Literal["low", "medium", "high"]


class ExtractedClaims(BaseModel):
    claims: list[ExtractedClaim]

