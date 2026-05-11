import importlib.util
import sys
from pathlib import Path

def load_storage_module():
    root = Path(__file__).resolve().parents[1]
    for modname in ["records", "storage", "input_handler", "text_utils", "models", "agents"]:
        sys.modules.pop(modname, None)
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("week11_storage", root / "storage.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def test_save_load_json_records(tmp_path):
    storage = load_storage_module()
    p = tmp_path / "records.json"
    storage.save_records([{"date": "2026-05-11", "content": "测试 JSON #json", "tags": ["json"]}], p)
    rows = storage.load_records(p)
    assert rows[0]["date"] == "2026-05-11"
    assert rows[0]["content"] == "测试 JSON #json"
    assert "json" in rows[0].get("tags", [])
