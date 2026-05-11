"""Week 07 PyHelper: modular package."""

from pathlib import Path

try:
    from .encouragement import daily_message
    from .records import format_record, make_record
    from .storage import append_line, load_lines
except ImportError:
    from encouragement import daily_message
    from records import format_record, make_record
    from storage import append_line, load_lines

DATA_FILE = Path(__file__).with_name("pyhelper_data.txt")


def load_records() -> list[dict]:
    records = []
    for line in load_lines(DATA_FILE):
        if "|" in line:
            date, content = line.split("|", 1)
            records.append(make_record(date, content))
    return records


def add_record(date: str, content: str) -> None:
    append_line(DATA_FILE, f"{date}|{content}")


def main() -> None:
    print(daily_message())
    records = load_records() + [make_record("2026-05-12", "把 PyHelper 拆成模块")]
    for record in records:
        print("- " + format_record(record))


if __name__ == "__main__":
    main()
