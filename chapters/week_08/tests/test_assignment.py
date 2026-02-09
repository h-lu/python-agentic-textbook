"""Week 08 作业测试

这些测试用于验证学生是否正确完成了作业要求。
"""

import pytest
import sys
import os

# 添加 starter_code 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))

from todo_manager import add_task, mark_done, delete_task, list_tasks


class TestBasicRequirements:
    """测试基础作业要求"""

    def test_add_task_returns_list(self):
        """测试 add_task 返回列表"""
        tasks = []
        result = add_task(tasks, "测试任务")
        assert isinstance(result, list)
        assert len(result) == 1

    def test_add_task_creates_correct_structure(self):
        """测试 add_task 创建正确的任务结构"""
        tasks = []
        result = add_task(tasks, "买牛奶")

        assert "name" in result[0]
        assert "done" in result[0]
        assert result[0]["name"] == "买牛奶"
        assert result[0]["done"] == False

    def test_add_task_strips_whitespace(self):
        """测试 add_task 去除首尾空格"""
        tasks = []
        result = add_task(tasks, "  买牛奶  ")
        assert result[0]["name"] == "买牛奶"

    def test_mark_done_success(self):
        """测试 mark_done 成功标记"""
        tasks = [{"name": "买牛奶", "done": False}]
        result = mark_done(tasks, 1)

        assert result == True
        assert tasks[0]["done"] == True

    def test_mark_done_invalid_index_returns_false(self):
        """测试 mark_done 无效索引返回 False"""
        tasks = [{"name": "买牛奶", "done": False}]
        result = mark_done(tasks, 99)

        assert result == False
        assert tasks[0]["done"] == False  # 状态不应改变

    def test_mark_done_zero_index(self):
        """测试 mark_done 索引 0 返回 False"""
        tasks = [{"name": "买牛奶", "done": False}]
        result = mark_done(tasks, 0)
        assert result == False

    def test_delete_task_success(self):
        """测试 delete_task 成功删除"""
        tasks = [
            {"name": "买牛奶", "done": False},
            {"name": "写作业", "done": False}
        ]
        result = delete_task(tasks, 1)

        assert result == True
        assert len(tasks) == 1
        assert tasks[0]["name"] == "写作业"

    def test_delete_task_invalid_index(self):
        """测试 delete_task 无效索引返回 False"""
        tasks = [{"name": "买牛奶", "done": False}]
        result = delete_task(tasks, 99)

        assert result == False
        assert len(tasks) == 1  # 列表不应改变

    def test_delete_task_empty_list(self):
        """测试 delete_task 空列表返回 False"""
        tasks = []
        result = delete_task(tasks, 1)
        assert result == False


class TestEdgeCases:
    """测试边界情况"""

    def test_add_task_empty_string(self):
        """测试添加空字符串任务"""
        tasks = []
        result = add_task(tasks, "")
        assert len(result) == 1
        assert result[0]["name"] == ""

    def test_add_task_emoji(self):
        """测试添加带 emoji 的任务"""
        tasks = []
        result = add_task(tasks, "🥛 买牛奶")
        assert result[0]["name"] == "🥛 买牛奶"

    def test_mark_done_negative_index(self):
        """测试 mark_done 负数索引"""
        tasks = [{"name": "买牛奶", "done": False}]
        result = mark_done(tasks, -1)
        assert result == False

    def test_multiple_tasks_operations(self):
        """测试多个任务的连续操作"""
        tasks = []

        # 添加三个任务
        add_task(tasks, "任务1")
        add_task(tasks, "任务2")
        add_task(tasks, "任务3")
        assert len(tasks) == 3

        # 标记第二个完成
        mark_done(tasks, 2)
        assert tasks[1]["done"] == True

        # 删除第一个
        delete_task(tasks, 1)
        assert len(tasks) == 2
        assert tasks[0]["name"] == "任务2"
        assert tasks[0]["done"] == True  # 状态应保持


class TestListTasks:
    """测试 list_tasks 函数（打印输出）"""

    def test_list_tasks_empty(self, capsys):
        """测试列出空任务列表"""
        list_tasks([])
        captured = capsys.readouterr()
        assert "暂无任务" in captured.out

    def test_list_tasks_output(self, capsys):
        """测试列出任务时的输出"""
        tasks = [
            {"name": "买牛奶", "done": True},
            {"name": "写作业", "done": False}
        ]
        list_tasks(tasks)
        captured = capsys.readouterr()

        assert "1. [✓] 买牛奶" in captured.out
        assert "2. [ ] 写作业" in captured.out
