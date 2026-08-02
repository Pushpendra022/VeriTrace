from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"), env_file_encoding="utf-8", extra="ignore"
    )

    app_env: Literal["development", "test", "production"] = "development"
    app_name: str = "VeriTrace"
    database_url: str = "sqlite:///./evidence_review.db"
    frontend_url: str = "http://localhost:5173"
    llm_provider: Literal["gemini", "mock"] = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-flash-latest"
    enable_llm: bool = True
    max_upload_mb: int = Field(default=20, ge=1, le=20)
    max_document_characters: int = Field(default=1_000_000, ge=1)
    max_extracted_claims: int = Field(default=15, ge=1, le=15)
    max_bulk_verification: int = Field(default=15, ge=1, le=15)
    verification_concurrency: int = Field(default=2, ge=1, le=3)
    rate_limit: str = "60/minute"
    review_retention_days: int | None = Field(default=7, ge=1, le=365)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @field_validator("frontend_url")
    @classmethod
    def validate_frontend_urls(cls, value: str) -> str:
        origins = [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]
        if not origins or any(not origin.startswith(("http://", "https://")) for origin in origins):
            raise ValueError("FRONTEND_URL must contain one or more HTTP(S) origins")
        return ",".join(origins)

    @model_validator(mode="after")
    def validate_production(self) -> "Settings":
        if self.app_env == "production" and "*" in self.frontend_url:
            raise ValueError("Wildcard CORS origins are not allowed in production")
        if self.enable_llm and self.llm_provider == "gemini" and self.app_env == "production" and not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when Gemini is enabled in production")
        return self

    @property
    def cors_origins(self) -> list[str]:
        return self.frontend_url.split(",")


@lru_cache
def get_settings() -> Settings:
    return Settings()
