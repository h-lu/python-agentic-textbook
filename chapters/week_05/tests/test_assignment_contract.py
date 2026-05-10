"""Week 05 assignment contract: tests import the diary implementation students edit."""

import sys
from pathlib import Path

STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))
sys.modules.pop("solution", None)

import solution


def test_diary_solution_persists_and_searches_entries(tmp_path):
    diary = tmp_path / "diary.txt"
    solution.add_diary_entry("今天学会了文件操作", diary)
    solution.add_diary_entry("with 会自动关闭文件", diary)

    entries = solution.read_all_diaries(diary)
    assert len(entries) == 2
    assert "文件操作" in entries[0]
    assert solution.search_diaries("with", diary) == [entries[1]]
    assert solution.count_diaries(diary) == 2


def test_diary_solution_handles_missing_file(tmp_path):
    missing = tmp_path / "missing.txt"
    assert solution.read_all_diaries(missing) == []
    assert solution.search_diaries("anything", missing) == []
    assert solution.count_diaries(missing) == 0
