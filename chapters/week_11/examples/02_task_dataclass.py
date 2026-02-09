"""
示例：用 dataclass 定义任务模型（第 2 节）

本示例演示：
1. 用 @dataclass 装饰器定义数据类
2. 字段默认值的使用
3. dataclass 自动生成的方法（__init__、__repr__、__eq__）
4. 与手写类的对比

运行方式：python3 chapters/week_11/examples/02_task_dataclass.py
预期输出：展示 dataclass 的基本用法和优势
"""

from dataclasses import dataclass
from datetime import date

# =====================
# 1. dataclass 基础定义
# =====================

@dataclass
class Task:
    """任务数据模型"""
    title: str          # 任务标题（必需）
    description: str    # 任务描述（必需）
    due_date: str       # 截止日期（必需）
    priority: str       # 优先级（必需）
    completed: bool = False  # 是否完成（可选，默认 False）

print("=== 创建 Task 对象 ===")
# 创建任务（不传 completed，使用默认值）
task1 = Task(
    title="完成 Week 11 作业",
    description="写 dataclass 和类型提示的练习",
    due_date="2026-02-15",
    priority="high"
)

print(task1)  # 自动生成的 __repr__ 方法
print(f"\n访问字段：")
print(f"  标题：{task1.title}")
print(f"  截止：{task1.due_date}")
print(f"  已完成：{task1.completed}")
print()

# =====================
# 2. 默认值的使用
# =====================

print("=== 默认值演示 ===")
# 不传 completed，自动是 False
task2 = Task("复习", "复习 Week 10", "2026-02-16", "medium")
print(f"task2.completed = {task2.completed}")  # False

# 可以显式传 True
task3 = Task("预习", "预习 Week 12", "2026-02-17", "low", completed=True)
print(f"task3.completed = {task3.completed}")  # True
print()

# =====================
# 3. dataclass 自动生成的方法
# =====================

print("=== 自动生成的方法 ===")

# __repr__：友好的字符串表示
print("__repr__ 自动生成：")
print(task1)
print()

# __eq__：对象比较
task_a = Task("任务A", "描述A", "2026-02-15", "high")
task_b = Task("任务A", "描述A", "2026-02-15", "high")
task_c = Task("任务C", "描述C", "2026-02-16", "low")

print("__eq__ 自动生成：")
print(f"task_a == task_b: {task_a == task_b}")  # True
print(f"task_a == task_c: {task_a == task_c}")  # False
print()

# __init__：自动生成构造函数
print("__init__ 自动生成：")
print("不用手写 __init__ 方法，dataclass 自动处理")
print()

# =====================
# 4. 对比：手写类 vs dataclass
# =====================

print("=== 手写类（没有 dataclass）===")
print("如果不用 dataclass，需要手写这些代码：\n")

print("""
class Task:
    def __init__(self, title, description, due_date, priority, completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

    def __repr__(self):
        return f"Task(title={self.title!r}, completed={self.completed!r})"

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return (self.title == other.title and
                self.description == other.description and
                self.due_date == other.due_date and
                self.priority == other.priority and
                self.completed == other.completed)
""")

print("用了 @dataclass，上面 15+ 行代码变成 1 行装饰器！\n")

# =====================
# 5. 字段顺序和默认值规则
# =====================

print("=== 字段定义规则 ===")
print("1. 没有默认值的字段必须在有默认值的字段前面")
print("2. 如果违反规则，会报 SyntaxError\n")

# 正确的定义
@dataclass
class CorrectTask:
    title: str           # 无默认值
    priority: str = "medium"  # 有默认值

# 错误的定义（会报错）
# @dataclass
# class WrongTask:
#     title: str = "默认标题"  # 有默认值在前
#     priority: str           # 无默认值在后 → SyntaxError!

print("✓ 正确：无默认值的字段在前，有默认值的在后\n")

# =====================
# 6. 实际应用：任务列表
# =====================

print("=== 实际应用：任务列表 ===")

@dataclass
class SimpleTask:
    title: str
    priority: str
    completed: bool = False

tasks = [
    SimpleTask("写作业", "high"),
    SimpleTask("复习", "medium", completed=True),
    SimpleTask("预习", "low"),
]

print("所有任务：")
for task in tasks:
    status = "✓" if task.completed else "○"
    print(f"  [{status}] {task.title} ({task.priority})")

# 统计未完成任务
incomplete_count = sum(1 for t in tasks if not t.completed)
print(f"\n未完成：{incomplete_count}/{len(tasks)}")
print()

# =====================
# 7. 可变性（mutable）
# =====================

print("=== 可变性 ===")
task = SimpleTask("测试任务", "high")
print(f"初始状态：{task}")

task.completed = True
print(f"修改后：  {task}")
print()

print("=" * 50)
print("dataclass 总结：")
print("1. @dataclass 装饰器自动生成 __init__、__repr__、__eq__")
print("2. 字段默认值让某些参数变为可选")
print("3. 字段顺序：无默认值在前，有默认值在后")
print("4. 用 .field_name 访问属性，不用 ['key'] 索引")
print("5. 最小封装：只存数据，不写复杂逻辑")
