import re
from dataclasses import dataclass

from rapidfuzz.fuzz import ratio


@dataclass(frozen=True)
class EvidenceLocation:
    verified: bool
    start_char: int | None
    end_char: int | None


def locate_quote(page_text: str, quote: str) -> EvidenceLocation:
    if not quote:
        return EvidenceLocation(False, None, None)
    exact = page_text.find(quote)
    if exact >= 0:
        return EvidenceLocation(True, exact, exact + len(quote))
    normalized_quote = re.sub(r"\s+", " ", quote).strip()
    for match in re.finditer(re.escape(normalized_quote), re.sub(r"\s+", " ", page_text), re.I):
        return EvidenceLocation(True, match.start(), match.end())
    sentences = [item.strip() for item in re.split(r"(?<=[.!?])\s+", page_text) if item.strip()]
    best = max(sentences, key=lambda item: ratio(item, normalized_quote), default="")
    if best and ratio(best, normalized_quote) >= 92:
        start = page_text.find(best)
        return EvidenceLocation(True, start, start + len(best))
    return EvidenceLocation(False, None, None)

