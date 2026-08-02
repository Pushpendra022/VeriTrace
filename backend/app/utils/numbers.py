import re
from decimal import Decimal

NUMBER_PATTERN = re.compile(r"(?<![A-Za-z])[-+]?\d[\d,]*(?:\.\d+)?")


def normalize_number(value: str) -> Decimal:
    return Decimal(value.replace(",", ""))


def extract_numbers(text: str) -> list[Decimal]:
    return [normalize_number(value) for value in NUMBER_PATTERN.findall(text)]


def extract_percentages(text: str) -> list[Decimal]:
    return [normalize_number(value) for value in re.findall(r"([-+]?\d[\d,]*(?:\.\d+)?)\s*%", text)]


def extract_currency_values(text: str) -> list[tuple[str, Decimal, str | None]]:
    pattern = r"([$€£])\s*([-+]?\d[\d,]*(?:\.\d+)?)\s*(thousand|million|billion)?"
    return [(symbol, normalize_number(value), unit) for symbol, value, unit in re.findall(pattern, text, re.I)]


def compare_numeric_sets(left: list[Decimal], right: list[Decimal], approximate: bool = False) -> bool:
    if not left:
        return True
    tolerance = Decimal("0.02") if approximate else Decimal("0")
    return all(any(abs(a - b) <= max(abs(a), Decimal(1)) * tolerance for b in right) for a in left)


def detect_approximation(text: str) -> bool:
    return bool(re.search(r"\b(approximately|about|nearly|roughly)\b", text, re.I))


def detect_negation(text: str) -> bool:
    return bool(re.search(r"\b(no|not|never|didn't|doesn't|without)\b", text, re.I))

