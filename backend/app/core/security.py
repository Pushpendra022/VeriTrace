import re
from pathlib import Path

SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def sanitize_filename(filename: str) -> str:
    name = Path(filename).name
    safe = SAFE_NAME.sub("-", name).strip(".-")
    return safe[:255] or "document"

