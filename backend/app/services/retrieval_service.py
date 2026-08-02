import re
from dataclasses import dataclass

from rapidfuzz.fuzz import token_set_ratio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.document import DocumentChunk


@dataclass(frozen=True)
class RetrievalResult:
    chunks: list[DocumentChunk]
    chunks_searched: int
    top_similarity_score: float
    context_characters: int


def retrieve_chunks(claim: str, chunks: list[DocumentChunk], limit: int = 4) -> RetrievalResult:
    if not chunks:
        return RetrievalResult([], 0, 0, 0)
    corpus = [claim, *[chunk.text for chunk in chunks]]
    matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(corpus)
    similarities = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    claim_numbers = set(re.findall(r"[-+]?\$?\d[\d,.]*%?", claim))
    claim_words = set(re.findall(r"[A-Za-z]{4,}", claim.lower()))
    scored = []
    for index, chunk in enumerate(chunks):
        number_overlap = len(claim_numbers & set(re.findall(r"[-+]?\$?\d[\d,.]*%?", chunk.text)))
        word_overlap = len(claim_words & set(re.findall(r"[A-Za-z]{4,}", chunk.text.lower()))) / max(1, len(claim_words))
        fuzzy = token_set_ratio(claim, chunk.text) / 100
        score = float(similarities[index]) + min(.25, number_overlap * .08) + word_overlap * .12 + fuzzy * .08
        scored.append((score, chunk))
    selected = [item[1] for item in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]
    return RetrievalResult(selected, len(chunks), round(max(score for score, _ in scored), 4), sum(len(chunk.text) for chunk in selected))

