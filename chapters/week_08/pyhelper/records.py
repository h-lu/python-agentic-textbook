try:
    from .input_handler import clean_content, is_valid_date
except ImportError:
    from input_handler import clean_content, is_valid_date

def make_record(date_text: str, content: str) -> dict[str, str] | None:
    date_text = date_text.strip()
    content = clean_content(content)
    if not is_valid_date(date_text) or not content:
        return None
    return {"date": date_text, "content": content}

def add_record(records: list[dict[str, str]], date_text: str, content: str) -> bool:
    record = make_record(date_text, content)
    if record is None:
        return False
    records.append(record)
    return True

def list_records(records: list[dict[str, str]]) -> list[str]:
    return [f"{item['date']}: {item['content']}" for item in records]

def stats(records: list[dict[str, str]]) -> str:
    days = {item["date"] for item in records}
    return f"共 {len(records)} 条记录，覆盖 {len(days)} 天。"
