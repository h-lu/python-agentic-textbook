"""Week 11 JSON 转换测试

测试 dataclass 与 JSON 的相互转换，包括 Enum 的序列化。
"""

import pytest
import json
import tempfile
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "starter_code"))

from solution import SerializableTask, SerializableNote
from dataclasses import asdict


class TestTaskDictConversion:
    """测试 Task 的字典转换"""

    def test_to_dict(self):
        """测试转换为字典"""
        task = SerializableTask(
            title="作业",
            priority="high",
            description="完成 dataclass 练习"
        )

        result = task.to_dict()

        assert isinstance(result, dict)
        assert result["title"] == "作业"
        assert result["priority"] == "high"
        assert result["description"] == "完成 dataclass 练习"
        assert result["completed"] is False

    def test_from_dict(self):
        """测试从字典创建"""
        data = {
            "title": "作业",
            "priority": "high",
            "description": "完成 dataclass 练习",
            "completed": True
        }

        task = SerializableTask.from_dict(data)

        assert task.title == "作业"
        assert task.priority == "high"
        assert task.description == "完成 dataclass 练习"
        assert task.completed is True

    def test_from_dict_with_missing_fields(self):
        """测试从字典创建（缺少字段）"""
        data = {
            "title": "作业"
        }

        task = SerializableTask.from_dict(data)

        assert task.title == "作业"
        assert task.priority == "medium"  # 默认值
        assert task.description == ""  # 默认值
        assert task.completed is False  # 默认值

    def test_round_trip_conversion(self):
        """测试往返转换（dict -> object -> dict）"""
        original = SerializableTask(
            title="作业",
            priority="high",
            description="描述",
            completed=True
        )

        # object -> dict
        data_dict = original.to_dict()

        # dict -> object
        restored = SerializableTask.from_dict(data_dict)

        # 恢复的对象应该和原对象相等
        assert restored.title == original.title
        assert restored.priority == original.priority
        assert restored.description == original.description
        assert restored.completed == original.completed


