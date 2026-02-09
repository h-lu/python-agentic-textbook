"""
示例：基础 pytest 测试

本例演示：
1. 测试函数必须以 test_ 开头
2. 使用 assert 进行断言
3. 测试正常路径和边界情况

运行方式：
  cd chapters/week_08/examples/02_todo_with_tests
  pytest test_todo.py -v

  或者：
  python3 -m pytest test_todo.py -v

预期输出：
  所有测试通过（绿色小点）
"""

import pytest
from todo import add_task, mark_done, delete_task


def test_add_task_basic():
    """测试基本添加任务功能"""
    tasks = []
    result = add_task(tasks, "买牛奶")

    assert len(result) == 1
    assert result[0]["name"] == "买牛奶"
    assert result[0]["done"] == False


def test_add_task_strips_whitespace():
    """测试添加任务时去除首尾空格"""
    tasks = []
    result = add_task(tasks, "  买牛奶  ")

    assert result[0]["name"] == "买牛奶"


def test_mark_done_success():
    """测试成功标记任务完成"""
    tasks = [{"name": "买牛奶", "done": False}]
    result = mark_done(tasks, 1)

    assert result == True
    assert tasks[0]["done"] == True


def test_mark_done_invalid_index():
    """测试标记不存在的任务返回 False"""
    tasks = [{"name": "买牛奶", "done": False}]

    # 测试索引 0（不合法）
    assert mark_done(tasks, 0) == False
    # 测试超出范围的索引
    assert mark_done(tasks, 99) == False
    # 测试负数索引
    assert mark_done(tasks, -1) == False

    # 确保原任务未被修改
    assert tasks[0]["done"] == False


def test_delete_task_success():
    """测试成功删除任务"""
    tasks = [
        {"name": "买牛奶", "done": False},
        {"name": "写作业", "done": False}
    ]
    result = delete_task(tasks, 1)

    assert result == True
    assert len(tasks) == 1
    assert tasks[0]["name"] == "写作业"


def test_delete_task_invalid_index():
    """测试删除不存在的任务返回 False"""
    tasks = [{"name": "买牛奶", "done": False}]

    result = delete_task(tasks, 99)

    assert result == False
    assert len(tasks) == 1  # 任务列表应该保持不变


# 反例：错误的测试写法
def wrong_test_naming():
    """
    反例：测试函数不以 test_ 开头

    这个函数不会被 pytest 识别为测试！
    运行 pytest 时会显示 "collected 0 items"
    """
    tasks = []
    add_task(tasks, "测试")
    assert len(tasks) == 1


# 反例：没有断言的测试
def test_no_assertion():
    """
    反例：没有断言的测试

    这个测试总是会通过，但它什么都没验证！
    这只是调用了函数，没有检查结果是否正确。
    """
    tasks = []
    add_task(tasks, "买牛奶")
    # 缺少 assert，测试通过了也不知道对不对
    print(f"任务列表: {tasks}")  # 只在用 -s 时才看得到
