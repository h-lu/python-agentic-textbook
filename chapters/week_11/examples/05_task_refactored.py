"""
示例：从字典到 dataclass 的完整重构（第 5 节）

本示例演示：
1. dataclass 的 JSON 序列化（to_dict / from_dict）
2. asdict() 函数的使用
3. 处理嵌套 dataclass
4. 完整的保存/加载流程

运行方式：python3 chapters/week_11/examples/05_task_refactored.py
预期输出：展示从字典到 dataclass 的完整重构流程
"""

import json
from dataclasses import dataclass, asdict
from typing import Optional, List
from pathlib import Path
import tempfile

# =====================
# 1. 定义带序列化的 dataclass
# =====================

@dataclass
class Task:
    """任务数据模型（支持 JSON 序列化）"""
    title: str
    priority: str
    description: str = ""
    completed: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """
        从字典创建 Task 对象

        Args:
            data: 包含任务数据的字典

        Returns:
            Task 对象
        """
        return cls(
            title=data["title"],
            priority=data["priority"],
            description=data.get("description", ""),
            completed=data.get("completed", False)
        )

    def to_dict(self) -> dict:
        """
        转换为字典

        Returns:
            任务数据的字典表示
        """
        return asdict(self)

print("=== 创建 Task 对象 ===")
task = Task("写作业", "high", "完成 dataclass 练习")
print(task)
print()

# =====================
# 2. dataclass 与字典的相互转换
# =====================

print("=== dataclass ↔ 字典转换 ===")

# dataclass → 字典
task_dict = task.to_dict()
print("转换为字典：")
print(json.dumps(task_dict, ensure_ascii=False, indent=2))
print()

# 字典 → dataclass
restored_task = Task.from_dict(task_dict)
print(f"恢复为 Task：{restored_task}")
print(f"相等吗？{task == restored_task}")
print()

# =====================
# 3. 保存和加载函数
# =====================

def save_task(filepath: str, task: Task) -> None:
    """
    保存任务到文件（JSON 格式）

    Args:
        filepath: 文件路径
        task: 要保存的任务
    """
    filepath = Path(filepath)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(task.to_dict(), f, ensure_ascii=False, indent=2)
    print(f"✓ 任务已保存到 {filepath}")

def load_task(filepath: str) -> Optional[Task]:
    """
    从文件加载任务

    Args:
        filepath: 文件路径

    Returns:
        Task 对象，如果文件不存在返回 None
    """
    filepath = Path(filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Task.from_dict(data)
    except FileNotFoundError:
        print(f"✗ 文件不存在：{filepath}")
        return None

print("=== 保存和加载演示 ===")
with tempfile.TemporaryDirectory() as tmpdir:
    # 保存任务
    json_file = Path(tmpdir) / "task.json"
    save_task(json_file, task)

    # 查看文件内容
    print("\nJSON 文件内容：")
    print(json_file.read_text(encoding="utf-8"))

    # 加载任务
    loaded = load_task(json_file)
    print(f"\n加载的任务：{loaded}")
    print(f"标题：{loaded.title}")
    print(f"优先级：{loaded.priority}")
    print()

# =====================
# 4. 处理任务列表
# =====================

def save_tasks(filepath: str, tasks: list[Task]) -> None:
    """保存任务列表到文件"""
    filepath = Path(filepath)
    with open(filepath, "w", encoding="utf-8") as f:
        data = [task.to_dict() for task in tasks]
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ 已保存 {len(tasks)} 个任务到 {filepath}")

def load_tasks(filepath: str) -> list[Task]:
    """从文件加载任务列表"""
    filepath = Path(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task.from_dict(item) for item in data]

print("=== 任务列表的保存和加载 ===")
all_tasks = [
    Task("写作业", "high", "完成 dataclass 练习"),
    Task("复习", "medium", "复习 Week 10 内容"),
    Task("预习", "low", "预习 Week 12", completed=True),
]

with tempfile.TemporaryDirectory() as tmpdir:
    # 保存列表
    list_file = Path(tmpdir) / "tasks.json"
    save_tasks(list_file, all_tasks)

    # 查看文件内容
    print("\nJSON 文件内容（列表）：")
    content = list_file.read_text(encoding="utf-8")
    print(content[:200] + "...\n")

    # 加载列表
    loaded_tasks = load_tasks(list_file)
    print(f"加载了 {len(loaded_tasks)} 个任务")
    for t in loaded_tasks:
        print(f"  - [{t.priority}] {t.title}")
    print()

# =====================
# 5. 处理嵌套 dataclass
# =====================

@dataclass
class TaskList:
    """任务列表（嵌套 dataclass）"""
    name: str
    tasks: list[Task]

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskList":
        """从字典创建"""
        return cls(
            name=data["name"],
            tasks=[Task.from_dict(t) for t in data["tasks"]]
        )

print("=== 嵌套 dataclass 序列化 ===")
project = TaskList(
    name="Week 11 学习任务",
    tasks=[
        Task("读教材", "high", "完成 Week 11 章节"),
        Task("写代码", "high", "完成所有练习"),
        Task("写作业", "medium", "提交作业"),
    ]
)

# 转换为字典
project_dict = project.to_dict()
print("转换为字典：")
print(json.dumps(project_dict, ensure_ascii=False, indent=2))
print()

# 恢复为对象
restored_project = TaskList.from_dict(project_dict)
print(f"恢复后：{restored_project.name}")
print(f"包含 {len(restored_project.tasks)} 个任务")
print()

# =====================
# 6. 数据迁移：兼容旧格式
# =====================

@dataclass
class TaskV2:
    """任务模型 v2：添加了 due_date 字段"""
    title: str
    priority: str
    due_date: str = "未设置"

    @classmethod
    def from_dict(cls, data: dict) -> "TaskV2":
        """从字典创建，支持 v1 格式迁移"""
        # v1 格式只有 title 和 priority
        if "due_date" not in data:
            print("  检测到 v1 格式，自动添加 due_date")
            data = data.copy()
            data["due_date"] = "未设置"
        return cls(**data)

print("=== 数据迁移演示 ===")
# 模拟 v1 格式数据
v1_data = {"title": "旧任务", "priority": "high"}
print("v1 格式数据：")
print(json.dumps(v1_data, ensure_ascii=False))

# 迁移到 v2
task_v2 = TaskV2.from_dict(v1_data)
print(f"\n迁移为 v2：{task_v2}")
print()

# =====================
# 7. 重构总结
# =====================

print("=" * 50)
print("从字典到 dataclass 的重构收益：\n")

print("之前（纯字典）：")
print("  - 字段名容易拼错：task['complted'] 静默失败")
print("  - 不知道有哪些字段：全靠记忆和注释")
print("  - IDE 无法提示：得手打完整字段名\n")

print("之后（dataclass）：")
print("  - 字段明确：task.title 自动补全")
print("  - 类型清晰：Task.from_dict() 知道返回类型")
print("  - 易于维护：结构定义在一处，修改方便\n")

print("关键技巧：")
print("  1. 用 to_dict() / from_dict() 配合 JSON")
print("  2. 用 asdict() 自动转换嵌套结构")
print("  3. 用 .get() 处理可选字段")
print("  4. 在 from_dict() 中做数据迁移\n")

print("=" * 50)
print("dataclass 不是取代字典，")
print("而是在代码中更好地组织数据。")
