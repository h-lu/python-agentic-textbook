"""
test_todo_manager.py - Todo Manager 完整测试

对贯穿案例 Todo Manager 的完整测试：
- 正例：正常添加任务、标记完成、删除任务
- 边界：空任务名、超长任务名、特殊字符
- 反例：删除不存在的任务、完成不存在的任务
"""

import pytest
import sys
from pathlib import Path

# 添加 starter_code 目录到路径（测试目标代码）
sys.path.insert(0, str(Path(__file__).parent.parent / "starter_code"))

from todo_manager import (
    add_task,
    list_tasks,
    mark_done,
    delete_task,
    get_task_count,
)


# =====================
# 1. 添加任务测试
# =====================

class TestAddTask:
    """测试 add_task 函数"""

    # 测试类型: 正例
    # 覆盖场景: 正常添加单个任务
    # 预期结果: 任务被正确添加到列表
    def test_add_single_task(self):
        """测试添加单个任务"""
        tasks = []
        result = add_task(tasks, "买牛奶")

        assert len(result) == 1
        assert result[0]["name"] == "买牛奶"
        assert result[0]["done"] is False

    # 测试类型: 正例
    # 覆盖场景: 连续添加多个任务
    # 预期结果: 所有任务按顺序添加
    def test_add_multiple_tasks(self):
        """测试添加多个任务"""
        tasks = []
        add_task(tasks, "任务一")
        add_task(tasks, "任务二")
        add_task(tasks, "任务三")

        assert len(tasks) == 3
        assert [t["name"] for t in tasks] == ["任务一", "任务二", "任务三"]

    # 测试类型: 正例
    # 覆盖场景: 任务名包含首尾空格
    # 预期结果: 空格被自动去除
    def test_add_task_strips_leading_trailing_spaces(self):
        """测试任务名去除首尾空格"""
        tasks = []
        add_task(tasks, "  买牛奶  ")

        assert tasks[0]["name"] == "买牛奶"

    # 测试类型: 正例
    # 覆盖场景: 任务名包含特殊字符
    # 预期结果: 特殊字符被保留
    @pytest.mark.parametrize("name", [
        "任务！",
        "任务？",
        "任务@#$%",
        "🎉 庆祝",
        "任务\t制表符",
    ])
    def test_add_task_special_characters(self, name):
        """测试各种特殊字符"""
        tasks = []
        add_task(tasks, name)

        # strip 后比较
        assert tasks[0]["name"] == name.strip()

    # 测试类型: 边界
    # 覆盖场景: 添加空字符串任务名
    # 预期结果: 空字符串被添加（不抛出异常）
    def test_add_task_empty_string(self):
        """测试添加空字符串任务名"""
        tasks = []
        result = add_task(tasks, "")

        assert len(result) == 1
        assert result[0]["name"] == ""

    # 测试类型: 边界
    # 覆盖场景: 添加只有空格的任务名
    # 预期结果: 空格被 strip 后变成空字符串
    def test_add_task_whitespace_only(self):
        """测试添加只有空格的任务名"""
        tasks = []
        result = add_task(tasks, "   ")

        assert len(result) == 1
        assert result[0]["name"] == ""

    # 测试类型: 正例
    # 覆盖场景: 添加超长任务名
    # 预期结果: 正常添加（不限制长度）
    def test_add_task_very_long_name(self):
        """测试添加超长任务名"""
        tasks = []
        long_name = "x" * 1000
        result = add_task(tasks, long_name)

        assert len(result) == 1
        assert result[0]["name"] == long_name


# =====================
# 2. 列出任务测试
# =====================

class TestListTasks:
    """测试 list_tasks 函数（打印输出）"""

    # 测试类型: 正例
    # 覆盖场景: 正常列出任务
    # 预期结果: 正确打印任务列表
    def test_list_tasks_normal(self, capsys):
        """测试正常列出任务"""
        tasks = [
            {"name": "买牛奶", "done": True},
            {"name": "写作业", "done": False},
        ]
        list_tasks(tasks)

        captured = capsys.readouterr()
        assert "1. [✓] 买牛奶" in captured.out
        assert "2. [ ] 写作业" in captured.out

    # 测试类型: 边界
    # 覆盖场景: 空任务列表
    # 预期结果: 打印"暂无任务"
    def test_list_tasks_empty(self, capsys):
        """测试空列表打印提示"""
        list_tasks([])

        captured = capsys.readouterr()
        assert "暂无任务" in captured.out

    # 测试类型: 正例
    # 覆盖场景: 所有任务都完成
    # 预期结果: 所有任务显示为完成状态
    def test_list_tasks_all_done(self, capsys):
        """测试所有任务完成"""
        tasks = [
            {"name": "任务1", "done": True},
            {"name": "任务2", "done": True},
        ]
        list_tasks(tasks)

        captured = capsys.readouterr()
        assert "[✓]" in captured.out
        assert "[ ]" not in captured.out

    # 测试类型: 正例
    # 覆盖场景: 所有任务都未完成
    # 预期结果: 所有任务显示为未完成状态
    def test_list_tasks_none_done(self, capsys):
        """测试所有任务未完成"""
        tasks = [
            {"name": "任务1", "done": False},
            {"name": "任务2", "done": False},
        ]
        list_tasks(tasks)

        captured = capsys.readouterr()
        assert "[ ]" in captured.out
        assert "[✓]" not in captured.out


