"""Week 04 PyHelper: in-memory records with list/dict."""

def add_record(records: list[dict], date: str, content: str) -> list[dict]:
    records.append({"date": date, "content": content})
    return records


def list_records(records: list[dict]) -> list[str]:
    return [f"{item['date']}: {item['content']}" for item in records]


def count_by_date(records: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in records:
        counts[item["date"]] = counts.get(item["date"], 0) + 1
    return counts


def main() -> None:
    records: list[dict] = []
    add_record(records, "2026-05-11", "学习了列表和字典")
    add_record(records, "2026-05-11", "给 PyHelper 增加学习记录")
    print("PyHelper 学习记录：")
    for line in list_records(records):
        print("- " + line)
    print("统计：", count_by_date(records))


if __name__ == "__main__":
    main()
