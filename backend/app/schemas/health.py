from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]
    database: Literal["connected"]
    llm_provider: Literal["gemini", "mock"]

