from decimal import Decimal
from pathlib import Path

import fitz

from app.services.chunking_service import create_chunks
from app.services.deterministic_validator import validate_facts
from app.services.evidence_locator import locate_quote
from app.models.document import DocumentChunk
from app.services.extraction_service import ExtractedPage, extract_document, normalize_text
from app.services.retrieval_service import retrieve_chunks
from app.utils.numbers import detect_approximation, extract_currency_values, extract_numbers, extract_percentages


def test_text_normalization_and_chunk_offsets() -> None:
    text = normalize_text("Revenue in-\ncreased  18%.\n\n\nMargin rose.")
    assert text == "Revenue increased 18%.\n\nMargin rose."
    chunks = create_chunks([ExtractedPage(1, text, 100, 100 + len(text))], target_words=4, overlap_words=1)
    assert chunks[0].page_number == 1 and chunks[0].start_char == 100


def test_fact_utilities_and_mismatch_detection() -> None:
    assert extract_numbers("$11.4 million and 18%") == [Decimal("11.4"), Decimal("18")]
    assert extract_percentages("grew 18.1%") == [Decimal("18.1")]
    assert extract_currency_values("$11.4 million") == [("$", Decimal("11.4"), "million")]
    assert detect_approximation("roughly 18%")
    checks = validate_facts("Revenue was $14.2 million and grew 22%.", "Revenue was $11.4 million and grew 18%.")
    assert not checks.numbers_consistent and not checks.percentages_consistent and not checks.currency_consistent


def test_exact_quote_location() -> None:
    source = "Before. Total revenue reached $11.4 million. After."
    result = locate_quote(source, "Total revenue reached $11.4 million.")
    assert result.verified and source[result.start_char:result.end_char] == "Total revenue reached $11.4 million."


def test_pdf_page_extraction(tmp_path: Path) -> None:
    path = tmp_path / "report.pdf"
    pdf = fitz.open(); page = pdf.new_page(); page.insert_text((72, 72), "Revenue reached $11.4 million."); pdf.save(path); pdf.close()
    pages = extract_document(path, ".pdf")
    assert len(pages) == 1 and "Revenue reached" in pages[0].text


def test_retrieval_prioritizes_matching_financial_fact() -> None:
    chunks = [DocumentChunk(id="a", document_id="d", page_number=1, text="Headcount was 214 employees.", start_char=0, end_char=28, token_estimate=7), DocumentChunk(id="b", document_id="d", page_number=2, text="Revenue reached $11.4 million and grew 18%.", start_char=29, end_char=74, token_estimate=12)]
    result = retrieve_chunks("Revenue grew 18% to $11.4 million.", chunks, 1)
    assert result.chunks[0].id == "b" and result.chunks_searched == 2
