def make_record(date: str, content: str) -> dict:
    if not content.strip():
        raise ValueError("content must not be blank")
    return {"date": date, "content": content.strip()}


def search_records(records: list[dict], keyword: str) -> list[dict]:
    return [item for item in records if keyword in item["content"]]
