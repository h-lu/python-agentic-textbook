"""
Todo Manager - 被测模块（参数化测试版本）

本模块提供待办事项管理的核心功能，
增加了输入校验功能用于演示参数化测试。

运行方式：
  python3 todo.py
"""


class TaskError(ValueError):
    """任务相关的错误"""
    pass


def add_task(tasks, task_name):
    """
    添加任务到列表

    Raises:
        TaskError: 当任务名为空或超过 100 个字符时
    """
    task_name = task_name.strip()

    # 输入校验
    if not task_name:
        raise TaskError("任务名不能为空")
    if len(task_name) > 100:
        raise TaskError("任务名不能超过 100 个字符")

    tasks.append({"name": task_name, "done": False})
    return tasks


def mark_done(tasks, index):
    """标记任务为完成（1-based 索引）"""
    if 1 <= index <= len(tasks):
        tasks[index - 1]["done"] = True
        return True
    return False


def is_valid_task_name(name):
    """
    检查任务名是否有效

    有效标准：
    - 非空
    - 不超过 100 个字符
    """
    name = name.strip()
    return bool(name) and len(name) <= 100
