"""
Todo Manager - 被测模块（fixture 示例版本）

本模块提供待办事项管理的核心功能。

运行方式：
  python3 todo.py
"""


def add_task(tasks, task_name):
    """添加任务到列表"""
    task_name = task_name.strip()
    tasks.append({"name": task_name, "done": False})
    return tasks


def mark_done(tasks, index):
    """标记任务为完成（1-based 索引）"""
    if 1 <= index <= len(tasks):
        tasks[index - 1]["done"] = True
        return True
    return False


def delete_task(tasks, index):
    """删除指定索引的任务（1-based 索引）"""
    if 1 <= index <= len(tasks):
        tasks.pop(index - 1)
        return True
    return False


def count_done(tasks):
    """统计已完成任务数量"""
    return sum(1 for task in tasks if task["done"])


def count_pending(tasks):
    """统计未完成任务数量"""
    return sum(1 for task in tasks if not task["done"])
