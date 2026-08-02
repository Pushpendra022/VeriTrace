import re


def extract_dates(text: str) -> list[str]:
    years = re.findall(r"\b(?:19|20)\d{2}\b", text)
    dates = re.findall(r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+(?:19|20)\d{2}\b", text, re.I)
    return years + [value.lower() for value in dates]