class TestTaskJsonFileOperations:
    """测试 Task 的 JSON 文件操作"""

    def test_to_json(self):
        """测试保存为 JSON 文件"""
        task = SerializableTask(
            title="作业",
            priority="high",
            description="完成 dataclass 练习"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmpfile = f.name

        try:
            task.to_json(tmpfile)

            # 验证文件存在且内容正确
            with open(tmpfile, 'r', encoding='utf-8') as f:
                data = json.load(f)

            assert data["title"] == "作业"
            assert data["priority"] == "high"
        finally:
            if os.path.exists(tmpfile):
                os.unlink(tmpfile)

    def test_from_json(self):
        """测试从 JSON 文件加载"""
        task = SerializableTask(
            title="作业",
            priority="high",
            description="完成 dataclass 练习"
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmpfile = f.name

        try:
            # 先保存
            task.to_json(tmpfile)

            # 再加载
            loaded = SerializableTask.from_json(tmpfile)

            assert loaded.title == "作业"
            assert loaded.priority == "high"
            assert loaded.description == "完成 dataclass 练习"
        finally:
            if os.path.exists(tmpfile):
                os.unlink(tmpfile)

    def test_json_file_round_trip(self):
        """测试 JSON 文件往返转换"""
        original = SerializableTask(
            title="作业",
            priority="high",
            description="描述",
            completed=True
        )

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmpfile = f.name

        try:
            # 保存
            original.to_json(tmpfile)

            # 加载
            loaded = SerializableTask.from_json(tmpfile)

            # 验证
            assert loaded.title == original.title
            assert loaded.priority == original.priority
            assert loaded.description == original.description
            assert loaded.completed == original.completed
        finally:
            if os.path.exists(tmpfile):
                os.unlink(tmpfile)


class TestNoteWithEnum:
    """测试带 Enum 的笔记模型"""

    def test_note_to_dict_with_enum(self):
        """测试笔记转换为字典（处理 Enum）"""
        note = SerializableNote(
            id="001",
            content="学习 dataclass",
            tags=["Python"],
            status=SerializableNote.NoteStatus.DRAFT
        )

        data = note.to_dict()

        assert data["id"] == "001"
        assert data["content"] == "学习 dataclass"
        assert data["tags"] == ["Python"]
        assert data["status"] == "草稿"  # Enum 转字符串

    def test_note_from_dict_with_enum(self):
        """测试从字典恢复笔记（处理 Enum）"""
        data = {
            "id": "001",
            "content": "学习 dataclass",
            "tags": ["Python"],
            "status": "已发布"  # 字符串
        }

        note = SerializableNote.from_dict(data)

        assert note.id == "001"
        assert note.content == "学习 dataclass"
        assert note.tags == ["Python"]
        assert note.status == SerializableNote.NoteStatus.PUBLISHED  # 字符串转 Enum

    def test_note_enum_round_trip(self):
        """测试笔记 Enum 的往返转换"""
        original = SerializableNote(
            id="001",
            content="学习 dataclass",
            status=SerializableNote.NoteStatus.PUBLISHED
        )

        # object -> dict
        data_dict = original.to_dict()
        assert data_dict["status"] == "已发布"

        # dict -> object
        restored = SerializableNote.from_dict(data_dict)
        assert restored.status == SerializableNote.NoteStatus.PUBLISHED


class TestNoteStateTransitions:
    """测试笔记状态转换"""

    def test_publish_draft_note(self):
        """测试发布草稿笔记"""
        note = SerializableNote(
            id="001",
            content="学习 dataclass",
            status=SerializableNote.NoteStatus.DRAFT
        )

        note.publish()
        assert note.status == SerializableNote.NoteStatus.PUBLISHED

    def test_archive_note(self):
        """测试归档笔记"""
        note = SerializableNote(
            id="001",
            content="学习 dataclass",
            status=SerializableNote.NoteStatus.PUBLISHED
        )

        note.archive()
        assert note.status == SerializableNote.NoteStatus.ARCHIVED

    def test_cannot_publish_archived_note(self):
        """测试不能发布已归档的笔记"""
        note = SerializableNote(
            id="001",
            content="学习 dataclass",
            status=SerializableNote.NoteStatus.PUBLISHED
        )
        note.archive()

        with pytest.raises(ValueError, match="已归档的笔记不能发布"):
            note.publish()


class TestAsdictUtility:
    """测试 asdict 工具函数"""

    def test_asdict_basic(self):
        """测试 asdict 基本功能"""
        from solution import Task

        task = Task("作业", "描述", "2026-02-15", "high", completed=True)
        data = asdict(task)

        assert data["title"] == "作业"
        assert data["completed"] is True

    def test_asdict_with_nested_structures(self):
        """测试 asdict 处理嵌套结构"""
        from dataclasses import dataclass

        @dataclass
        class Inner:
            value: int

        @dataclass
        class Outer:
            inner: Inner
            name: str

        obj = Outer(inner=Inner(value=42), name="test")
        data = asdict(obj)

        assert data["inner"]["value"] == 42
        assert data["name"] == "test"


class TestJsonEdgeCases:
    """测试 JSON 转换的边界情况"""

    def test_empty_strings(self):
        """测试空字符串"""
        task = SerializableTask(title="", priority="")

        data = task.to_dict()
        assert data["title"] == ""
        assert data["priority"] == ""

    def test_unicode_characters(self):
        """测试 Unicode 字符"""
        task = SerializableTask(title="作业🎯", priority="高")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            tmpfile = f.name

        try:
            task.to_json(tmpfile)
            loaded = SerializableTask.from_json(tmpfile)

            assert loaded.title == "作业🎯"
            assert loaded.priority == "高"
        finally:
            if os.path.exists(tmpfile):
                os.unlink(tmpfile)

    def test_special_characters(self):
        """测试特殊字符"""
        task = SerializableTask(
            title="Line1\nLine2",
            description="Tab\there",
            priority="high"
        )

        data = task.to_dict()
        assert "\n" in data["title"]
        assert "\t" in data["description"]

    def test_very_long_strings(self):
        """测试超长字符串"""
        long_title = "A" * 10000
        task = SerializableTask(title=long_title, priority="high")

        data = task.to_dict()
        assert len(data["title"]) == 10000

    def test_tags_with_multiple_items(self):
        """测试多个标签"""
        note = SerializableNote(
            id="001",
            content="学习 dataclass",
            tags=["Python", "dataclass", "类型提示", "测试", "JSON"]
        )

        data = note.to_dict()
        assert len(data["tags"]) == 5

        restored = SerializableNote.from_dict(data)
        assert len(restored.tags) == 5
        assert "Python" in restored.tags


class TestJsonWithDifferentStatuses:
    """测试不同状态的 JSON 序列化"""

    def test_all_note_statuses_serialize(self):
        """测试所有笔记状态都能正确序列化"""
        statuses = [
            SerializableNote.NoteStatus.DRAFT,
            SerializableNote.NoteStatus.PUBLISHED,
            SerializableNote.NoteStatus.ARCHIVED
        ]

        for status in statuses:
            note = SerializableNote(
                id="001",
                content="内容",
                status=status
            )

            data = note.to_dict()
            assert isinstance(data["status"], str)

            restored = SerializableNote.from_dict(data)
            assert restored.status == status
