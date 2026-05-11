import importlib.util
import sys
from pathlib import Path

def load_storage_module():
    root = Path(__file__).resolve().parents[1]
    for modname in ["records", "storage", "input_handler", "text_utils", "models", "agents"]:
        sys.modules.pop(modname, None)
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("week08_storage", root / "storage.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def test_save_load_skips_bad_lines(tmp_path):
    storage = load_storage_module()
    p = tmp_path / "records.txt"
    storage.save_records([{"date": "2026-05-11", "content": "测试存储"}], p)
    p.write_text(p.read_text(encoding="utf-8") + "bad-line\n", encoding="utf-8")
    assert storage.load_records(p) == [{"date": "2026-05-11", "content": "测试存储"}]
