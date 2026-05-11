import json
import os
from pathlib import Path
from tempfile import gettempdir

SAMPLE_JSON_FILE = Path(__file__).with_name("sample_records.json")
SAMPLE_TEXT_FILE = Path(__file__).with_name("pyhelper_data.txt")

def data_file() -> Path:
    return Path(os.environ.get("PYHELPER_DATA_FILE", Path(gettempdir()) / "pyhelper_week10_data.json"))

def _record_from_text(line: str) -> dict | None:
    try:
        date_text, content = line.strip().split("|", 1)
    except ValueError:
        return None
    try:
        from .records import make_record
    except ImportError:
        from records import make_record
    return make_record(date_text, content)

def migrate_text_records(path: Path = SAMPLE_TEXT_FILE) -> list[dict]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []
    return [record for line in lines if (record := _record_from_text(line)) is not None]

def load_records(path: Path | None = None) -> list[dict]:
    path = path or data_file()
    source = path if path.exists() else SAMPLE_JSON_FILE
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return migrate_text_records()
    except json.JSONDecodeError:
        return migrate_text_records(source)
    records = payload.get("records", payload if isinstance(payload, list) else [])
    try:
        from .records import make_record
    except ImportError:
        from records import make_record
    normalized = []
    for item in records:
        if isinstance(item, dict):
            rec = make_record(str(item.get("date", "")), str(item.get("content", "")))
            if rec is not None:
                normalized.append(rec)
    return normalized

def save_records(records: list[dict], path: Path | None = None) -> None:
    path = path or data_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(export_json(records), encoding="utf-8")

def export_json(records: list[dict]) -> str:
    return json.dumps({"version": 2, "records": records}, ensure_ascii=False, indent=2)

def import_json(text: str) -> list[dict]:
    payload = json.loads(text)
    records = payload.get("records", payload if isinstance(payload, list) else [])
    try:
        from .records import make_record
    except ImportError:
        from records import make_record
    result = []
    for item in records:
        rec = make_record(str(item.get("date", "")), str(item.get("content", "")))
        if rec is not None:
            result.append(rec)
    return result
