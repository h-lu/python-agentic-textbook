"""
PyHelper 数据模型（Week 11：dataclass 建模）

本模块定义 PyHelper 的核心数据模型：
1. Note：学习笔记
2. NoteStatus：笔记状态（Enum）
3. StudyPlan：学习计划
4. JSON 序列化支持

运行方式：python3 -m chapters.week_11.examples.pyhelper.models
预期输出：演示 dataclass 模型的创建和序列化
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import date
from enum import Enum
from typing import List
from pathlib import Path


# =====================
# 1. 状态定义（Enum）
# =====================

class NoteStatus(Enum):
    """笔记状态"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


# =====================
# 2. 学习笔记模型
# =====================

@dataclass
class Note:
    """学习笔记数据模型

    字段说明：
        id: 笔记唯一标识
        content: 笔记内容
        tags: 标签列表
        created_at: 创建日期（ISO 格式字符串）
        status: 笔记状态
    """
    id: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: date.today().isoformat())
    status: NoteStatus = NoteStatus.DRAFT

    def publish(self) -> None:
        """发布笔记"""
        if self.status == NoteStatus.ARCHIVED:
            raise ValueError("已归档的笔记不能发布")
        self.status = NoteStatus.PUBLISHED

    def archive(self) -> None:
        """归档笔记"""
        self.status = NoteStatus.ARCHIVED

    def add_tag(self, tag: str) -> None:
        """添加标签（避免重复）"""
        if tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self) -> dict:
        """转换为字典（处理 Enum）"""
        data = asdict(self)
        data["status"] = self.status.value  # Enum 转字符串
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """从字典恢复（处理 Enum）"""
        data = data.copy()
        if "status" in data and isinstance(data["status"], str):
            data["status"] = NoteStatus(data["status"])
        return cls(**data)

    def to_json(self, filepath: str) -> None:
        """保存为 JSON 文件"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, filepath: str) -> "Note":
        """从 JSON 文件加载"""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


# =====================
# 3. 学习计划模型
# =====================

@dataclass
class StudyPlan:
    """学习计划数据模型"""
    title: str
    week: int
    goals: List[str] = field(default_factory=list)
    completed: bool = False

    def complete_goal(self, goal: str) -> None:
        """标记某个目标为完成（从列表中移除）"""
        if goal in self.goals:
            self.goals.remove(goal)
        if not self.goals:
            self.completed = True

    def to_dict(self) -> dict:
        """转换为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "StudyPlan":
        """从字典恢复"""
        return cls(**data)


# =====================
# 4. 演示和测试
# =====================

if __name__ == "__main__":
    print("=" * 60)
    print("PyHelper 数据模型演示")
    print("=" * 60)

    # 演示 1：创建笔记
    print("\n【演示 1】创建学习笔记")
    print("-" * 40)
    note = Note(
        id="20260209-001",
        content="今天学了 dataclass，很有用！\n\n关键点：\n1. @dataclass 装饰器\n2. 字段默认值\n3. 类型提示",
        tags=["Python", "dataclass"]
    )
    print(f"创建笔记：{note.id}")
    print(f"状态：{note.status.value}")
    print(f"标签：{note.tags}")

    # 演示 2：状态转换
    print("\n【演示 2】状态转换")
    print("-" * 40)
    print(f"初始状态：{note.status.value}")
    note.publish()
    print(f"发布后：  {note.status.value}")

    try:
        note.archive()
        note.publish()  # 已归档 → 发布：非法
    except ValueError as e:
        print(f"阻止非法转换：{e}")

    # 演示 3：标签管理
    print("\n【演示 3】标签管理")
    print("-" * 40)
    note.add_tag("学习")
    print(f"添加标签后：{note.tags}")
    note.add_tag("Python")  # 重复标签不会添加
    print(f"去重后：      {note.tags}")

    # 演示 4：JSON 序列化
    print("\n【演示 4】JSON 序列化")
    print("-" * 40)
    note_dict = note.to_dict()
    print("转换为字典：")
    print(json.dumps(note_dict, ensure_ascii=False, indent=2))

    # 演示 5：保存和加载
    print("\n【演示 5】保存和加载")
    print("-" * 40)
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        # 保存
        json_path = Path(tmpdir) / "note_20260209_001.json"
        note.to_json(json_path)
        print(f"✓ 保存到：{json_path.name}")

        # 加载
        loaded = Note.from_json(json_path)
        print(f"✓ 加载笔记：{loaded.id}")
        print(f"  状态：{loaded.status.value}")
        print(f"  标签：{loaded.tags}")
        print(f"  内容预览：{loaded.content[:30]}...")

    # 演示 6：学习计划
    print("\n【演示 6】学习计划")
    print("-" * 40)
    plan = StudyPlan(
        title="Week 11 学习计划",
        week=11,
        goals=[
            "理解 dataclass 的概念",
            "掌握类型提示语法",
            "实现状态管理"
        ]
    )
    print(f"计划：{plan.title}")
    print(f"目标：{len(plan.goals)} 个")

    plan.complete_goal("理解 dataclass 的概念")
    print(f"完成 1 个目标后：{len(plan.goals)} 个")

    plan.complete_goal("掌握类型提示语法")
    plan.complete_goal("实现状态管理")
    print(f"所有目标完成后，completed = {plan.completed}")

    # 演示 7：批量处理
    print("\n【演示 7】批量处理笔记")
    print("-" * 40)

    def get_notes_by_status(notes: List[Note], status: NoteStatus) -> List[Note]:
        """按状态筛选笔记"""
        return [note for note in notes if note.status == status]

    all_notes = [
        Note("001", "笔记 A", status=NoteStatus.DRAFT),
        Note("002", "笔记 B", status=NoteStatus.PUBLISHED),
        Note("003", "笔记 C", status=NoteStatus.DRAFT),
    ]

    draft_notes = get_notes_by_status(all_notes, NoteStatus.DRAFT)
    print(f"草稿笔记：{len(draft_notes)} 个")
    for note in draft_notes:
        print(f"  - {note.id}: {note.content}")

    # 总结
    print("\n" + "=" * 60)
    print("本周改进总结")
    print("=" * 60)
    print("✓ 用 @dataclass 定义 Note 和 StudyPlan 模型")
    print("✓ 用 Enum 管理笔记状态（draft/published/archived）")
    print("✓ 实现状态转换方法（publish/archive）")
    print("✓ 添加 JSON 序列化支持（to_json/from_json）")
    print("✓ 类型提示让代码更清晰（List[Note] 等）")
    print("=" * 60)
