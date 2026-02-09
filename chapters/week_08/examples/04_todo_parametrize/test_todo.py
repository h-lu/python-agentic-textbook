"""
示例：参数化测试（@pytest.mark.parametrize）

本例演示：
1. 用同一套测试逻辑测试多组数据
2. 覆盖各种边界情况
3. 使用 pytest.param 标记预期失败
4. 多参数组合（笛卡尔积）

运行方式：
  cd chapters/week_08/examples/04_todo_parametrize
  pytest test_todo.py -v

预期输出：
  一个测试函数运行多组数据，每组显示独立的结果
"""

import pytest
from todo import add_task, mark_done, is_valid_task_name, TaskError


# ========== 基础参数化测试 ==========

@pytest.mark.parametrize("task_name,expected_name", [
    ("买牛奶", "买牛奶"),               # 普通中文
    ("  买牛奶  ", "买牛奶"),           # 带空格，应该被 strip
    ("写作业！", "写作业！"),           # 带标点
    ("Task 123", "Task 123"),           # 英文数字混合
    ("🥛 买牛奶", "🥛 买牛奶"),         # 带 emoji
])
def test_add_task_various_names(task_name, expected_name):
    """
    测试各种任务名的处理

    一个测试函数，4 组数据，相当于写了 4 个测试
    """
    tasks = []
    result = add_task(tasks, task_name)

    assert result[0]["name"] == expected_name
    assert result[0]["done"] == False


# ========== 测试边界情况 ==========

@pytest.mark.parametrize("task_name,should_accept", [
    ("正常任务", True),                   # 正常情况
    ("  有空格  ", True),                # 带空格
    ("", False),                          # 空字符串，应该拒绝
    ("   ", False),                       # 只有空格
    ("a" * 100, True),                    # 刚好 100 字符
    ("a" * 101, False),                   # 101 字符，应该拒绝
    ("a" * 1000, False),                  # 超长任务名
])
def test_add_task_edge_cases(task_name, should_accept):
    """
    测试边界情况

    should_accept 为 True：应该成功添加
    should_accept 为 False：应该抛出 TaskError
    """
    tasks = []

    if should_accept:
        result = add_task(tasks, task_name)
        assert len(result) == 1
        assert result[0]["name"] == task_name.strip()
    else:
        # 应该抛出异常
        with pytest.raises(TaskError):
            add_task(tasks, task_name)


# ========== 标记预期失败（xfail） ==========

@pytest.mark.parametrize("task_name,expected", [
    ("正常任务", "正常任务"),
    pytest.param(
        "", "",
        marks=pytest.mark.xfail(reason="空任务名校验会抛出异常，不是返回空字符串")
    ),
])
def test_add_task_with_xfail(task_name, expected):
    """
    演示 xfail：标记已知会失败的测试

    xfail 的测试如果失败了，显示 X 而不是 F
    如果意外通过了，会显示 XPASS（提醒你可能修好了）
    """
    tasks = []
    result = add_task(tasks, task_name)
    assert result[0]["name"] == expected


# ========== 多参数组合（笛卡尔积） ==========

@pytest.mark.parametrize("initial_count", [0, 1, 5])
@pytest.mark.parametrize("task_name", ["任务A", "任务B"])
def test_add_task_multiple_dimensions(initial_count, task_name):
    """
    测试不同初始任务数量下的添加功能

    两个 @parametrize 装饰器会产生笛卡尔积：
    - 0 + 任务A
    - 0 + 任务B
    - 1 + 任务A
    - 1 + 任务B
    - 5 + 任务A
    - 5 + 任务B

    总共 3 × 2 = 6 个测试用例
    """
    # 准备初始任务
    tasks = [{"name": f"已有任务{i}", "done": False} for i in range(initial_count)]

    result = add_task(tasks, task_name)

    assert len(result) == initial_count + 1
    assert result[-1]["name"] == task_name


# ========== 参数化测试 is_valid_task_name ==========

@pytest.mark.parametrize("name,expected_valid", [
    # 有效的情况
    ("买牛奶", True),
    ("写作业", True),
    ("  有前后空格也有效  ", True),
    ("a" * 100, True),  # 边界值

    # 无效的情况
    ("", False),
    ("   ", False),
    ("a" * 101, False),  # 超过 100 字符
    ("a" * 1000, False),
])
def test_is_valid_task_name(name, expected_valid):
    """测试任务名校验函数"""
    result = is_valid_task_name(name)
    assert result == expected_valid


# ========== 反例：不使用参数化的冗余代码 ==========

def test_without_parametrize_redundant():
    """
    反例：不使用参数化导致大量重复代码

    下面的代码和上面的参数化版本功能相同，
    但要写很多行，而且容易遗漏情况。
    """
    # 测试空字符串
    assert is_valid_task_name("") == False

    # 测试只有空格
    assert is_valid_task_name("   ") == False

    # 测试正常中文
    assert is_valid_task_name("买牛奶") == True

    # 测试超长字符串
    assert is_valid_task_name("a" * 101) == False

    # 如果还要测试 emoji、英文、特殊字符……
    # 代码会越来越长，而且格式不统一

    # 对比参数化版本：
    # 所有测试数据集中在一个列表里，一目了然
    # 新增测试情况只需加一行
    # 测试逻辑只写一次，不会出错
