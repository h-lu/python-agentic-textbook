"""
Todo Manager - 被测模块

本模块提供待办事项管理的核心功能：
- add_task(): 添加任务
- list_tasks(): 列出所有任务
- mark_done(): 标记任务完成
- delete_task(): 删除任务（修复了边界检查）

运行方式：
  python3 todo.py

预期输出：
  模块自测通过
"""


def add_task(tasks, task_name):
    """
    添加任务到列表

    Args:
        tasks: 任务列表（列表的引用，会被修改）
        task_name: 任务名称字符串

    Returns:
        更新后的任务列表
    """
    task_name = task_name.strip()
    tasks.append({"name": task_name, "done": False})
    return tasks


def list_tasks(tasks):
    """
    列出所有任务

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
        index: 任务索引（1-based，用户视角）

    Returns:
        bool: 是否成功标记
    """
    if 1 <= index <= len(tasks):
        tasks[index - 1]["done"] = True
        return True
    return False


def delete_task(tasks, index):
    """
    删除指定索引的任务（修复了边界检查）

    Args:
        tasks: 任务列表
        index: 任务索引（1-based）

    Returns:
        bool: 是否成功删除
    """
    if 1 <= index <= len(tasks):
        tasks.pop(index - 1)
        return True
    return False


# 简单的自测代码
if __name__ == "__main__":
    print("=== Todo 模块自测 ===")

    # 测试 add_task
    tasks = []
    add_task(tasks, "测试任务")
    assert len(tasks) == 1
    assert tasks[0]["name"] == "测试任务"
    assert tasks[0]["done"] == False
    print("✓ add_task 测试通过")

    # 测试 mark_done
    mark_done(tasks, 1)
    assert tasks[0]["done"] == True
    print("✓ mark_done 测试通过")

    # 测试 delete_task 边界检查
    result = delete_task(tasks, 99)  # 不存在的索引
    assert result == False
    assert len(tasks) == 1  # 任务还在
    print("✓ delete_task 边界检查测试通过")

    print("\n=== 所有自测通过 ===")