# =====================
# 3. 标记完成测试
# =====================

class TestMarkDone:
    """测试 mark_done 函数"""

    # 测试类型: 正例
    # 覆盖场景: 正常标记任务完成
    # 预期结果: 返回 True，任务状态变为完成
    def test_mark_done_success(self):
        """测试成功标记完成"""
        tasks = [
            {"name": "买牛奶", "done": False},
            {"name": "写作业", "done": False},
        ]
        result = mark_done(tasks, 1)

        assert result is True
        assert tasks[0]["done"] is True
        assert tasks[1]["done"] is False  # 其他任务不受影响

    # 测试类型: 正例
    # 覆盖场景: 标记最后一个任务
    # 预期结果: 返回 True，任务状态变为完成
    def test_mark_done_last_task(self):
        """测试标记最后一个任务"""
        tasks = [
            {"name": "任务1", "done": False},
            {"name": "任务2", "done": False},
        ]
        result = mark_done(tasks, 2)

        assert result is True
        assert tasks[1]["done"] is True

    # 测试类型: 反例
    # 覆盖场景: 索引为 0（无效）
    # 预期结果: 返回 False，任务状态不变
    def test_mark_done_index_zero(self):
        """测试索引为 0 返回 False"""
        tasks = [{"name": "任务", "done": False}]
        result = mark_done(tasks, 0)

        assert result is False
        assert tasks[0]["done"] is False

    # 测试类型: 反例
    # 覆盖场景: 索引为负数
    # 预期结果: 返回 False，任务状态不变
    def test_mark_done_negative_index(self):
        """测试负数索引返回 False"""
        tasks = [{"name": "任务", "done": False}]
        result = mark_done(tasks, -1)

        assert result is False
        assert tasks[0]["done"] is False

    # 测试类型: 反例
    # 覆盖场景: 索引超出范围
    # 预期结果: 返回 False，任务状态不变
    def test_mark_done_index_out_of_range(self):
        """测试索引超出范围返回 False"""
        tasks = [{"name": "任务", "done": False}]
        result = mark_done(tasks, 99)

        assert result is False
        assert tasks[0]["done"] is False

    # 测试类型: 反例
    # 覆盖场景: 空列表
    # 预期结果: 返回 False
    def test_mark_done_empty_list(self):
        """测试空列表返回 False"""
        result = mark_done([], 1)

        assert result is False

    # 测试类型: 边界
    # 覆盖场景: 重复标记已完成的任务
    # 预期结果: 返回 True，状态保持完成
    def test_mark_done_already_done(self):
        """测试重复标记已完成的任务"""
        tasks = [{"name": "任务", "done": True}]
        result = mark_done(tasks, 1)

        assert result is True
        assert tasks[0]["done"] is True


# =====================
# 4. 删除任务测试
# =====================

class TestDeleteTask:
    """测试 delete_task 函数"""

    # 测试类型: 正例
    # 覆盖场景: 正常删除第一个任务
    # 预期结果: 返回 True，任务被删除
    def test_delete_first_task(self):
        """测试删除第一个任务"""
        tasks = [
            {"name": "任务1", "done": False},
            {"name": "任务2", "done": False},
        ]
        result = delete_task(tasks, 1)

        assert result is True
        assert len(tasks) == 1
        assert tasks[0]["name"] == "任务2"

    # 测试类型: 正例
    # 覆盖场景: 正常删除最后一个任务
    # 预期结果: 返回 True，任务被删除
    def test_delete_last_task(self):
        """测试删除最后一个任务"""
        tasks = [
            {"name": "任务1", "done": False},
            {"name": "任务2", "done": False},
        ]
        result = delete_task(tasks, 2)

        assert result is True
        assert len(tasks) == 1
        assert tasks[0]["name"] == "任务1"

    # 测试类型: 正例
    # 覆盖场景: 删除中间的任务
    # 预期结果: 返回 True，任务被删除，其他任务保留
    def test_delete_middle_task(self):
        """测试删除中间的任务"""
        tasks = [
            {"name": "任务1", "done": False},
            {"name": "任务2", "done": False},
            {"name": "任务3", "done": False},
        ]
        result = delete_task(tasks, 2)

        assert result is True
        assert len(tasks) == 2
        assert tasks[0]["name"] == "任务1"
        assert tasks[1]["name"] == "任务3"

    # 测试类型: 正例
    # 覆盖场景: 删除唯一任务
    # 预期结果: 返回 True，列表变空
    def test_delete_only_task(self):
        """测试删除唯一任务"""
        tasks = [{"name": "任务", "done": False}]
        result = delete_task(tasks, 1)

        assert result is True
        assert len(tasks) == 0

    # 测试类型: 反例
    # 覆盖场景: 索引为 0（无效）
    # 预期结果: 返回 False，列表不变
    def test_delete_index_zero(self):
        """测试索引为 0 返回 False"""
        tasks = [{"name": "任务", "done": False}]
        result = delete_task(tasks, 0)

        assert result is False
        assert len(tasks) == 1

    # 测试类型: 反例
    # 覆盖场景: 索引为负数
    # 预期结果: 返回 False，列表不变
    def test_delete_negative_index(self):
        """测试负数索引返回 False"""
        tasks = [{"name": "任务", "done": False}]
        result = delete_task(tasks, -1)

        assert result is False
        assert len(tasks) == 1

    # 测试类型: 反例
    # 覆盖场景: 索引超出范围
    # 预期结果: 返回 False，列表不变
    def test_delete_index_out_of_range(self):
        """测试索引超出范围返回 False"""
        tasks = [{"name": "任务", "done": False}]
        result = delete_task(tasks, 99)

        assert result is False
        assert len(tasks) == 1

    # 测试类型: 反例
    # 覆盖场景: 空列表
    # 预期结果: 返回 False
    def test_delete_empty_list(self):
        """测试空列表返回 False"""
        result = delete_task([], 1)

        assert result is False


