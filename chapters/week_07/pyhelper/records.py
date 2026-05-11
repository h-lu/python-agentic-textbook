def make_record(date: str, content: str) -> dict:
    return {"date": date, "content": content.strip()}


def format_record(record: dict) -> str:
    return f"{record['date']}: {record['content']}"
