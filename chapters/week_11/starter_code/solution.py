"""Week 11 作业参考实现：dataclass、Enum、类型提示。"""

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Student:
    """练习 1：学生数据模型。"""

    name: str
    age: int
    major: str = "未定"
    gpa: float = 0.0


def calculate_average(scores: List[int]) -> float:
    """计算平均分；空列表返回 0.0。"""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def find_student(students: List[dict], name: str) -> Optional[dict]:
    """按姓名查找学生。"""
    for student in students:
        if student.get("name") == name:
            return student
    return None


def filter_by_major(students: List[dict], major: str) -> List[dict]:
    """筛选某个专业的学生。"""
    return [student for student in students if student.get("major") == major]


def count_by_major(students: List[dict]) -> Dict[str, int]:
    """统计每个专业的学生人数。"""
    counts: Dict[str, int] = {}
    for student in students:
        major = student.get("major", "未定")
        counts[major] = counts.get(major, 0) + 1
    return counts


def get_top_student(students: List[dict]) -> Optional[dict]:
    """获取 GPA 最高的学生。"""
    if not students:
        return None
    return max(students, key=lambda student: student.get("gpa", 0.0))


class EnrollmentStatus(Enum):
    """练习 3/5：选课状态。"""

    PENDING = "待审核"
    APPROVED = "已通过"
    REJECTED = "已拒绝"
    COMPLETED = "已完成"


@dataclass
class Enrollment:
    """选课记录，支持基础和进阶字段。"""

    student_name: str = ""
    course_name: str = ""
    student_id: str = ""
    course_id: str = ""
    status: EnrollmentStatus = EnrollmentStatus.PENDING
    enrolled_date: date = field(default_factory=date.today)
    approved_date: Optional[date] = None
    completed_date: Optional[date] = None
    reviewer: Optional[str] = None
    reject_reason: Optional[str] = None
    grade: Optional[float] = None
    notes: str = ""

    def approve(self, reviewer: str = "") -> None:
        """审核通过。"""
        if not self.can_approve():
            raise ValueError(f"{self.status.value}的课程不能再次审核")
        self.status = EnrollmentStatus.APPROVED
        self.reviewer = reviewer or None
        self.approved_date = date.today()

    def reject(self, reviewer: str = "", reason: str = "") -> None:
        """审核拒绝。"""
        if not self.can_reject():
            raise ValueError(f"{self.status.value}的课程不能拒绝")
        self.status = EnrollmentStatus.REJECTED
        self.reviewer = reviewer or None
        self.reject_reason = reason or None
        self.approved_date = date.today()

    def complete(self, grade: Optional[float] = None) -> None:
        """完成课程。"""
        if not self.can_complete():
            raise ValueError(f"{self.status.value}的课程不能完成")
        self.status = EnrollmentStatus.COMPLETED
        self.completed_date = date.today()
        self.grade = grade

    def can_approve(self) -> bool:
        return self.status == EnrollmentStatus.PENDING

    def can_reject(self) -> bool:
        return self.status == EnrollmentStatus.PENDING

    def can_complete(self) -> bool:
        return self.status == EnrollmentStatus.APPROVED


@dataclass
class Task:
    """练习 4：可转 JSON 的任务 dataclass。"""

    title: str
    priority: str
    completed: bool = False
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            title=data.get("title", ""),
            priority=data.get("priority", "medium"),
            completed=data.get("completed", False),
            tags=list(data.get("tags", [])),
        )

    def to_json(self, filepath: str) -> None:
        with Path(filepath).open("w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, filepath: str) -> "Task":
        with Path(filepath).open("r", encoding="utf-8") as file:
            data = json.load(file)
        return cls.from_dict(data)


@dataclass
class Book:
    """练习 6：从字典重构而来的图书模型。"""

    title: str
    author: str
    isbn: str
    price: float = 0.0
    stock: int = 0
    category: str = "未分类"

    def is_available(self) -> bool:
        return self.stock > 0

    def get_value(self) -> float:
        return self.price * self.stock

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(
            title=data.get("title", ""),
            author=data.get("author", ""),
            isbn=data.get("isbn", ""),
            price=float(data.get("price", 0.0)),
            stock=int(data.get("stock", 0)),
            category=data.get("category", "未分类"),
        )


def find_by_isbn(books: List[Book], isbn: str) -> Optional[Book]:
    for book in books:
        if book.isbn == isbn:
            return book
    return None


def update_stock(books: List[Book], isbn: str, quantity: int) -> Optional[Book]:
    book = find_by_isbn(books, isbn)
    if book:
        book.stock += quantity
    return book


def calculate_value(books: List[Book]) -> float:
    return sum(book.get_value() for book in books)


def save_books(books: List[Book], filepath: str) -> None:
    with Path(filepath).open("w", encoding="utf-8") as file:
        json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=2)


def load_books(filepath: str) -> List[Book]:
    with Path(filepath).open("r", encoding="utf-8") as file:
        data = json.load(file)
    return [Book.from_dict(item) for item in data]
