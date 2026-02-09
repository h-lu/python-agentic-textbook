"""
示例：TDD（测试驱动开发）完整演示

本例演示完整的 TDD 循环：
1. 红：写测试，运行，看到失败
2. 绿：写最少代码让测试通过
3. 重构：改进代码，保持测试通过

运行方式：
  cd chapters/week_08/examples/05_todo_tdd
  pytest test_todo.py -v

  运行单个测试：
  pytest test_todo.py::test_delete_task_success -v

预期输出：
  所有测试通过，展示 TDD 的完整流程
"""

import pytest
from todo import add_task, mark_done, delete_task, delete_task_refactored


# ========== 已有功能的测试（假设之前已写好） ==========

def test_add_task():
    """已有功能：添加任务"""
    tasks = []
    result = add_task(tasks, "买牛奶")

    assert len(result) == 1
    assert result[0]["name"] == "买牛奶"


def test_mark_done():
    """已有功能：标记完成"""
    tasks = [{"name": "买牛奶", "done": False}]
    result = mark_done(tasks, 1)

    assert result == True
    assert tasks[0]["done"] == True


# ========== TDD 第一步：红（写测试，看到失败） ==========

def test_delete_task_success():
    """
    TDD 第一步：写测试

    在 delete_task 实现之前，先写测试定义它的行为：
    - 输入：任务列表和要删除的索引（1-based）
    - 正常情况：删除成功，返回 True
    - 副作用：任务列表减少一个元素
    """
    tasks = [
        {"name": "买牛奶", "done": False},
        {"name": "写作业", "done": False}
    ]

    result = delete_task(tasks, 1)  # 删除第一个任务

    assert result == True
    assert len(tasks) == 1
    assert tasks[0]["name"] == "写作业"  # 剩下的应该是第二个任务


# 第一次运行 pytest 时：
# ImportError: cannot import name 'delete_task' from 'todo'
# 这是"红"阶段 - 测试因为实现缺失而失败


# ========== TDD 第二步：绿（写最少代码让测试通过） ==========

# 在 todo.py 中添加：
# def delete_task(tasks, index):
#     if 1 <= index <= len(tasks):
#         tasks.pop(index - 1)
#         return True
#     return False

# 再次运行 pytest：
# test_delete_task_success PASSED
# 这是"绿"阶段 - 测试通过了


# ========== 添加更多测试覆盖边界情况 ==========

@pytest.mark.parametrize("invalid_index", [0, -1, 99])
def test_delete_task_invalid_index(invalid_index):
    """
    测试删除非法索引返回 False

    边界情况：
    - 0：不是合法的 1-based 索引
    - -1：负数索引
    - 99：超出列表长度
    """
    tasks = [{"name": "买牛奶", "done": False}]

    result = delete_task(tasks, invalid_index)

    assert result == False
    assert len(tasks) == 1  # 任务列表应该保持不变


# ========== TDD 第三步：重构（保持测试通过） ==========

def test_delete_task_refactored():
    """
    测试重构后的版本

    重构内容：
    - 提取 list_index 变量
    - 使用 0-based 索引进行边界检查

    重要：重构后必须运行所有测试，确保行为没变
    """
    tasks = [
        {"name": "买牛奶", "done": False},
        {"name": "写作业", "done": False}
    ]

    # 测试正常删除
    result = delete_task_refactored(tasks, 1)
    assert result == True
    assert len(tasks) == 1
    assert tasks[0]["name"] == "写作业"

    # 测试非法索引
    result = delete_task_refactored(tasks, 99)
    assert result == False
    assert len(tasks) == 1  # 未改变


# 运行所有测试，确保重构没有破坏功能
# pytest test_todo.py -v
# 所有测试都应该通过


# ========== 反例：没有测试保护的重构 ==========

def delete_task_broken(tasks, index):
    """
    反例：重构时引入 bug

    这个版本"忘记"了边界检查，直接 pop
    """
    tasks.pop(index - 1)  # 没有检查索引！
    return True


def test_delete_task_broken():
    """
    反例：如果没有测试，这个 bug 可能不会被发现

    这个测试展示了如果没有边界检查会发生什么
    """
    tasks = [{"name": "买牛奶", "done": False}]

    # 正常情况下工作
    result = delete_task_broken(tasks, 1)
    assert result == True
    assert len(tasks) == 0

    # 但如果传入非法索引：
    tasks = [{"name": "买牛奶", "done": False}]

    try:
        delete_task_broken(tasks, 99)  # 会抛出 IndexError
        assert False, "应该抛出异常"
    except IndexError:
        pass  # 预期中的异常

    # 这就是为什么要写测试 - 防止这种边界情况出错


# ========== TDD 总结 ==========

"""
TDD 的核心价值：

1. 测试先行
   - 在写实现之前，先想清楚函数应该做什么
   - 测试就是函数的"契约"或"规格说明"

2. 快速反馈
   - 红-绿循环提供即时反馈
   - 知道什么时候"做完了"

3. 重构信心
   - 有测试保护，才敢改进代码结构
   - 重构后运行测试，立即知道有没有破坏功能

4. 活文档
   - 测试比注释更准确地描述代码行为
   - 测试是可执行的文档

TDD 不是银弹，但在以下场景特别有用：
- 核心算法/业务逻辑
- 边界情况复杂的函数
- 需要频繁重构的代码
- 多人协作的模块
"""
