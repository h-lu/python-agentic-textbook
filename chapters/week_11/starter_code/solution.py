"""Week 11: dataclass 与类型提示 - 学生作业参考实现

本模块包含 dataclass、类型提示、状态管理相关的完整实现，供学生参考。

运行方式:
  python3 solution.py
"""

from dataclasses import dataclass, field, asdict
from datetime import date
from enum import Enum
from typing import List, Optional, Any
import json


# ==================== 1. dataclass 基础 ====================

@dataclass
class Task:
    """任务数据模型 - dataclass 基础示例"""
    title: str
    description: str
    due_date: str
    priority: str
    completed: bool = False


# ==================== 2. 状态管理 ====================

class TaskStatus(Enum):
    """任务状态枚举"""
    TODO = "待办"
    IN_PROGRESS = "进行中"
    DONE = "已完成"


@dataclass
class TaskWithStatus:
    """带状态管理的任务模型"""
    title: str
    priority: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO

    def mark_in_progress(self) -> None:
        """标记为进行中"""
        if self.status == TaskStatus.DONE:
            raise ValueError("已完成的任务不能重新开始")
        self.status = TaskStatus.IN_PROGRESS

    def mark_done(self) -> None:
        """标记为完成"""
        self.status = TaskStatus.DONE

    def can_restart(self) -> bool:
        """检查是否可以重新开始"""
        return self.status != TaskStatus.DONE


# ==================== 3. 字段默认值（含可变默认值）====================

@dataclass
class Note:
    """学习笔记数据模型 - 展示可变默认值用法"""
    id: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: date.today().isoformat())


# ==================== 4. JSON 序列化支持 ====================

@dataclass
class SerializableTask:
    """支持 JSON 序列化的任务模型"""
    title: str
    priority: str
    description: str = ""
    completed: bool = False

    def to_dict(self) -> dict:
        """转换为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SerializableTask":
        """从字典创建实例"""
        return cls(
            title=data.get("title", ""),
            priority=data.get("priority", "medium"),
            description=data.get("description", ""),
            completed=data.get("completed", False)
        )

    def to_json(self, filepath: str) -> None:
        """保存为 JSON 文件"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, filepath: str) -> "SerializableTask":
        """从 JSON 文件加载"""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)


@dataclass
class SerializableNote:
    """支持 JSON 序列化的笔记模型（含 Enum）"""
    class NoteStatus(Enum):
        DRAFT = "草稿"
        PUBLISHED = "已发布"
        ARCHIVED = "已归档"

    id: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: date.today().isoformat())
    status: NoteStatus = NoteStatus.DRAFT

    def to_dict(self) -> dict:
        """转换为字典（处理 Enum）"""
        data = asdict(self)
        data["status"] = self.status.value  # Enum 转字符串
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "SerializableNote":
        """从字典恢复（处理 Enum）"""
        data = data.copy()
        if "status" in data:
            data["status"] = cls.NoteStatus(data["status"])
        return cls(**data)

    def publish(self) -> None:
        """发布笔记"""
        if self.status == self.NoteStatus.ARCHIVED:
            raise ValueError("已归档的笔记不能发布")
        self.status = self.NoteStatus.PUBLISHED

    def archive(self) -> None:
        """归档笔记"""
        self.status = self.NoteStatus.ARCHIVED


# ==================== 5. 类型提示工具函数 ====================

def get_high_priority_tasks(tasks: List[TaskWithStatus]) -> List[TaskWithStatus]:
    """获取高优先级任务

    Args:
        tasks: 任务列表

    Returns:
        高优先级任务列表
    """
    return [task for task in tasks if task.priority == "high"]


def get_tasks_by_status(
    tasks: List[TaskWithStatus],
    status: TaskStatus
) -> List[TaskWithStatus]:
    """按状态筛选任务

    Args:
        tasks: 任务列表
        status: 目标状态

    Returns:
        匹配状态的任务列表
    """
    return [task for task in tasks if task.status == status]


def find_task_by_title(
    tasks: List[TaskWithStatus],
    title: str
) -> Optional[TaskWithStatus]:
    """按标题查找任务

    Args:
        tasks: 任务列表
        title: 任务标题

    Returns:
        找到的任务，或 None
    """
    for task in tasks:
        if task.title == title:
            return task
    return None


# ==================== 6. 状态转换验证 ====================

def validate_state_transition(
    current_status: TaskStatus,
    new_status: TaskStatus
) -> bool:
    """验证状态转换是否合法

    合法转换:
    - TODO -> IN_PROGRESS
    - IN_PROGRESS -> DONE
    - TODO -> DONE (直接完成)

    非法转换:
    - DONE -> TODO
    - DONE -> IN_PROGRESS

    Args:
        current_status: 当前状态
        new_status: 目标状态

    Returns:
        是否合法
    """
    # 已完成不能回到其他状态
    if current_status == TaskStatus.DONE:
        return False

    # 其他转换都合法
    return True


# ==================== 测试代码 ====================

if __name__ == "__main__":
    print("=== Week 11 作业参考实现测试 ===\n")

    # 测试 dataclass 基础
    print("--- 测试 dataclass 基础 ---")
    task1 = Task(
        title="完成 Week 11 作业",
        description="写 dataclass 和类型提示的练习",
        due_date="2026-02-15",
        priority="high"
    )
    print(f"任务: {task1.title}")
    print(f"已完成: {task1.completed}")

    # 测试状态管理
    print("\n--- 测试状态管理 ---")
    task2 = TaskWithStatus(title="写作业", priority="high")
    print(f"初始状态: {task2.status.value}")
    task2.mark_in_progress()
    print(f"标记进行中: {task2.status.value}")
    task2.mark_done()
    print(f"标记完成: {task2.status.value}")

    try:
        task2.mark_in_progress()
        print("错误：应该抛出异常")
    except ValueError as e:
        print(f"正确捕获异常: {e}")

    # 测试可变默认值
    print("\n--- 测试可变默认值 ---")
    note1 = Note(id="001", content="笔记1")
    note2 = Note(id="002", content="笔记2", tags=["Python"])
    note1.tags.append("dataclass")
    print(f"note1 tags: {note1.tags}")
    print(f"note2 tags: {note2.tags}")
    assert note2.tags == ["Python"], "可变默认值隔离测试失败"

    # 测试 JSON 序列化
    print("\n--- 测试 JSON 序列化 ---")
    import tempfile
    import os

    task3 = SerializableTask(
        title="测试任务",
        priority="high",
        description="测试 JSON 序列化"
    )

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        tmpfile = f.name

    try:
        task3.to_json(tmpfile)
        loaded = SerializableTask.from_json(tmpfile)
        print(f"原任务: {task3.title}")
        print(f"加载后: {loaded.title}")
        assert loaded.title == task3.title
        assert loaded.priority == task3.priority
        print("JSON 序列化测试通过")
    finally:
        os.unlink(tmpfile)

    # 测试类型提示函数
    print("\n--- 测试类型提示函数 ---")
    tasks = [
        TaskWithStatus(title="任务1", priority="high"),
        TaskWithStatus(title="任务2", priority="low"),
        TaskWithStatus(title="任务3", priority="high", status=TaskStatus.IN_PROGRESS)
    ]
    high_priority = get_high_priority_tasks(tasks)
    print(f"高优先级任务数: {len(high_priority)}")
    assert len(high_priority) == 2

    todo_tasks = get_tasks_by_status(tasks, TaskStatus.TODO)
    print(f"待办任务数: {len(todo_tasks)}")
    assert len(todo_tasks) == 2

    print("\n✓ 所有测试通过！")
