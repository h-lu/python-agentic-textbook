"""
示例：使用 fixture 管理测试数据

本例演示：
1. 用 @pytest.fixture 定义测试准备数据
2. fixture 可以返回任何类型的数据
3. 测试函数通过参数名使用 fixture
4. fixture 的 yield 语法（可选的清理代码）

运行方式：
  cd chapters/week_08/examples/03_todo_fixture
  pytest test_todo.py -v

  显示 print 输出：
  pytest test_todo.py -v -s

预期输出：
  所有测试通过，fixture 自动准备测试数据
"""

import pytest
from todo import add_task, mark_done, delete_task, count_done, count_pending


# ========== fixture 定义 ==========

@pytest.fixture
def empty_tasks():
    """提供一个空的任务列表"""
    return []


@pytest.fixture
def single_task():
    """提供一个只有单个任务的列表"""
    return [{"name": "买牛奶", "done": False}]


@pytest.fixture
def sample_tasks():
    """
    提供一组多样化的测试数据

    包含：
    - 2 个未完成任务
    - 1 个已完成任务
    """
    return [
        {"name": "买牛奶", "done": True},
        {"name": "写作业", "done": False},
        {"name": "运动", "done": False}
    ]


@pytest.fixture
def tasks_with_cleanup():
    """
    演示 yield 语法的 fixture

    yield 之前的代码：测试前执行（准备）
    yield 之后的代码：测试后执行（清理）
    """
    print("\n[fixture] 准备测试数据...")
    tasks = [{"name": "测试任务", "done": False}]

    yield tasks  # 把数据交给测试函数

    # 测试结束后执行清理
    print("[fixture] 测试结束，清理数据...")
    tasks.clear()


# ========== 使用 fixture 的测试 ==========

def test_add_task_to_empty_list(empty_tasks):
    """使用 empty_tasks fixture 测试添加任务"""
    # empty_tasks 是一个空列表，由 fixture 提供
    result = add_task(empty_tasks, "新任务")

    assert len(result) == 1
    assert result[0]["name"] == "新任务"
    assert result[0]["done"] == False


def test_mark_done_with_single_task(single_task):
    """使用 single_task fixture 测试标记完成"""
    # single_task 是 [{"name": "买牛奶", "done": False}]
    result = mark_done(single_task, 1)

    assert result == True
    assert single_task[0]["done"] == True


def test_count_done(sample_tasks):
    """使用 sample_tasks fixture 测试统计功能"""
    # sample_tasks 有 3 个任务，其中 1 个已完成
    done_count = count_done(sample_tasks)
    pending_count = count_pending(sample_tasks)

    assert done_count == 1
    assert pending_count == 2


def test_delete_from_sample(sample_tasks):
    """使用 sample_tasks fixture 测试删除"""
    # 删除第一个任务（买牛奶）
    result = delete_task(sample_tasks, 1)

    assert result == True
    assert len(sample_tasks) == 2
    # 剩下的应该是写作业和运动
    assert sample_tasks[0]["name"] == "写作业"
    assert sample_tasks[1]["name"] == "运动"


def test_fixture_with_cleanup(tasks_with_cleanup):
    """演示带清理的 fixture（加 -s 参数看输出）"""
    # 使用 tasks_with_cleanup，测试前后会有 print 输出
    assert len(tasks_with_cleanup) == 1
    assert tasks_with_cleanup[0]["name"] == "测试任务"


# ========== 多个 fixture 组合使用 ==========

def test_add_to_existing_tasks(sample_tasks):
    """在已有任务基础上添加新任务"""
    original_count = len(sample_tasks)

    add_task(sample_tasks, "新任务")

    assert len(sample_tasks) == original_count + 1
    assert sample_tasks[-1]["name"] == "新任务"


# ========== 反例：不使用 fixture 的问题 ==========

def test_without_fixture_problem():
    """
    反例：不使用 fixture 导致代码重复

    如果每个测试都要自己创建测试数据：
    1. 代码重复
    2. 修改测试数据格式时要改很多地方
    3. 测试数据不一致可能导致奇怪的问题
    """
    # 测试 1 自己创建数据
    tasks1 = [{"name": "任务1", "done": False}]
    mark_done(tasks1, 1)
    assert tasks1[0]["done"] == True

    # 测试 2 又要自己创建类似的数据
    tasks2 = [{"name": "任务2", "done": False}]
    mark_done(tasks2, 1)
    assert tasks2[0]["done"] == True

    # 如果以后任务字典的格式变了（比如加了一个 priority 字段），
    # 所有这些地方都要改！


# 对比：使用 fixture 后，数据格式只在 fixture 里定义一次
# 如果格式变了，只需要改 fixture，所有测试自动生效
