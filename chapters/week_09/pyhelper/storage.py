import os
from pathlib import Path
from tempfile import gettempdir

SAMPLE_DATA_FILE = Path(__file__).with_name("pyhelper_data.txt")

def data_file() -> Path:
    return Path(os.environ.get("PYHELPER_DATA_FILE", Path(gettempdir()) / "pyhelper_week09_data.txt"))

def parse_line(line: str) -> dict | None:
    try:
        date_text, content = line.strip().split("|", 1)
    except ValueError:
        return None
    try:
        from .records import make_record
    except ImportError:
        from records import make_record
    return make_record(date_text, content)

def load_records(path: Path | None = None) -> list[dict]:
    path = path or data_file()
    source = path if path.exists() else SAMPLE_DATA_FILE
    try:
        lines = source.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []
    except OSError as exc:
        print(f"读取记录失败：{exc}")
        return []
    return [record for line in lines if (record := parse_line(line)) is not None]

def save_records(records: list[dict], path: Path | None = None) -> None:
    path = path or data_file()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(f"{item['date']}|{item['content']}\n" for item in records), encoding="utf-8")
    except OSError as exc:
        print(f"保存记录失败：{exc}")
