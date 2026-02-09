"""Week 11 冒烟测试 - 基础功能检查

这些测试验证 dataclass 和类型提示的最基本功能。
"""

import sys
from dataclasses import dataclass

# 添加 starter_code 到路径
sys.path.insert(0, 'starter_code')


def test_dataclass_basic_creation():
    """测试 dataclass 基本创建"""
    @dataclass
    class SimpleTask:
        title: str
        priority: str
        completed: bool = False

    task = SimpleTask(title="测试", priority="high")
    assert task.title == "测试"
    assert task.priority == "high"
    assert task.completed is False  # 使用默认值


def test_dataclass_field_access():
    """测试 dataclass 字段访问"""
    @dataclass
    class SimpleTask:
        title: str
        completed: bool = False

    task = SimpleTask(title="测试", completed=True)
    assert task.title == "测试"
    assert task.completed is True


def test_dataclass_equality():
    """测试 dataclass 相等性比较"""
    @dataclass
    class SimpleTask:
        title: str
        priority: str

    task1 = SimpleTask(title="测试", priority="high")
    task2 = SimpleTask(title="测试", priority="high")
    task3 = SimpleTask(title="测试", priority="low")

    assert task1 == task2  # 相同字段值
    assert task1 != task3  # 不同字段值


def test_dataclass_repr():
    """测试 dataclass 的字符串表示"""
    @dataclass
    class SimpleTask:
        title: str
        priority: str

    task = SimpleTask(title="测试", priority="high")
    repr_str = repr(task)
    assert "测试" in repr_str
    assert "high" in repr_str


def test_enum_basic():
    """测试 Enum 基本功能"""
    from enum import Enum

    class Status(Enum):
        TODO = 1
        DONE = 2

    assert Status.TODO.value == 1
    assert Status.DONE.value == 2
    assert Status.TODO == Status.TODO


def test_type_hints_syntax():
    """测试类型提示语法是否正确"""
    from typing import List, Optional

    def func1(name: str) -> bool:
        return len(name) > 0

    def func2(items: List[str]) -> int:
        return len(items)

    def func3(value: Optional[str]) -> str:
        return value or "default"

    # 这些函数应该能正常调用
    assert func1("test") is True
    assert func2(["a", "b"]) == 2
    assert func3(None) == "default"
    assert func3("hello") == "hello"
