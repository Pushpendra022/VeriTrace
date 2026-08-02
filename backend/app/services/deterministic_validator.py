from dataclasses import dataclass

from app.utils.dates import extract_dates
from app.utils.numbers import compare_numeric_sets, detect_approximation, extract_currency_values, extract_numbers, extract_percentages


@dataclass(frozen=True)
class DeterministicChecks:
    numbers_consistent: bool
    percentages_consistent: bool
    dates_consistent: bool
    currency_consistent: bool


def validate_facts(claim: str, evidence: str) -> DeterministicChecks:
    approximate = detect_approximation(claim)
    claim_dates = extract_dates(claim)
    evidence_dates = extract_dates(evidence)
    return DeterministicChecks(
        compare_numeric_sets(extract_numbers(claim), extract_numbers(evidence), approximate),
        compare_numeric_sets(extract_percentages(claim), extract_percentages(evidence), approximate),
        not claim_dates or all(item in evidence_dates for item in claim_dates),
        not extract_currency_values(claim) or all(item in extract_currency_values(evidence) for item in extract_currency_values(claim)),
    )

