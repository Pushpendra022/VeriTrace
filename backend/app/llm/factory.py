from app.core.config import Settings
from app.core.exceptions import AppError
from app.llm.base import LLMProvider
from app.llm.gemini_provider import GeminiProvider
from app.llm.mock_provider import MockProvider


def create_provider(settings: Settings) -> LLMProvider:
    if settings.llm_provider == "mock":
        return MockProvider()
    if not settings.enable_llm:
        raise AppError("LLM_DISABLED", "Semantic verification is disabled. You can still load a sample review.", 503)
    return GeminiProvider(settings.gemini_api_key, settings.gemini_model, settings.max_extracted_claims)

