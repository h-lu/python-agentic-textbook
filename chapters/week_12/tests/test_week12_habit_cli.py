"""Week 12 habit-cli assignment contract tests."""

import json
import sys
from pathlib import Path

import pytest

STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))
sys.modules.pop("habit", None)
sys.modules.pop("solution", None)

import habit


@pytest.fixture
def isolated_habit_files(tmp_path, monkeypatch):
    monkeypatch.setattr(habit, "DATA_FILE", tmp_path / "habits.json")
    monkeypatch.setattr(habit, "LOG_FILE", tmp_path / "habit.log")
    monkeypatch.setattr(habit, "today_string", lambda: "2026-02-09")
    return tmp_path


def read_data():
    return json.loads(habit.DATA_FILE.read_text(encoding="utf-8"))


def test_parser_has_assignment_subcommands():
    parser = habit.create_parser()
    assert parser.parse_args(["add", "读书"]).command == "add"
    assert parser.parse_args(["list", "--active"]).active is True
    assert parser.parse_args(["checkin", "读书"]).command == "checkin"
    assert parser.parse_args(["log", "读书"]).command == "log"
    assert parser.parse_args(["delete", "读书"]).command == "delete"
    assert parser.parse_args(["stats", "--json"]).json is True


def test_add_list_and_duplicate_flow(isolated_habit_files, capsys):
    assert habit.main(["add", "每天学 Python 30 分钟", "--description", "Week 01-12 系统学习"]) == 0
    data = read_data()
    assert data["habits"][0]["name"] == "每天学 Python 30 分钟"
    assert data["habits"][0]["description"] == "Week 01-12 系统学习"
    assert data["habits"][0]["active"] is True

    assert habit.main(["list"]) == 0
    assert "习惯列表" in capsys.readouterr().out

    assert habit.main(["add", "每天学 Python 30 分钟"]) == 1
    assert "习惯已存在" in capsys.readouterr().err


def test_checkin_log_stats_and_delete_flow(isolated_habit_files, capsys):
    assert habit.main(["add", "读书"]) == 0
    assert habit.main(["checkin", "读书"]) == 0
    assert habit.main(["checkin", "读书"]) == 0

    data = read_data()
    assert data["habits"][0]["checkins"] == ["2026-02-09"]

    assert habit.main(["log", "读书"]) == 0
    assert "2026-02-09" in capsys.readouterr().out

    assert habit.main(["stats", "--json"]) == 0
    stats = json.loads(capsys.readouterr().out)
    assert stats == {"total_habits": 1, "active_habits": 1, "total_checkins": 1}

    assert habit.main(["delete", "读书"]) == 0
    assert read_data()["habits"] == []


def test_list_active_filters_archived_habits(isolated_habit_files, capsys):
    habit.save_data(
        {
            "habits": [
                {
                    "name": "读书",
                    "description": "",
                    "created_at": "2026-02-09",
                    "active": True,
                    "checkins": [],
                },
                {
                    "name": "旧习惯",
                    "description": "",
                    "created_at": "2026-02-09",
                    "active": False,
                    "checkins": ["2026-02-09"],
                },
            ]
        }
    )

    assert habit.main(["list", "--active"]) == 0
    output = capsys.readouterr().out
    assert "读书" in output
    assert "旧习惯" not in output


def test_error_exit_codes_and_stderr(isolated_habit_files, capsys):
    assert habit.main(["add", "   "]) == 1
    assert "不能为空" in capsys.readouterr().err

    assert habit.main(["checkin", "不存在的习惯"]) == 1
    assert "习惯不存在" in capsys.readouterr().err

    assert habit.main(["delete", "不存在的习惯"]) == 1
    assert "习惯不存在" in capsys.readouterr().err

    assert habit.main(["log", "   "]) == 1
    assert "不能为空" in capsys.readouterr().err

    assert habit.main(["delete", "   "]) == 1
    assert "不能为空" in capsys.readouterr().err


def test_logs_are_written_to_temp_file(isolated_habit_files):
    habit.main(["add", "写日记"])
    habit.main(["checkin", "写日记"])
    habit.main(["checkin", "不存在"])

    log_text = habit.LOG_FILE.read_text(encoding="utf-8")
    assert "INFO - 添加习惯：写日记" in log_text
    assert "INFO - 打卡成功：写日记" in log_text
    assert "WARNING - 习惯不存在：不存在" in log_text


def test_corrupt_data_file_recovers_with_empty_collection(isolated_habit_files):
    habit.DATA_FILE.write_text("{不是 json", encoding="utf-8")

    assert habit.load_data() == {"habits": []}
    assert "ERROR - 数据文件格式错误" in habit.LOG_FILE.read_text(encoding="utf-8")
