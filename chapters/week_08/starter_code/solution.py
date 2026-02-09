"""
Week 08 作业参考实现

本文件提供练习 1-4 的参考实现。
学生可以先尝试自己完成，遇到困难时再参考。
"""

import pytest


# =====================
# 练习 1 & 2：基础测试和 Fixture
# =====================

# 假设 todo_manager.py 包含以下函数：
# - add_task(tasks, task_name)
# - mark_done(tasks, index)
# - delete_task(tasks, index)
# - list_tasks(tasks)


# Fixture 定义
@pytest.fixture
def empty_tasks():
    """提供一个空的任务列表"""
    return []


@pytest.fixture
def sample_tasks():
    """提供包含 3 个任务的列表"""
    return [
        {"name": "买牛奶", "done": True},
        {"name": "写作业", "done": False},
        {"name": "运动", "done": False}
    ]


# 练习 1：基础测试（至少 5 个）
# 以下代码假设从 todo_manager 导入函数

"""
from todo_manager import add_task, mark_done, delete_task


def test_add_task_success():
    '''测试正常添加任务'''
    tasks = []
    result = add_task(tasks, "买牛奶")

    assert len(result) == 1
    assert result[0]["name"] == "买牛奶"
    assert result[0]["done"] == False


def test_mark_done_success():
    '''测试标记任务完成'''
    tasks = [{"name": "买牛奶", "done": False}]
    result = mark_done(tasks, 1)

    assert result == True
    assert tasks[0]["done"] == True


def test_delete_task_success():
    '''测试删除任务'''
    tasks = [
        {"name": "买牛奶", "done": False},
        {"name": "写作业", "done": False}
    ]
    result = delete_task(tasks, 1)

    assert result == True
    assert len(tasks) == 1
    assert tasks[0]["name"] == "写作业"


def test_mark_done_invalid_index():
    '''测试标记不存在的任务'''
    tasks = [{"name": "买牛奶", "done": False}]
    result = mark_done(tasks, 99)

    assert result == False
    assert tasks[0]["done"] == False  # 状态不应改变


def test_delete_task_invalid_index():
    '''测试删除不存在的任务'''
    tasks = [{"name": "买牛奶", "done": False}]
    result = delete_task(tasks, 99)

    assert result == False
    assert len(tasks) == 1  # 列表不应改变


# 练习 2：使用 Fixture 的测试

def test_mark_done_with_fixture(sample_tasks):
    '''使用 fixture 测试标记完成'''
    result = mark_done(sample_tasks, 2)

    assert result == True
    assert sample_tasks[1]["done"] == True


def test_delete_task_with_fixture(sample_tasks):
    '''使用 fixture 测试删除任务'''
    result = delete_task(sample_tasks, 1)

    assert result == True
    assert len(sample_tasks) == 2
    assert sample_tasks[0]["name"] == "写作业"


def test_add_task_with_empty_fixture(empty_tasks):
    '''使用 empty_tasks fixture 测试添加'''
    result = add_task(empty_tasks, "新任务")

    assert len(result) == 1
    assert result[0]["name"] == "新任务"


# =====================
# 练习 3：参数化测试
# =====================

@pytest.mark.parametrize("task_name", [
    "买牛奶",
    "  买牛奶  ",
    "完成 Python 作业"
])
def test_add_task_various_names(task_name):
    '''测试各种任务名的处理'''
    tasks = []
    result = add_task(tasks, task_name)

    assert len(result) == 1


@pytest.mark.parametrize("invalid_index", [0, -1, 99])
def test_mark_done_invalid_indices(invalid_index):
    '''测试各种无效索引'''
    tasks = [{"name": "任务", "done": False}]
    result = mark_done(tasks, invalid_index)

    assert result == False
"""


# =====================
# 练习 4：TDD 实践
# =====================

# 练习 4 的实现示例（TDD 第二步：绿）
def add_task_with_priority(tasks, task_name, priority="medium"):
    """添加带优先级的任务

    priority 可以是 "high", "medium", "low"
    """
    valid_priorities = ["high", "medium", "low"]
    if priority not in valid_priorities:
        raise ValueError(f"优先级必须是 {valid_priorities}")

    tasks.append({
        "name": task_name,
        "done": False,
        "priority": priority
    })
    return tasks


# TDD 测试
def test_add_task_with_priority():
    """测试添加带优先级的任务"""
    tasks = []
    result = add_task_with_priority(tasks, "紧急任务", priority="high")

    assert len(result) == 1
    assert result[0]["name"] == "紧急任务"
    assert result[0]["priority"] == "high"
    assert result[0]["done"] == False


# 练习 4 的更多测试（边界情况）
def test_add_task_with_invalid_priority():
    """测试无效优先级应该抛出异常"""
    tasks = []

    with pytest.raises(ValueError):
        add_task_with_priority(tasks, "任务", priority="invalid")


if __name__ == "__main__":
    print("这是参考实现文件，请用 pytest 运行测试：")
    print("  pytest solution.py -v")
