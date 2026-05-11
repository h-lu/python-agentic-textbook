import re
from datetime import date

def normalize_keyword(keyword: str) -> str:
    return keyword.strip().casefold()

def contains_keyword(text: str, keyword: str) -> bool:
    key = normalize_keyword(keyword)
    return bool(key) and key in text.casefold()

def extract_tags(text: str) -> list[str]:
    return re.findall(r"#([\w\u4e00-\u9fff-]+)", text)

def in_date_range(date_text: str, start: str | None = None, end: str | None = None) -> bool:
    current = date.fromisoformat(date_text)
    if start and current < date.fromisoformat(start):
        return False
    if end and current > date.fromisoformat(end):
        return False
    return True
