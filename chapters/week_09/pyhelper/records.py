try:
    from .text_utils import contains_keyword
except ImportError:
    from text_utils import contains_keyword


def filter_by_keyword(records: list[dict], keyword: str) -> list[dict]:
    return [item for item in records if contains_keyword(item.get("content", ""), keyword)]


def filter_by_date_range(records: list[dict], start: str, end: str) -> list[dict]:
    return [item for item in records if start <= item.get("date", "") <= end]
