try:
    from .input_handler import clean_content, is_valid_date
    from .models import Note
    from .text_utils import contains_keyword, extract_tags, in_date_range
except ImportError:
    from input_handler import clean_content, is_valid_date
    from models import Note
    from text_utils import contains_keyword, extract_tags, in_date_range

def make_note(date_text: str, content: str) -> Note | None:
    date_text = date_text.strip()
    content = clean_content(content)
    if not is_valid_date(date_text) or not content:
        return None
    return Note(date=date_text, content=content, tags=extract_tags(content))

def make_record(date_text: str, content: str) -> dict | None:
    note = make_note(date_text, content)
    return note.to_dict() if note else None

def add_record(records: list[dict], date_text: str, content: str) -> bool:
    record = make_record(date_text, content)
    if record is None:
        return False
    records.append(record)
    return True

def list_records(records: list[dict]) -> list[str]:
    return [f"{item['date']}: {item['content']}" for item in records]

def stats(records: list[dict]) -> str:
    days = {item["date"] for item in records}
    reviewed = sum(1 for item in records if item.get("reviewed"))
    return f"共 {len(records)} 条记录，覆盖 {len(days)} 天，已审查 {reviewed} 条。"

def search_records(records: list[dict], keyword: str = "", start: str | None = None, end: str | None = None) -> list[dict]:
    result = []
    for item in records:
        note = Note.from_dict(item)
        if keyword and not contains_keyword(note.content, keyword):
            continue
        if not in_date_range(note.date, start, end):
            continue
        result.append(note.to_dict())
    return result
