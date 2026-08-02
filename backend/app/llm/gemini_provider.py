import asyncio
import json

from google import genai
from google.genai import types

from app.core.exceptions import AppError
from app.llm.base import LLMProvider
from app.llm.prompts import CLAIM_EXTRACTION_PROMPT, VERIFICATION_PROMPT


class GeminiProvider(LLMProvider):
    name = "gemini"

    def __init__(self, api_key: str, model: str, max_claims: int = 15):
        if not api_key:
            raise AppError("LLM_NOT_CONFIGURED", "Gemini is not configured. Add a server-side API key or use a sample review.", 503)
        self.client, self.model, self.max_claims = genai.Client(api_key=api_key), model, max_claims

    async def _generate(self, prompt: str) -> dict[str, object]:
        try:
            response = await asyncio.wait_for(self.client.aio.models.generate_content(model=self.model, contents=prompt, config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0)), timeout=30)
            if not response.text:
                raise AppError("MODEL_EMPTY_RESPONSE", "The verification service returned an empty response.", 502)
            return json.loads(response.text)
        except AppError:
            raise
        except asyncio.TimeoutError as exc:
            raise AppError("MODEL_TIMEOUT", "The verification service timed out. Please try again.", 504) from exc
        except json.JSONDecodeError as exc:
            raise AppError("MODEL_INVALID_JSON", "The verification response could not be validated.", 502) from exc
        except Exception as exc:
            message = str(exc).lower()
            code = "MODEL_QUOTA_EXCEEDED" if "quota" in message or "429" in message else "MODEL_UNAVAILABLE"
            friendly = "The verification service has reached its current usage limit." if code == "MODEL_QUOTA_EXCEEDED" else "The verification service is temporarily unavailable."
            raise AppError(code, friendly, 503) from exc

    async def verify_claim(self, claim: str, context: list[dict[str, object]]) -> dict[str, object]:
        return await self._generate(VERIFICATION_PROMPT.format(claim=claim, context=json.dumps(context, ensure_ascii=False)))

    async def extract_claims(self, document_text: str) -> dict[str, object]:
        return await self._generate(CLAIM_EXTRACTION_PROMPT.format(limit=self.max_claims, text=document_text))

