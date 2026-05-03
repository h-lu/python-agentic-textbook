"""Week 10 AI 协作练习：修复后的学生 JSON 管理器。"""

import json
from pathlib import Path


def load_students(filename):
    """从 JSON 文件加载学生列表；文件不存在或损坏时返回空列表。"""
    path = Path(filename)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return []

    return data if isinstance(data, list) else []


def save_students(filename, students):
    """保存学生列表到 JSON 文件。"""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(students, file, ensure_ascii=False, indent=2)


def validate_student(student):
    """验证学生记录。"""
    return (
        isinstance(student, dict)
        and isinstance(student.get("name"), str)
        and student.get("name").strip() != ""
        and isinstance(student.get("score"), (int, float))
    )


def add_student(filename, student):
    """添加一名学生；数据不合法时返回 False。"""
    if not validate_student(student):
        return False
    students = load_students(filename)
    students.append(student)
    save_students(filename, students)
    return True


def find_student(filename, name):
    """按姓名查找学生。"""
    for student in load_students(filename):
        if student.get("name") == name:
            return student
    return None
