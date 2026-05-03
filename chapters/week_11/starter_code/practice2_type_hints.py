"""练习 2：给函数添加类型提示。"""

try:
    from solution import (
        calculate_average,
        count_by_major,
        filter_by_major,
        find_student,
        get_top_student,
    )
except ImportError:  # pragma: no cover - package import fallback
    from .solution import (
        calculate_average,
        count_by_major,
        filter_by_major,
        find_student,
        get_top_student,
    )


__all__ = [
    "calculate_average",
    "find_student",
    "filter_by_major",
    "count_by_major",
    "get_top_student",
]


if __name__ == "__main__":
    students = [
        {"name": "小北", "major": "计算机科学", "gpa": 3.5},
        {"name": "阿码", "major": "数学", "gpa": 3.9},
        {"name": "老潘", "major": "计算机科学", "gpa": 3.2},
    ]
    print("平均分:", calculate_average([80, 90, 100]))
    print("查找阿码:", find_student(students, "阿码"))
    print("专业统计:", count_by_major(students))
