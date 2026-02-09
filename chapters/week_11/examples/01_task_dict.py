"""
示例：用字典存储任务数据（第 1 节）

本示例演示：
1. 用字典存储任务的多个属性
2. 字典的三个痛点（字段不明确、拼写错误静默失败、IDE 无法智能提示）
3. 字典访问可能出现的 KeyError

运行方式：python3 chapters/week_11/examples/01_task_dict.py
预期输出：展示字典存储任务的基本用法和潜在问题
"""

# =====================
# 1. 基础用法：字典存储任务
# =====================

task1 = {
    "title": "完成 Week 11 作业",
    "description": "写 dataclass 和类型提示的练习",
    "due_date": "2026-02-15",
    "priority": "high",
    "completed": False
}

print("=== 基础用法 ===")
print(f"任务：{task1['title']}")
print(f"截止：{task1['due_date']}")
print(f"已完成：{task1['completed']}\n")

# =====================
# 2. 字典的痛点演示
# =====================

print("=== 痛点 1：字段不明确 ===")
# 创建任务时可能忘记某些字段
task2 = {
    "title": "复习 Week 10 内容",
    "priority": "medium"
    # 注意：没有 "completed" 字段
}

# 访问不存在的字段会报错
try:
    print(f"已完成：{task2['completed']}")  # KeyError!
except KeyError as e:
    print(f"❌ KeyError: 字段 {e} 不存在")
    print("   提示：你得记得每个任务字典应该有哪些字段\n")

# =====================
# 3. 痛点 2：拼写错误静默失败
# =====================

print("=== 痛点 2：拼写错误静默失败 ===")
task3 = {
    "title": "写代码练习",
    "priority": "high"
}

# 拼写错误：写成 "complted" 而不是 "completed"
task3["complted"] = True  # 静默添加了错误字段

print(f"任务：{task3['title']}")
print(f"已完成字段：{task3.get('completed', '未定义')}")
print(f"错误字段：{task3.get('complted', '未定义')}")
print("   问题：创建时没有报错，但字段名拼错了\n")

# =====================
# 4. 痛点 3：IDE 无法智能提示
# =====================

print("=== 痛点 3：IDE 无法智能提示 ===")
print("用字典时，IDE 不知道有哪些字段：")
print("  task['ti'] + Tab → 无法自动补全为 task['title']")
print("  task['pr'] + Tab → 无法自动补全为 task['priority']")
print("  你得手动输入完整字段名，容易出错\n")

# =====================
# 5. 函数中使用字典
# =====================

def get_incomplete_tasks(tasks):
    """获取未完成的任务列表"""
    incomplete = []
    for task in tasks:
        # 如果某个任务缺少 "completed" 字段，这里会报错
        if not task.get("completed", True):  # 用 get() 提供默认值
            incomplete.append(task)
    return incomplete

def get_high_priority_tasks(tasks):
    """获取高优先级任务"""
    high_priority = []
    for task in tasks:
        # 同样，如果缺少 "priority" 字段会有问题
        if task.get("priority") == "high":
            high_priority.append(task)
    return high_priority

print("=== 函数中使用字典 ===")
all_tasks = [
    {"title": "任务 A", "priority": "high", "completed": False},
    {"title": "任务 B", "priority": "low", "completed": True},
    {"title": "任务 C", "priority": "high", "completed": True},
]

incomplete = get_incomplete_tasks(all_tasks)
print(f"未完成任务数：{len(incomplete)}")

high_priority = get_high_priority_tasks(all_tasks)
print(f"高优先级任务数：{len(high_priority)}")
print()

# =====================
# 6. 字典的灵活性（优点也是缺点）
# =====================

print("=== 字典的灵活性 ===")
# 字典可以随意添加字段
task4 = {"title": "新任务"}
task4["priority"] = "medium"
task4["tags"] = ["Python", "学习"]
task4["estimated_hours"] = 2
task4["created_at"] = "2026-02-09"

print("动态添加的字段：")
for key, value in task4.items():
    print(f"  {key}: {value}")
print()
print("⚠️  问题：没有地方定义'任务必须有哪些字段'，全靠记忆和注释\n")

print("=" * 50)
print("字典总结：")
print("优点：灵活、动态、易用")
print("缺点：")
print("  1. 字段不明确，得靠记忆")
print("  2. 拼写错误不会立即报错")
print("  3. IDE 无法提供智能提示")
print("\n→ dataclass 就是为了解决这些问题")
