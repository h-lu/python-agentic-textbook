"""
todo_manager.py - 待办事项管理器

贯穿 Week 08 的示例项目，用于演示 pytest 测试。

功能：
- add_task()：添加任务
- list_tasks()：列出所有任务
- mark_done()：标记任务为完成
- delete_task()：删除任务

运行方式：
  python3 todo_manager.py
"""


def add_task(tasks, task_name):
    """
    添加任务到列表

    Args:
        tasks: 任务列表
        task_name: 任务名称

    Returns:
        更新后的任务列表
    """
    task_name = task_name.strip()
    tasks.append({"name": task_name, "done": False})
    return tasks


def list_tasks(tasks):
    """
    列出所有任务（打印输出）

    Args:
        tasks: 任务列表
    """
    if not tasks:
        print("暂无任务")
        return

    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else " "
        print(f"{i}. [{status}] {task['name']}")


def mark_done(tasks, index):
    """
    标记任务为完成

    Args:
        tasks: 任务列表
        index: 任务索引（1-based）

    Returns:
        True 如果成功，False 如果索引无效
    """
    if 1 <= index <= len(tasks):
        tasks[index - 1]["done"] = True
        return True
    return False


def delete_task(tasks, index):
    """
    删除指定索引的任务

    Args:
        tasks: 任务列表
        index: 任务索引（1-based）

    Returns:
        True 如果成功，False 如果索引无效
    """
    list_index = index - 1
    if 0 <= list_index < len(tasks):
        tasks.pop(list_index)
        return True
    return False


def get_task_count(tasks):
    """
    获取任务总数和已完成数

    Args:
        tasks: 任务列表

    Returns:
        字典，包含 total 和 completed
    """
    total = len(tasks)
    completed = sum(1 for task in tasks if task["done"])
    return {"total": total, "completed": completed}


# =====================
# 测试代码
# =====================

if __name__ == "__main__":
    print("=== 待办事项管理器 ===")

    tasks = []

    # 添加任务
    add_task(tasks, "买牛奶")
    add_task(tasks, "写作业")
    add_task(tasks, "运动")

    # 列出任务
    print("\n任务列表：")
    list_tasks(tasks)

    # 标记完成
    mark_done(tasks, 1)
    print("\n标记第一个任务完成：")
    list_tasks(tasks)

    # 删除任务
    delete_task(tasks, 2)
    print("\n删除第二个任务：")
    list_tasks(tasks)

    # 统计
    stats = get_task_count(tasks)
    print(f"\n统计：共 {stats['total']} 个任务，已完成 {stats['completed']} 个")

    print("\n✓ 演示完成！")
