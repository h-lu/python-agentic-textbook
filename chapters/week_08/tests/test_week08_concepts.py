"""
test_week08_concepts.py - Week 08 核心概念测试

测试学生对本周核心概念的掌握：
- pytest 断言（正例、反例）
- pytest.raises 测试异常
- fixture 使用
- 参数化测试
"""

import pytest
import sys
from pathlib import Path

# 添加 examples 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))

from todo_manager import add_task, mark_done, delete_task, get_task_count


# =====================
# 1. 基本断言测试
# =====================

# 测试类型: 正例
# 覆盖场景: 正常添加任务
# 预期结果: 任务被添加到列表，返回更新后的列表
def test_add_task_basic():
    """测试基本添加任务功能"""
    tasks = []
    result = add_task(tasks, "买牛奶")

    assert len(result) == 1
    assert result[0]["name"] == "买牛奶"
    assert result[0]["done"] is False


# 测试类型: 正例
# 覆盖场景: 添加多个任务
# 预期结果: 所有任务都被正确添加
def test_add_task_multiple():
    """测试添加多个任务"""
    tasks = []
    add_task(tasks, "任务一")
    add_task(tasks, "任务二")
    add_task(tasks, "任务三")

    assert len(tasks) == 3
    assert tasks[0]["name"] == "任务一"
    assert tasks[1]["name"] == "任务二"
    assert tasks[2]["name"] == "任务三"


# 测试类型: 正例
# 覆盖场景: 任务名包含首尾空格
# 预期结果: 空格被自动去除
def test_add_task_strips_whitespace():
    """测试任务名自动去除首尾空格"""
    tasks = []
    add_task(tasks, "  买牛奶  ")

    assert tasks[0]["name"] == "买牛奶"


# 测试类型: 边界
# 覆盖场景: 添加空字符串任务名
# 预期结果: 空字符串被添加（不抛出异常）
def test_add_task_empty_string():
    """测试添加空字符串任务名"""
    tasks = []
    result = add_task(tasks, "")

    assert len(result) == 1
    assert result[0]["name"] == ""


# 测试类型: 边界
# 覆盖场景: 添加只有空格的任务名
# 预期结果: 空格被 strip 后变成空字符串
def test_add_task_whitespace_only():
    """测试添加只有空格的任务名"""
    tasks = []
    result = add_task(tasks, "   ")

    assert len(result) == 1
    assert result[0]["name"] == ""


# 测试类型: 反例
# 覆盖场景: 错误的预期结果
# 预期结果: 测试失败（用于演示失败情况，实际使用时可以删除或标记为 xfail）
@pytest.mark.xfail(reason="故意失败的测试，用于演示")
def test_add_task_wrong_expectation():
    """故意写错预期的测试（演示用）"""
    tasks = []
    result = add_task(tasks, "买牛奶")

    # 故意写错预期
    assert result[0]["name"] == "买面包"


# =====================
# 2. 异常测试（使用示例中的 storage 模块）
# =====================

# 导入 storage 模块来测试异常
sys.path.insert(0, str(Path(__file__).parent.parent / "examples" / "pyhelper"))
from storage import save_learning_log


# 测试类型: 反例
# 覆盖场景: 传入非列表数据到 save_learning_log
# 预期结果: 抛出 TypeError 异常
def test_save_learning_log_non_list_raises():
    """测试 save_learning_log 传入非列表抛出 TypeError"""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.json"
        with pytest.raises(TypeError, match="必须是列表"):
            save_learning_log("不是列表", file_path)


# 测试类型: 反例
# 覆盖场景: 传入包含非字典的列表
# 预期结果: 抛出 ValueError 异常
def test_save_learning_log_invalid_record_raises():
    """测试 save_learning_log 传入无效记录抛出 ValueError"""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.json"
        with pytest.raises(ValueError, match="必须是字典"):
            save_learning_log(["不是字典"], file_path)


# =====================
# 3. Fixture 使用
# =====================

@pytest.fixture
def empty_tasks():
    """
    提供一个空的任务列表

    测试类型: 正例
    覆盖场景: 每个测试使用全新的空列表
    预期结果: 返回空列表
    """
    return []


@pytest.fixture
def sample_tasks():
    """
    提供包含三个任务的列表

    测试类型: 正例
    覆盖场景: 测试需要预设数据的场景
    预期结果: 返回包含三个任务的列表
    """
    return [
        {"name": "买牛奶", "done": True},
        {"name": "写作业", "done": False},
        {"name": "运动", "done": False}
    ]


@pytest.fixture
def three_tasks_with_cleanup():
    """
    提供任务列表并在测试后清理

    测试类型: 正例
    覆盖场景: 演示 fixture 的清理功能
    预期结果: 测试前后有正确的状态
    """
    tasks = [
        {"name": "任务A", "done": False},
        {"name": "任务B", "done": False}
    ]
    yield tasks
    # 测试结束后清理
    tasks.clear()


