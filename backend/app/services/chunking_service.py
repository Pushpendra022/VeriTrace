import re
from dataclasses import dataclass

from app.services.extraction_service import ExtractedPage


@dataclass(frozen=True)
class ChunkData:
    page_number: int
    text: str
    start_char: int
    end_char: int
    token_estimate: int


def create_chunks(pages: list[ExtractedPage], target_words: int = 600, overlap_words: int = 75) -> list[ChunkData]:
    chunks: list[ChunkData] = []
    for page in pages:
        words = list(re.finditer(r"\S+", page.text))
        if not words:
            continue
        step = max(1, target_words - overlap_words)
        for index in range(0, len(words), step):
            group = words[index:index + target_words]
            local_start, local_end = group[0].start(), group[-1].end()
            text = page.text[local_start:local_end]
            chunks.append(ChunkData(page.page_number, text, page.start_char + local_start, page.start_char + local_end, max(1, round(len(text) / 4))))
            if index + target_words >= len(words):
                break
    return chunks

