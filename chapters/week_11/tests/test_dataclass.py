"""Week 11 dataclass 基础测试

测试 dataclass 的创建、字段默认值、比较等功能。
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "starter_code"))

from solution import Task, Note


class TestDataclassCreation:
    """测试 dataclass 创建"""

    def test_create_with_all_required_fields(self):
        """测试提供所有必需字段创建"""
        task = Task(
            title="完成作业",
            description="写 dataclass 练习",
            due_date="2026-02-15",
            priority="high"
        )
        assert task.title == "完成作业"
        assert task.description == "写 dataclass 练习"
        assert task.due_date == "2026-02-15"
        assert task.priority == "high"

    def test_create_with_default_value(self):
        """测试使用默认值"""
        task = Task(
            title="完成作业",
            description="写 dataclass 练习",
            due_date="2026-02-15",
            priority="high"
        )
        # completed 有默认值 False
        assert task.completed is False

    def test_create_explicitly_override_default(self):
        """测试显式覆盖默认值"""
        task = Task(
            title="完成作业",
            description="写 dataclass 练习",
            due_date="2026-02-15",
            priority="high",
            completed=True
        )
        assert task.completed is True

    def test_create_missing_required_field(self):
        """测试缺少必需字段应抛出 TypeError"""
        with pytest.raises(TypeError):
            Task(
                title="完成作业",
                # 缺少 description, due_date, priority
            )


class TestDataclassEquality:
    """测试 dataclass 相等性比较"""

    def test_equal_objects(self):
        """测试相同字段值的两个实例相等"""
        task1 = Task("作业", "描述", "2026-02-15", "high")
        task2 = Task("作业", "描述", "2026-02-15", "high")
        assert task1 == task2

    def test_unequal_objects(self):
        """测试不同字段值的实例不相等"""
        task1 = Task("作业", "描述", "2026-02-15", "high")
        task2 = Task("作业", "描述", "2026-02-15", "low")
        assert task1 != task2

    def test_unequal_different_field(self):
        """测试不同字段导致不相等"""
        task1 = Task("作业1", "描述", "2026-02-15", "high")
        task2 = Task("作业2", "描述", "2026-02-15", "high")
        assert task1 != task2


class TestDataclassImmutability:
    """测试 dataclass 字段可变性"""

    def test_fields_are_mutable(self):
        """测试 dataclass 字段可以修改"""
        task = Task("作业", "描述", "2026-02-15", "high", completed=False)
        task.completed = True
        assert task.completed is True

    def test_can_modify_any_field(self):
        """测试可以修改任何字段"""
        task = Task("作业", "描述", "2026-02-15", "high")
        task.priority = "low"
        assert task.priority == "low"


class TestDataclassRepr:
    """测试 dataclass 的字符串表示"""

    def test_repr_contains_field_info(self):
        """测试 __repr__ 包含字段信息"""
        task = Task("作业", "描述", "2026-02-15", "high")
        repr_str = repr(task)
        assert "作业" in repr_str
        assert "high" in repr_str


class TestFieldDefaults:
    """测试字段默认值"""

    def test_immutability_default(self):
        """测试不可变类型的默认值（int, str, bool）"""
        note1 = Note(id="001", content="笔记1")
        note2 = Note(id="002", content="笔记2")

        # created_at 默认值应该是今天的日期字符串
        assert isinstance(note1.created_at, str)
        assert len(note1.created_at) > 0

    def test_mutable_default_with_factory(self):
        """测试可变默认值使用 field(default_factory=...)"""
        note1 = Note(id="001", content="笔记1")
        note2 = Note(id="002", content="笔记2")

        # 每个实例有独立的列表
        note1.tags.append("tag1")

        assert note1.tags == ["tag1"]
        assert note2.tags == []  # note2 的列表应该是空的

    def test_custom_tags_on_creation(self):
        """测试创建时指定 tags"""
        note = Note(id="001", content="笔记1", tags=["Python", "dataclass"])
        assert note.tags == ["Python", "dataclass"]


class TestDataclassWithMethods:
    """测试带方法的 dataclass"""

    def test_dataclass_can_have_methods(self):
        """测试 dataclass 可以有方法"""
        from solution import TaskWithStatus, TaskStatus

        task = TaskWithStatus(title="作业", priority="high")
        assert task.can_restart() is True

        task.mark_in_progress()
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.can_restart() is True

        task.mark_done()
        assert task.status == TaskStatus.DONE
        assert task.can_restart() is False


class TestEdgeCases:
    """测试边界情况"""

    def test_empty_string_fields(self):
        """测试空字符串字段"""
        task = Task("", "", "", "")
        assert task.title == ""
        assert task.description == ""

    def test_unicode_fields(self):
        """测试 Unicode 字段"""
        task = Task("作业🎯", "描述😊", "2026-02-15", "高")
        assert "作业🎯" in task.title

    def test_long_string_fields(self):
        """测试超长字符串"""
        long_title = "A" * 1000
        task = Task(long_title, "描述", "2026-02-15", "high")
        assert len(task.title) == 1000

    def test_special_characters_in_fields(self):
        """测试特殊字符"""
        task = Task("Title\nwith\nnewlines", "desc\twith\ttabs", "2026-02-15", "high")
        assert "\n" in task.title
        assert "\t" in task.description
