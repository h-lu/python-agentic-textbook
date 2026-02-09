"""
示例：状态管理——让变化可预测（第 4 节）

本示例演示：
1. 用 Enum 定义任务状态
2. 在 dataclass 中使用 Enum 类型
3. 实现状态转换方法（带验证）
4. 防止非法状态转换

运行方式：python3 chapters/week_11/examples/04_task_state.py
预期输出：演示状态管理和状态转换验证
"""

from enum import Enum
from dataclasses import dataclass

# =====================
# 1. 用 Enum 定义状态
# =====================

class TaskStatus(Enum):
    """任务可能的状态"""
    TODO = "待办"
    IN_PROGRESS = "进行中"
    DONE = "已完成"

print("=== Enum 定义状态 ===")
print(f"TaskStatus.TODO = {TaskStatus.TODO}")
print(f"TaskStatus.TODO.value = {TaskStatus.TODO.value}")
print()

# =====================
# 2. dataclass 使用 Enum 类型
# =====================

@dataclass
class Task:
    """任务数据模型（带状态管理）"""
    title: str
    priority: str
    status: TaskStatus = TaskStatus.TODO

    def mark_in_progress(self) -> None:
        """标记为进行中"""
        if self.status == TaskStatus.DONE:
            raise ValueError("已完成的任务不能重新开始")
        self.status = TaskStatus.IN_PROGRESS

    def mark_done(self) -> None:
        """标记为完成"""
        self.status = TaskStatus.DONE

    def reset(self) -> None:
        """重置为待办"""
        if self.status == TaskStatus.DONE:
            raise ValueError("已完成的任务不能重置")
        self.status = TaskStatus.TODO

print("=== 创建任务并转换状态 ===")
task = Task("写作业", "high")
print(f"初始状态：{task.status.value}")

task.mark_in_progress()
print(f"开始后：  {task.status.value}")

task.mark_done()
print(f"完成后：  {task.status.value}\n")

# =====================
# 3. 防止非法状态转换
# =====================

print("=== 防止非法状态转换 ===")
task2 = Task("复习", "medium")
task2.mark_in_progress()
task2.mark_done()
print(f"task2 状态：{task2.status.value}")

try:
    task2.mark_in_progress()  # 已完成 → 进行中：非法！
except ValueError as e:
    print(f"❌ 阻止非法转换：{e}\n")

# =====================
# 4. 状态转换图
# =====================

print("=== 状态转换图 ===")
print("""
     ┌─────────┐
     │  TODO   │
     └────┬────┘
          │ mark_in_progress()
          ▼
     ┌─────────────┐
     │ IN_PROGRESS │
     └──────┬──────┘
            │ mark_done()
            ▼
       ┌─────────┐
       │  DONE   │
       └─────────┘

规则：
- TODO → IN_PROGRESS ✓
- IN_PROGRESS → DONE ✓
- DONE → IN_PROGRESS ✗ (已完成的任务不能重新开始)
""")

# =====================
# 5. 完整的状态转换演示
# =====================

print("=== 完整的状态转换演示 ===")

@dataclass
class ManagedTask:
    """带完整状态管理的任务"""
    title: str
    status: TaskStatus = TaskStatus.TODO

    def start(self) -> None:
        """开始任务"""
        if self.status != TaskStatus.TODO:
            raise ValueError(f"只有待办任务可以开始，当前状态：{self.status.value}")
        self.status = TaskStatus.IN_PROGRESS

    def complete(self) -> None:
        """完成任务"""
        if self.status != TaskStatus.IN_PROGRESS:
            raise ValueError(f"只有进行中的任务可以完成，当前状态：{self.status.value}")
        self.status = TaskStatus.DONE

    def __str__(self) -> str:
        return f"[{self.status.value}] {self.title}"

# 正常流程
task3 = ManagedTask("学习 dataclass")
print(task3)
task3.start()
print(task3)
task3.complete()
print(task3)

# 非法转换
print("\n尝试非法转换：")
try:
    task3.start()  # DONE → IN_PROGRESS：非法
except ValueError as e:
    print(f"❌ {e}")
print()

# =====================
# 6. 按状态筛选任务
# =====================

print("=== 按状态筛选任务 ===")

def get_tasks_by_status(tasks: list[ManagedTask], status: TaskStatus) -> list[ManagedTask]:
    """按状态筛选任务"""
    return [task for task in tasks if task.status == status]

all_tasks = [
    ManagedTask("任务A", TaskStatus.TODO),
    ManagedTask("任务B", TaskStatus.IN_PROGRESS),
    ManagedTask("任务C", TaskStatus.DONE),
    ManagedTask("任务D", TaskStatus.TODO),
]

todo_tasks = get_tasks_by_status(all_tasks, TaskStatus.TODO)
print(f"待办任务：{len(todo_tasks)} 个")
for task in todo_tasks:
    print(f"  - {task}")

done_tasks = get_tasks_by_status(all_tasks, TaskStatus.DONE)
print(f"已完成：{len(done_tasks)} 个")
for task in done_tasks:
    print(f"  - {task}")
print()

# =====================
# 7. 状态管理最佳实践
# =====================

print("=" * 50)
print("状态管理最佳实践：\n")

print("1. 用 Enum 定义状态")
print("   → 状态的值是有限的、明确的\n")

print("2. 封装状态转换逻辑")
print("   → 用方法控制状态变化，不直接修改 status\n")

print("3. 验证状态转换")
print("   → 在转换方法中检查当前状态，阻止非法转换\n")

print("4. 为状态转换编写测试")
print("   → 用 pytest 测试正常和非法转换路径\n")

print("5. 用状态机思维设计")
print("   → 画出状态转换图，明确允许的转换路径\n")

print("=" * 50)
print("状态管理不是'过度工程'——")
print("它让数据变化可预测、可测试、可维护。")
