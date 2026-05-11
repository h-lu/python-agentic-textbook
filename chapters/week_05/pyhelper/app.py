"""Week 05 PyHelper: text-file persistence."""

from pathlib import Path
from tempfile import gettempdir

DATA_FILE = Path(__file__).with_name("pyhelper_data.txt")


def add_record(date: str, content: str, filename: Path = DATA_FILE) -> None:
    with filename.open("a", encoding="utf-8") as f:
        f.write(f"{date}|{content}\n")


def load_records(filename: Path = DATA_FILE) -> list[dict]:
    if not filename.exists():
        return []
    records = []
    with filename.open("r", encoding="utf-8") as f:
        for line in f:
            date, content = line.rstrip("\n").split("|", 1)
            records.append({"date": date, "content": content})
    return records


def main() -> None:
    demo_file = Path(gettempdir()) / "pyhelper_week05_demo.txt"
    demo_file.write_text(DATA_FILE.read_text(encoding="utf-8"), encoding="utf-8")
    add_record("2026-05-12", "把学习记录写入文本文件", demo_file)
    print("PyHelper 演示记录：")
    for item in load_records(demo_file):
        print(f"- {item['date']}: {item['content']}")


if __name__ == "__main__":
    main()
