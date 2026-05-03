"""Week 11 assignment contract tests."""

import sys
from pathlib import Path

import pytest

STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))
sys.modules.pop("solution", None)

from solution import (
    Book,
    Enrollment,
    EnrollmentStatus,
    Student,
    Task,
    calculate_average,
    calculate_value,
    count_by_major,
    filter_by_major,
    find_by_isbn,
    find_student,
    get_top_student,
    load_books,
    save_books,
    update_stock,
)
from library_system_fixed import BookStatus, Library, LibraryBook
from practice1_student_dataclass import Student as PracticeStudent
from practice2_type_hints import calculate_average as practice_calculate_average
from practice2_type_hints import find_student as practice_find_student
from practice3_enum_status import Enrollment as PracticeEnrollment
from practice3_enum_status import EnrollmentStatus as PracticeEnrollmentStatus
from practice4_json_conversion import Task as PracticeTask
from practice5_enrollment_system import Enrollment as AdvancedEnrollment
from practice6_refactor_to_dataclass import Book as PracticeBook
from practice6_refactor_to_dataclass import calculate_value as practice_calculate_value


def test_student_dataclass_defaults_and_repr():
    student = Student("小北", 20)
    assert student.major == "未定"
    assert student.gpa == 0.0
    assert "Student" in repr(student)

    full = Student("阿码", 21, "计算机科学", 3.8)
    assert full.major == "计算机科学"
    assert full.gpa == 3.8

    practice_student = PracticeStudent("老潘", 42)
    assert practice_student.major == "未定"
    assert practice_student.gpa == 0.0


def test_type_hint_practice_functions():
    students = [
        {"name": "小北", "major": "计算机科学", "gpa": 3.5},
        {"name": "阿码", "major": "数学", "gpa": 3.9},
        {"name": "老潘", "major": "计算机科学", "gpa": 3.2},
    ]

    assert calculate_average([80, 90, 100]) == 90.0
    assert calculate_average([]) == 0.0
    assert find_student(students, "阿码") == students[1]
    assert find_student(students, "不存在") is None
    assert filter_by_major(students, "计算机科学") == [students[0], students[2]]
    assert count_by_major(students) == {"计算机科学": 2, "数学": 1}
    assert get_top_student(students) == students[1]
    assert get_top_student([]) is None

    assert practice_calculate_average([70, 80]) == 75.0
    assert practice_find_student(students, "小北") == students[0]


def test_enrollment_status_transitions():
    enrollment = Enrollment("小北", "Python 程序设计")
    assert enrollment.status == EnrollmentStatus.PENDING
    assert enrollment.can_approve() is True

    enrollment.approve("teacher1")
    assert enrollment.status == EnrollmentStatus.APPROVED
    assert enrollment.approved_date is not None
    assert enrollment.can_complete() is True

    enrollment.complete(95.5)
    assert enrollment.status == EnrollmentStatus.COMPLETED
    assert enrollment.grade == 95.5

    with pytest.raises(ValueError):
        enrollment.approve("teacher2")

    practice_enrollment = PracticeEnrollment("阿码", "数据建模")
    assert practice_enrollment.status == PracticeEnrollmentStatus.PENDING
    practice_enrollment.reject()
    assert practice_enrollment.status == PracticeEnrollmentStatus.REJECTED


def test_enrollment_reject_path():
    enrollment = Enrollment(student_id="S001", course_id="CS101")
    enrollment.reject("teacher1", "名额已满")
    assert enrollment.status == EnrollmentStatus.REJECTED
    assert enrollment.reject_reason == "名额已满"
    with pytest.raises(ValueError):
        enrollment.complete(80)

    advanced = AdvancedEnrollment(student_id="S002", course_id="CS102")
    advanced.approve("teacher2")
    assert advanced.can_complete() is True


def test_task_json_conversion(tmp_path):
    task = Task(title="完成 Week 11 作业", priority="high", tags=["Python", "dataclass"])
    data = task.to_dict()
    assert data == {
        "title": "完成 Week 11 作业",
        "priority": "high",
        "completed": False,
        "tags": ["Python", "dataclass"],
    }

    restored = Task.from_dict({"title": "补测试"})
    assert restored.priority == "medium"
    assert restored.tags == []

    path = tmp_path / "task.json"
    task.to_json(path)
    assert Task.from_json(path) == task

    practice_task = PracticeTask.from_dict({"title": "复盘"})
    assert practice_task.priority == "medium"
    assert practice_task.completed is False


def test_book_refactor_contract(tmp_path):
    books = [
        Book("Python 编程", "张三", "978-7-111-12345-6", 89.0, 10, "编程"),
        Book("算法导论", "李四", "978-7-111-23456-7", 128.0, 5, "算法"),
    ]

    found = find_by_isbn(books, "978-7-111-12345-6")
    assert found is books[0]
    assert found.is_available() is True
    assert found.get_value() == 890.0

    update_stock(books, "978-7-111-12345-6", -2)
    assert books[0].stock == 8
    assert calculate_value(books) == 89.0 * 8 + 128.0 * 5

    path = tmp_path / "books.json"
    save_books(books, path)
    assert load_books(path) == books

    practice_books = [PracticeBook("测试驱动", "小北", "ISBN-1", 50.0, 2, "编程")]
    assert practice_calculate_value(practice_books) == 100.0


def test_library_system_fixed_contract():
    book = LibraryBook("Python 入门", "阿码", "ISBN-2")
    library = Library([book])

    assert library.borrow_book("ISBN-2", "S001", days=7) is True
    assert book.status == BookStatus.BORROWED
    assert book.borrower_id == "S001"
    assert book.due_date is not None

    with pytest.raises(ValueError):
        library.borrow_book("ISBN-2", "S002")

    assert library.return_book("ISBN-2") is True
    assert book.status == BookStatus.AVAILABLE
    assert library.borrow_book("missing", "S001") is False
