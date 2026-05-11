def add_record(records: list[dict], date: str, content: str, tags: list[str] | None = None) -> list[dict]:
    records.append({"date": date, "content": content, "tags": tags or []})
    return records