# 测试类型: 正例
# 覆盖场景: 使用 empty_tasks fixture
def test_add_task_with_fixture(empty_tasks):
    """使用 empty_tasks fixture 测试添加任务"""
    result = add_task(empty_tasks, "新任务")

    assert len(result) == 1
    assert result[0]["name"] == "新任务"


# 测试类型: 正例
# 覆盖场景: 使用 sample_tasks fixture
def test_mark_done_with_fixture(sample_tasks):
    """使用 sample_tasks fixture 测试标记完成"""
    result = mark_done(sample_tasks, 2)  # 标记第二个任务

    assert result is True
    assert sample_tasks[1]["done"] is True


# 测试类型: 正例
# 覆盖场景: 使用 sample_tasks fixture 测试统计
def test_get_task_count_with_fixture(sample_tasks):
    """使用 sample_tasks fixture 测试统计功能"""
    stats = get_task_count(sample_tasks)

    assert stats["total"] == 3
    assert stats["completed"] == 1  # 只有第一个是完成的


# 测试类型: 边界
# 覆盖场景: 在空列表上操作
def test_mark_done_empty_list(empty_tasks):
    """测试在空列表上标记完成返回 False"""
    result = mark_done(empty_tasks, 1)

    assert result is False


# =====================
# 4. 参数化测试
# =====================

# 测试类型: 正例
# 覆盖场景: 多种有效任务名
# 预期结果: 所有有效任务名都能成功添加
@pytest.mark.parametrize("task_name", [
    "买牛奶",                    # 中文
    "Task 123",                  # 英文数字
    "写作业！",                  # 带标点
    "🥛 买牛奶",                 # 带 emoji
    "a-b_c.d",                   # 特殊字符
    "任务" + "x" * 50,           # 较长名称
])
def test_add_task_various_names(task_name):
    """参数化测试：各种有效任务名"""
    tasks = []
    result = add_task(tasks, task_name)

    assert len(result) == 1
    # 注意：如果任务名有首尾空格会被 strip
    assert result[0]["name"] == task_name.strip()


# 测试类型: 边界
# 覆盖场景: 各种无效索引
# 预期结果: 所有无效索引都返回 False
@pytest.mark.parametrize("invalid_index", [
    0,      # 零索引
    -1,     # 负数
    -100,   # 大负数
    99,     # 超出范围
    100,    # 远远超出范围
])
def test_mark_done_invalid_indices(invalid_index):
    """参数化测试：各种无效索引"""
    tasks = [{"name": "任务", "done": False}]
    result = mark_done(tasks, invalid_index)

    assert result is False


# 测试类型: 正例 + 边界
# 覆盖场景: 有效索引边界
# 预期结果: 有效索引返回 True，无效返回 False
@pytest.mark.parametrize("index,expected", [
    (1, True),   # 第一个
    (2, True),   # 第二个
    (3, True),   # 第三个
    (4, False),  # 超出范围
    (0, False),  # 无效索引
])
def test_delete_task_with_params(index, expected):
    """参数化测试：删除任务的各种索引"""
    tasks = [
        {"name": "任务1", "done": False},
        {"name": "任务2", "done": False},
        {"name": "任务3", "done": False}
    ]
    result = delete_task(tasks, index)

    assert result is expected


# 测试类型: 正例
# 覆盖场景: 多维度参数组合
# 预期结果: 笛卡尔积生成所有组合
@pytest.mark.parametrize("initial_count", [0, 1, 3])
@pytest.mark.parametrize("task_name", ["任务A", "任务B"])
def test_add_task_multiple_dimensions(initial_count, task_name):
    """多维度参数化测试"""
    tasks = [{"name": f"已有{i}", "done": False} for i in range(initial_count)]

    result = add_task(tasks, task_name)

    assert len(result) == initial_count + 1
    assert result[-1]["name"] == task_name


# 测试类型: 边界
# 覆盖场景: 标记为预期失败的测试
# 预期结果: 测试失败但不影响整体结果
@pytest.mark.xfail(reason="演示：已知问题，待修复")
def test_add_task_unicode_edge_case():
    """演示 xfail：已知问题的测试"""
    tasks = []
    # 假设这是一个已知会导致问题的输入
    add_task(tasks, "\x00")  # null 字符
    assert len(tasks) == 1


# =====================
# 5. 组合测试
# =====================

# 测试类型: 正例
# 覆盖场景: fixture 和参数化结合
def test_delete_task_with_fixture_and_params(sample_tasks):
    """结合 fixture 和参数"""
    initial_count = len(sample_tasks)

    result = delete_task(sample_tasks, 1)

    assert result is True
    assert len(sample_tasks) == initial_count - 1
