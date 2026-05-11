import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from records import make_record, search_records


def test_make_record_strips_content():
    assert make_record("2026-05-11", "  pytest  ")["content"] == "pytest"


def test_search_records():
    records = [make_record("2026-05-11", "学习 pytest")]
    assert len(search_records(records, "pytest")) == 1