# =====================
# 5. 统计功能测试
# =====================

class TestGetTaskCount:
    """测试 get_task_count 函数"""

    # 测试类型: 正例
    # 覆盖场景: 正常统计
    # 预期结果: 返回正确的总数和完成数
    def test_count_normal(self):
        """测试正常统计"""
        tasks = [
            {"name": "任务1", "done": True},
            {"name": "任务2", "done": False},
            {"name": "任务3", "done": True},
        ]
        result = get_task_count(tasks)

        assert result["total"] == 3
        assert result["completed"] == 2

    # 测试类型: 边界
    # 覆盖场景: 空列表
    # 预期结果: 总数和完成数都为 0
    def test_count_empty(self):
        """测试空列表统计"""
        result = get_task_count([])

        assert result["total"] == 0
        assert result["completed"] == 0

    # 测试类型: 正例
    # 覆盖场景: 所有任务完成
    # 预期结果: completed 等于 total
    def test_count_all_done(self):
        """测试所有任务完成"""
        tasks = [
            {"name": "任务1", "done": True},
            {"name": "任务2", "done": True},
        ]
        result = get_task_count(tasks)

        assert result["total"] == 2
        assert result["completed"] == 2

    # 测试类型: 正例
    # 覆盖场景: 所有任务未完成
    # 预期结果: completed 为 0
    def test_count_none_done(self):
        """测试所有任务未完成"""
        tasks = [
            {"name": "任务1", "done": False},
            {"name": "任务2", "done": False},
        ]
        result = get_task_count(tasks)

        assert result["total"] == 2
        assert result["completed"] == 0

    # 测试类型: 正例
    # 覆盖场景: 单个任务
    # 预期结果: 正确统计
    def test_count_single_task(self):
        """测试单个任务"""
        tasks = [{"name": "任务", "done": True}]
        result = get_task_count(tasks)

        assert result["total"] == 1
        assert result["completed"] == 1


# =====================
# 6. 集成测试
# =====================

class TestIntegration:
    """集成测试：多个功能的组合使用"""

    # 测试类型: 正例
    # 覆盖场景: 完整的工作流程
    # 预期结果: 所有操作按预期工作
    def test_complete_workflow(self, capsys):
        """测试完整工作流程"""
        tasks = []

        # 添加任务
        add_task(tasks, "买牛奶")
        add_task(tasks, "写作业")
        add_task(tasks, "运动")
        assert len(tasks) == 3

        # 标记完成
        mark_done(tasks, 1)
        assert tasks[0]["done"] is True

        # 列出任务
        list_tasks(tasks)
        captured = capsys.readouterr()
        assert "[✓] 买牛奶" in captured.out

        # 删除任务
        delete_task(tasks, 2)
        assert len(tasks) == 2

        # 统计
        stats = get_task_count(tasks)
        assert stats["total"] == 2
        assert stats["completed"] == 1

    # 测试类型: 正例
    # 覆盖场景: 添加后立即删除
    # 预期结果: 列表恢复为空
    def test_add_and_immediately_delete(self):
        """测试添加后立即删除"""
        tasks = []

        add_task(tasks, "临时任务")
        assert len(tasks) == 1

        delete_task(tasks, 1)
        assert len(tasks) == 0

    # 测试类型: 边界
    # 覆盖场景: 删除后重新添加
    # 预期结果: 新任务正常添加
    def test_delete_then_add(self):
        """测试删除后重新添加"""
        tasks = [{"name": "旧任务", "done": False}]

        delete_task(tasks, 1)
        assert len(tasks) == 0

        add_task(tasks, "新任务")
        assert len(tasks) == 1
        assert tasks[0]["name"] == "新任务"
