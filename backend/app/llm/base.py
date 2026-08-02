from abc import ABC, abstractmethod


class LLMProvider(ABC):
    name: str
    model: str

    @abstractmethod
    async def verify_claim(self, claim: str, context: list[dict[str, object]]) -> dict[str, object]: ...

    @abstractmethod
    async def extract_claims(self, document_text: str) -> dict[str, object]: ...

