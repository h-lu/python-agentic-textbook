import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from storage import load_records, save_records


def test_save_and_load_records(tmp_path):
    p = tmp_path / "records.json"
    save_records(p, [{"date": "2026-05-11", "content": "测试存储"}])
    assert load_records(p)[0]["content"] == "测试存储"
