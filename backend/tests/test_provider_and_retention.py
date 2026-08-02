import asyncio
from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.llm.mock_provider import MockProvider, SAMPLE_SOURCE
from app.llm.prompts import CLAIM_EXTRACTION_PROMPT
from app.models.document import Document
from app.schemas.verification import ModelVerification
from app.services.retention_service import delete_expired_reviews


def test_model_output_rejects_missing_and_unknown_verdicts() -> None:
    with pytest.raises(ValidationError):
        ModelVerification.model_validate({"verdict": "MAYBE"})
    with pytest.raises(ValidationError):
        ModelVerification.model_validate({"verdict": "SUPPORTED", "confidence": 2, "quote": "x", "explanation": "bad", "page_number": 1})


def test_claim_extraction_prompt_formats_json_example() -> None:
    prompt = CLAIM_EXTRACTION_PROMPT.format(limit=15, text="Revenue was $1 million.")
    assert '"claims"' in prompt and "Maximum 15" in prompt


def test_mock_provider_exposes_all_four_sample_verdicts() -> None:
    provider = MockProvider()
    context = [{"id": "chunk", "page_number": 1, "text": SAMPLE_SOURCE}]
    claims = {
        "Revenue reached $11.4 million and increased 18% year over year.": "SUPPORTED",
        "Revenue reached $14.2 million and increased 22% year over year.": "CONTRADICTED",
        "The company serves 340 enterprise customers.": "NOT_FOUND",
        "The business expanded strongly.": "NEEDS_REVIEW",
    }
    for claim, expected in claims.items():
        assert asyncio.run(provider.verify_claim(claim, context))["verdict"] == expected


def test_retention_deletes_only_expired_reviews() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    now = datetime.now(timezone.utc)
    with Session(engine) as db:
        old = Document(filename="old.txt", original_filename="old.txt", mime_type="text/plain", file_size=1, status="ready", page_count=1, character_count=1, created_at=now - timedelta(days=9), updated_at=now - timedelta(days=9))
        recent = Document(filename="new.txt", original_filename="new.txt", mime_type="text/plain", file_size=1, status="ready", page_count=1, character_count=1, created_at=now, updated_at=now)
        db.add_all([old, recent]); db.commit()
        assert delete_expired_reviews(db, 7, now) == 1
        assert [item.filename for item in db.scalars(select(Document)).all()] == ["new.txt"]
