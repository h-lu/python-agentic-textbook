"""
示例：添加类型提示让代码更清晰（第 3 节）

本示例演示：
1. 给 dataclass 字段添加类型提示
2. 给函数参数和返回值添加类型提示
3. 常用类型提示语法（list、dict、Optional）
4. 类型提示的价值（自文档化、IDE 提示、AI 辅助）

运行方式：python3 chapters/week_11/examples/03_task_typed.py
预期输出：演示类型提示的用法和效果
"""

from dataclasses import dataclass
from typing import Optional, List

# =====================
# 1. dataclass 中的类型提示
# =====================

@dataclass
class Task:
    """任务数据模型（带完整类型提示）"""
    title: str
    description: str
    due_date: str
    priority: str
    completed: bool = False

print("=== dataclass 类型提示 ===")
task = Task("写作业", "完成 dataclass 练习", "2026-02-15", "high")
print(f"创建任务：{task}")
print(f"类型注解告诉 IDE：title 是 str，completed 是 bool\n")

# =====================
# 2. 函数类型提示
# =====================

def process_tasks(tasks: list[Task]) -> list[Task]:
    """
    处理任务列表，返回高优先级的任务

    Args:
        tasks: 任务列表

    Returns:
        高优先级任务列表
    """
    high_priority = []
    for task in tasks:
        if task.priority == "high":
            high_priority.append(task)
    return high_priority

def get_incomplete_tasks(tasks: list[Task]) -> list[Task]:
    """获取未完成的任务"""
    return [task for task in tasks if not task.completed]

print("=== 函数类型提示 ===")
all_tasks = [
    Task("任务A", "描述A", "2026-02-15", "high"),
    Task("任务B", "描述B", "2026-02-16", "medium", completed=True),
    Task("任务C", "描述C", "2026-02-17", "high"),
]

high_priority = process_tasks(all_tasks)
print(f"高优先级任务：{len(high_priority)} 个")
for task in high_priority:
    print(f"  - {task.title}")
print()

# =====================
# 3. Optional 类型
# =====================

def find_task_by_title(tasks: list[Task], title: str) -> Optional[Task]:
    """
    根据标题查找任务

    Args:
        tasks: 任务列表
        title: 要查找的标题

    Returns:
        找到的 Task 对象，如果不存在返回 None
    """
    for task in tasks:
        if task.title == title:
            return task
    return None

print("=== Optional 类型 ===")
found = find_task_by_title(all_tasks, "任务A")
if found:
    print(f"找到任务：{found.title}")
else:
    print("未找到任务")

not_found = find_task_by_title(all_tasks, "不存在的任务")
print(f"查找结果：{not_found}")  # None
print("→ Optional[Task] 告诉调用者：可能返回 None\n")

# =====================
# 4. 常用类型提示语法
# =====================

def demonstrate_types():
    """演示常用的类型提示"""

    # 基本类型
    def basic_types(name: str, age: int, score: float) -> bool:
        return age > 18

    # 列表类型（Python 3.9+ 可以用小写 list）
    def process_list(items: list[str]) -> list[int]:
        return [len(item) for item in items]

    # 字典类型
    def create_mapping(tasks: list[Task]) -> dict[str, Task]:
        return {task.title: task for task in tasks}

    # 可选类型
    def get_first(tasks: list[Task]) -> Optional[Task]:
        return tasks[0] if tasks else None

    # None 类型
    def return_none() -> None:
        print("这个函数不返回值")

    print("=== 类型提示示例 ===")
    print("str, int, bool, float：基本类型")
    print("list[Task]：Task 对象的列表")
    print("dict[str, Task]：键是字符串，值是 Task 的字典")
    print("Optional[Task]：可能是 Task 或 None")
    print("None：函数不返回值\n")

demonstrate_types()

# =====================
# 5. 类型提示不会强制检查
# =====================

print("=== 类型提示不会强制检查 ===")

def expect_task(task: Task) -> None:
    """这个函数期望接收 Task 对象"""
    print(f"任务标题：{task.title}")

# 正确调用
correct_task = Task("正确任务", "描述", "2026-02-15", "high")
expect_task(correct_task)

# 错误调用（类型不匹配，但 Python 不会在调用时报错）
print("\n尝试传入字符串（类型不匹配）：")
try:
    expect_task("不是 Task 对象")  # 类型提示只是提示，运行时不检查
except AttributeError as e:
    print(f"❌ 运行时报错：{e}")
    print("   类型提示在调用时不会阻止，只有运行到代码才会报错\n")

# =====================
# 6. 类型提示的三个价值
# =====================

print("=" * 50)
print("类型提示的三个价值：\n")

print("1. 代码自文档化")
print("   不用翻文档，看函数签名就知道传什么类型")
print("   def save(filepath: str, task: Task) -> None:\n")

print("2. IDE 智能提示")
print("   写了 tasks: list[Task]，IDE 知道每个元素是 Task")
print("   自动补全 .title、.completed 等属性\n")

print("3. AI 工具更容易理解")
print("   GitHub Copilot 看到类型提示能生成更准确的代码")
print("   告诉 AI '这里传 Task'，它知道 Task 有哪些字段\n")

print("=" * 50)
print("重要提醒：")
print("- Python 的类型提示只是提示，不会强制检查")
print("- 想要强制检查，需要用 mypy 等工具")
print("- 类型提示是给人、IDE、AI 看的，不是给 Python 解释器看的")
