"""Week 10 assignment contract tests."""

import datetime
import json
import sys
from pathlib import Path

STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))

from practice1_json_basics import (
    create_courses_data,
    create_student_data,
    json_string_roundtrip,
    read_json_file,
    write_json_file,
)
from practice2_data_exchange import convert_format, export_data, import_data
from practice3_serialization import deserialize_event, serialize_event
from practice4_defensive_programming import load_books_collection, safe_load_json, validate_book_data
from practice5_data_migration import detect_version, migrate_data, migrate_v1_to_v2
from practice6_config_manager import ConfigManager
from student_manager_fixed import add_student, find_student, load_students


def test_practice1_json_basics(tmp_path):
    student = create_student_data()
    path = write_json_file(student, tmp_path / "student.json")
    assert read_json_file(path) == student
    assert json_string_roundtrip({"name": "小北"}) == {"name": "小北"}
    assert create_courses_data()["courses"][0]["score"] == 90


def test_practice2_data_exchange(tmp_path):
    data = {"title": "Python 学习笔记", "author": "小北"}
    json_path = tmp_path / "out" / "data.json"
    txt_path = tmp_path / "out" / "data.txt"

    assert export_data(data, json_path) is True
    assert import_data(json_path) == data
    assert convert_format(json_path, txt_path, "txt") is True
    assert "title: Python 学习笔记" in txt_path.read_text(encoding="utf-8")
    assert import_data(tmp_path / "missing.json") is None


def test_practice3_serialization_roundtrip():
    event = {
        "name": "Python 考试",
        "date": datetime.date(2026, 3, 15),
        "created_at": datetime.datetime(2026, 2, 9, 14, 30),
    }
    restored = deserialize_event(serialize_event(event))
    assert restored["date"] == datetime.date(2026, 3, 15)
    assert restored["created_at"] == datetime.datetime(2026, 2, 9, 14, 30)


def test_practice4_defensive_programming(tmp_path):
    valid = [
        {"title": "Python 编程", "author": "张三", "rating": 5},
        {"title": 123, "author": "李四"},
        "坏数据",
    ]
    path = tmp_path / "books.json"
    path.write_text(json.dumps(valid, ensure_ascii=False), encoding="utf-8")

    assert safe_load_json(path) == valid
    assert validate_book_data(valid[0]) == (True, [])
    assert validate_book_data(valid[1])[0] is False
    assert load_books_collection(path) == [valid[0]]
    assert safe_load_json(tmp_path / "missing.json") is None


def test_practice5_data_migration(tmp_path):
    old = {"books": [{"name": "Python 编程", "writer": "张三"}], "version": 1}
    migrated, report = migrate_v1_to_v2(old)
    assert detect_version(old) == 1
    assert migrated["version"] == 2
    assert migrated["books"][0]["title"] == "Python 编程"
    assert report

    input_path = tmp_path / "v1.json"
    output_path = tmp_path / "v2.json"
    input_path.write_text(json.dumps(old, ensure_ascii=False), encoding="utf-8")
    written, _report = migrate_data(input_path, output_path)
    assert written == json.loads(output_path.read_text(encoding="utf-8"))


def test_practice6_config_manager(tmp_path):
    path = tmp_path / "app_config.json"
    config = ConfigManager(path)
    config.set("theme", "dark")
    config.set("editor.font_size", 14)
    config.save()

    loaded = ConfigManager(path)
    assert loaded.get("theme") == "dark"
    assert loaded.get("editor.font_size") == 14
    assert loaded.get("missing", "fallback") == "fallback"
    assert loaded.export(tmp_path / "settings.txt", format="txt") is True


def test_student_manager_fixed(tmp_path):
    path = tmp_path / "students.json"
    assert load_students(path) == []
    assert add_student(path, {"name": "小北", "score": 90}) is True
    assert add_student(path, {"score": 80}) is False
    assert find_student(path, "小北") == {"name": "小北", "score": 90}
    assert find_student(path, "不存在") is None
