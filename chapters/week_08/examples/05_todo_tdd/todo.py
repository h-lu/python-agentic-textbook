"""
Todo Manager - TDD 版本（测试驱动开发）

本模块通过 TDD 流程开发，包含：
1. delete_task - 通过 TDD 开发的功能

TDD 循环：
- 红：写测试，看到失败
- 绿：写最少代码让测试通过
- 重构：改进代码，保持测试通过

运行方式：
  python3 todo.py
"""


# 已有功能（假设之前已实现并测试）
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


# TDD 新开发的功能：delete_task
# 开发过程：
# 1. 先写 test_delete_task_success - 运行失败（红）
# 2. 实现 delete_task 让测试通过（绿）
# 3. 添加更多测试覆盖边界情况
# 4. 重构代码，保持测试通过

def delete_task(tasks, index):
    """
    删除指定索引的任务（1-based 索引）

    Args:
        tasks: 任务列表
        index: 要删除的任务索引（1-based）

    Returns:
        bool: 删除成功返回 True，索引非法返回 False
    """
    # 边界检查：确保索引在有效范围内
    if 1 <= index <= len(tasks):
        tasks.pop(index - 1)  # 转换为 0-based 索引
        return True
    return False


# 重构后的版本（保持测试通过）
def delete_task_refactored(tasks, index):
    """
    delete_task 的重构版本

    改进点：
    - 提取 list_index 变量，避免重复计算
    - 使用 0-based 索引进行边界检查，更直观
    """
    list_index = index - 1  # 转换为 0-based 索引

    if 0 <= list_index < len(tasks):
        tasks.pop(list_index)
        return True
    return False
