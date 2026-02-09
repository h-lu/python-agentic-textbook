"""Week 11 类型提示测试

测试类型提示相关的函数，验证类型标注的正确性。
注意：Python 不会在运行时强制检查类型，这些测试主要验证
函数在正确使用类型时能正常工作。
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "starter_code"))

from solution import (
    TaskWithStatus,
    TaskStatus,
    get_high_priority_tasks,
    get_tasks_by_status,
    find_task_by_title
)
from typing import List, Optional


class TestTypeHintedFunctions:
    """测试带类型提示的函数"""

    def test_get_high_priority_tasks_returns_list(self):
        """测试 get_high_priority_tasks 返回列表"""
        tasks = [
            TaskWithStatus(title="任务1", priority="high"),
            TaskWithStatus(title="任务2", priority="low"),
            TaskWithStatus(title="任务3", priority="high"),
        ]

        result = get_high_priority_tasks(tasks)

        # 验证返回类型是 List[TaskWithStatus]
        assert isinstance(result, list)
        assert all(isinstance(task, TaskWithStatus) for task in result)
        assert len(result) == 2

    def test_get_high_priority_tasks_empty_input(self):
        """测试空输入"""
        result = get_high_priority_tasks([])
        assert result == []

    def test_get_high_priority_tasks_no_matches(self):
        """测试没有匹配的情况"""
        tasks = [
            TaskWithStatus(title="任务1", priority="low"),
            TaskWithStatus(title="任务2", priority="medium"),
        ]

        result = get_high_priority_tasks(tasks)
        assert result == []

    def test_get_tasks_by_status(self):
        """测试按状态筛选"""
        tasks = [
            TaskWithStatus(title="T1", priority="high", status=TaskStatus.TODO),
            TaskWithStatus(title="T2", priority="high", status=TaskStatus.IN_PROGRESS),
            TaskWithStatus(title="T3", priority="high", status=TaskStatus.TODO),
        ]

        todo_tasks = get_tasks_by_status(tasks, TaskStatus.TODO)

        assert len(todo_tasks) == 2
        assert all(task.status == TaskStatus.TODO for task in todo_tasks)

    def test_get_tasks_by_status_with_in_progress(self):
        """测试筛选进行中任务"""
        tasks = [
            TaskWithStatus(title="T1", priority="high", status=TaskStatus.TODO),
            TaskWithStatus(title="T2", priority="high", status=TaskStatus.IN_PROGRESS),
            TaskWithStatus(title="T3", priority="high", status=TaskStatus.DONE),
        ]

        in_progress = get_tasks_by_status(tasks, TaskStatus.IN_PROGRESS)

        assert len(in_progress) == 1
        assert in_progress[0].title == "T2"

    def test_find_task_by_title_found(self):
        """测试找到任务"""
        tasks = [
            TaskWithStatus(title="任务1", priority="high"),
            TaskWithStatus(title="任务2", priority="low"),
        ]

        result = find_task_by_title(tasks, "任务1")

        # 返回类型应该是 Optional[TaskWithStatus]
        assert isinstance(result, TaskWithStatus)
        assert result.title == "任务1"

    def test_find_task_by_title_not_found(self):
        """测试找不到任务"""
        tasks = [
            TaskWithStatus(title="任务1", priority="high"),
        ]

        result = find_task_by_title(tasks, "不存在的任务")

        # 找不到应该返回 None
        assert result is None

    def test_find_task_by_title_empty_list(self):
        """测试空列表"""
        result = find_task_by_title([], "任务1")
        assert result is None

    def test_find_task_by_title_duplicate_titles(self):
        """测试重复标题（返回第一个）"""
        tasks = [
            TaskWithStatus(title="任务", priority="high"),
            TaskWithStatus(title="任务", priority="low"),
        ]

        result = find_task_by_title(tasks, "任务")

        assert result is not None
        assert result.title == "任务"
        # 应该返回第一个匹配的
        assert result.priority == "high"


class TestTypeHintBehavior:
    """测试类型提示的行为"""

    def test_python_does_not_enforce_types(self):
        """验证 Python 不会强制检查类型"""
        def typed_function(value: str) -> int:
            # 这个函数虽然标注 value: str，但 Python 不检查
            # 如果传入支持 len() 的类型也能运行
            return len(value)

        # 类型提示是 str，但传 list 也能运行（因为 list 有 len()）
        result = typed_function([1, 2, 3, 4, 5])  # 传了 list 而不是 str
        assert result == 5  # Python 不会因为类型不匹配而拒绝运行

    def test_type_hints_are_documentation(self):
        """测试类型提示作为文档的价值"""
        # 类型提示让函数签名更清晰
        # 通过 __annotations__ 可以访问
        def example(name: str, age: int = 18) -> bool:
            return age > 18

        annotations = example.__annotations__
        assert annotations["name"] == str
        assert annotations["age"] == int
        assert annotations["return"] == bool

    def test_optional_type(self):
        """测试 Optional 类型"""
        from typing import Optional

        def get_value(value: Optional[str]) -> str:
            return value or "default"

        assert get_value("hello") == "hello"
        assert get_value(None) == "default"
        assert get_value("") == "default"


class TestListTypeHints:
    """测试列表类型提示"""

    def test_list_of_tasks_type(self):
        """测试 List[Task] 类型"""
        tasks: List[TaskWithStatus] = [
            TaskWithStatus(title="T1", priority="high"),
            TaskWithStatus(title="T2", priority="low"),
        ]

        # 类型提示不会阻止错误的类型
        # 但如果访问 Task 特有的属性，会出错
        assert len(tasks) == 2
        assert all(isinstance(t, TaskWithStatus) for t in tasks)

    def test_list_type_with_comprehension(self):
        """测试列表推导式的类型"""
        tasks = [
            TaskWithStatus(title=f"任务{i}", priority="high")
            for i in range(3)
        ]

        assert len(tasks) == 3
        assert tasks[0].title == "任务0"
        assert tasks[2].title == "任务2"


class TestComplexTypeScenarios:
    """测试复杂类型场景"""

    def test_function_with_multiple_parameters(self):
        """测试多参数函数"""
        def combine(
            name: str,
            priority: str,
            completed: bool = False
        ) -> str:
            status = "完成" if completed else "未完成"
            return f"{name} ({priority}, {status})"

        result = combine("作业", "high", True)
        assert result == "作业 (high, 完成)"

    def test_nested_function_calls(self):
        """测试嵌套函数调用"""
        tasks = [
            TaskWithStatus(title="T1", priority="high", status=TaskStatus.TODO),
            TaskWithStatus(title="T2", priority="high", status=TaskStatus.DONE),
        ]

        # 先筛选 TODO，再筛选高优先级
        todo = get_tasks_by_status(tasks, TaskStatus.TODO)
        result = get_high_priority_tasks(todo)

        assert len(result) == 1
        assert result[0].title == "T1"

    def test_chained_operations(self):
        """测试链式操作"""
        tasks = [
            TaskWithStatus(title="T1", priority="high"),
            TaskWithStatus(title="T2", priority="low"),
        ]

        # 筛选 -> 查找
        high_priority = get_high_priority_tasks(tasks)
        found = find_task_by_title(high_priority, "T1")

        assert found is not None
        assert found.priority == "high"


class TestTypeHintEdgeCases:
    """测试类型提示的边界情况"""

    def test_none_for_optional_types(self):
        """测试 None 用于 Optional 类型"""
        def maybe_return(should_return: bool) -> Optional[str]:
            if should_return:
                return "value"
            return None

        assert maybe_return(True) == "value"
        assert maybe_return(False) is None

    def test_empty_collections(self):
        """测试空集合"""
        tasks: List[TaskWithStatus] = []

        result = get_high_priority_tasks(tasks)
        assert result == []

    def test_function_with_default_parameters(self):
        """测试带默认参数的函数"""
        def greet(name: str, greeting: str = "你好") -> str:
            return f"{greeting}，{name}!"

        assert greet("小北") == "你好，小北!"
        assert greet("小北", "Hello") == "Hello，小北!"

    def test_union_types(self):
        """测试联合类型"""
        from typing import Union

        def process(value: Union[str, int]) -> str:
            return str(value)

        assert process("text") == "text"
        assert process(123) == "123"
