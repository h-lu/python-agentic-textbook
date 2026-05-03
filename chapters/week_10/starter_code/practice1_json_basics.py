"""Week 10 练习 1：JSON 基础读写。"""

import json
from pathlib import Path


def create_student_data():
    """返回作业要求的学生示例数据。"""
    return {
        "name": "小北",
        "age": 20,
        "grades": [85, 90, 78],
        "is_active": True,
    }


def create_courses_data():
    """返回作业要求的嵌套课程数据。"""
    return {
        "student": "小北",
        "courses": [
            {"name": "Python", "score": 90},
            {"name": "数学", "score": 85},
        ],
    }


def write_json_file(data, filepath):
    """用 UTF-8 写入格式化 JSON 文件。"""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    return path


def read_json_file(filepath):
    """读取 JSON 文件并返回 Python 对象。"""
    with Path(filepath).open("r", encoding="utf-8") as file:
        return json.load(file)


def json_string_roundtrip(data):
    """演示 dumps/loads 的字符串往返。"""
    return json.loads(json.dumps(data, ensure_ascii=False))
