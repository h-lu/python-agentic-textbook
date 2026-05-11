import importlib.util
import sys
from pathlib import Path

def load_records_module():
    root = Path(__file__).resolve().parents[1]
    for modname in ["records", "storage", "input_handler", "text_utils", "models", "agents"]:
        sys.modules.pop(modname, None)
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("week09_records", root / "records.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def test_add_record_and_stats():
    records_mod = load_records_module()
    rows = []
    assert records_mod.add_record(rows, "2026-05-11", " 学习函数 #python ")
    assert not records_mod.add_record(rows, "bad", "")
    assert rows[0]["date"] == "2026-05-11"
    assert rows[0]["content"] == "学习函数 #python"
    assert "python" in [tag.casefold() for tag in rows[0].get("tags", [])]
    assert "1 条记录" in records_mod.stats(rows)
