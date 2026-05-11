import re


def normalize_keyword(keyword: str) -> str:
    return keyword.strip().lower()


def contains_keyword(text: str, keyword: str) -> bool:
    return normalize_keyword(keyword) in text.lower()


def extract_tags(text: str) -> list[str]:
    return re.findall(r"#([\w\u4e00-\u9fff-]+)", text)
