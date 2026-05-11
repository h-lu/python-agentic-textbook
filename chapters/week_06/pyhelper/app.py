"""Week 06 PyHelper: safe loading and validation."""

from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("pyhelper_data.txt")


def is_valid_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def parse_line(line: str) -> dict | None:
    try:
        raw_date, content = line.rstrip("\n").split("|", 1)
    except ValueError:
        return None
    if not is_valid_date(raw_date) or not content.strip():
        return None
    return {"date": raw_date, "content": content.strip()}


def load_records(filename: Path = DATA_FILE) -> list[dict]:
    try:
        lines = filename.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []
    records = []
    for line in lines:
        item = parse_line(line)
        if item is not None:
            records.append(item)
    return records


def main() -> None:
    print("安全读取结果：")
    for item in load_records():
        print(f"- {item['date']}: {item['content']}")


if __name__ == "__main__":
    main()
