import json
from pathlib import Path


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("records json must be a list")
    return data


def save_json(path: Path, records: list[dict]) -> None:
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def export_json(records: list[dict]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2)
