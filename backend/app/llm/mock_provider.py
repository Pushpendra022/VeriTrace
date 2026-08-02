from app.core.exceptions import AppError
from app.llm.base import LLMProvider

SAMPLE_SOURCE = "Total revenue reached $11.4 million, representing 18% year-over-year growth."


class MockProvider(LLMProvider):
    name, model = "mock", "deterministic-samples-v1"

    async def verify_claim(self, claim: str, context: list[dict[str, object]]) -> dict[str, object]:
        combined = " ".join(str(item.get("text", "")) for item in context)
        if SAMPLE_SOURCE not in combined:
            raise AppError("MOCK_SAMPLE_ONLY", "Demo mode only verifies built-in sample reviews.", 400)
        lowered = claim.lower()
        if "$11.4" in lowered and "18%" in lowered:
            verdict, confidence, explanation = "SUPPORTED", .98, "Every material value matches the source."
        elif "$14.2" in lowered or "22%" in lowered:
            verdict, confidence, explanation = "CONTRADICTED", .97, "The source reports $11.4 million and 18% growth instead."
        elif "340" in lowered:
            return {"verdict": "NOT_FOUND", "confidence": .91, "quote": "", "explanation": "The source does not discuss enterprise customer count.", "page_number": None, "chunk_id": None}
        else:
            verdict, confidence, explanation = "NEEDS_REVIEW", .55, "The evidence is related but does not establish the claim reliably."
        first = context[0]
        return {"verdict": verdict, "confidence": confidence, "quote": SAMPLE_SOURCE, "explanation": explanation, "page_number": first.get("page_number"), "chunk_id": first.get("id")}

    async def extract_claims(self, document_text: str) -> dict[str, object]:
        if SAMPLE_SOURCE not in document_text:
            raise AppError("MOCK_SAMPLE_ONLY", "Demo mode only extracts claims from built-in samples.", 400)
        return {"claims": [{"claim_text": "Revenue reached $11.4 million and increased 18% year over year.", "category": "financial", "importance": "high"}]}

