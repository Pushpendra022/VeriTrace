import re
from dataclasses import dataclass
from pathlib import Path

import fitz

from app.core.exceptions import AppError


@dataclass(frozen=True)
class ExtractedPage:
    page_number: int
    text: str
    start_char: int
    end_char: int


def normalize_text(text: str) -> str:
    text = re.sub(r"(?<=\w)-\n(?=[a-z])", "", text)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.replace("\r", "").split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def extract_document(path: Path, extension: str) -> list[ExtractedPage]:
    if extension == ".pdf":
        try:
            with fitz.open(path) as pdf:
                texts = [normalize_text(page.get_text("text")) for page in pdf]
        except Exception as exc:
            raise AppError("CORRUPTED_PDF", "We could not read this PDF. It may be corrupted.") from exc
        if not texts or sum(len(text) for text in texts) < max(20, len(texts) * 5):
            raise AppError("SCANNED_PDF", "This PDF appears to contain scanned pages. OCR is not supported in the current version.")
    else:
        try:
            texts = [normalize_text(path.read_text(encoding="utf-8-sig"))]
        except UnicodeDecodeError as exc:
            raise AppError("UNSUPPORTED_CONTENT", "This text document is not valid UTF-8 content.") from exc
    if not any(texts):
        raise AppError("EMPTY_DOCUMENT", "We could not extract readable text from this document.")
    pages, offset = [], 0
    for number, text in enumerate(texts, 1):
        pages.append(ExtractedPage(number, text, offset, offset + len(text)))
        offset += len(text) + 1
    return pages

