"""冒烟测试（Smoke Tests）

基础的冒烟测试，验证基本功能是否正常工作。
如果这些测试失败，说明实现存在严重问题。
"""

import pytest
import sys
import os

# 添加 starter_code 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))

# 尝试导入 solution.py 中的内容
try:
    from solution import (
        NoteInfo,
        StudyPlan,
        ReviewResult,
        ReaderAgent,
        WriterAgent,
        ReviewerAgent,
        iterative_plan_generation
    )
    SOLUTION_AVAILABLE = True
except ImportError:
    SOLUTION_AVAILABLE = False


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestDataClasses:
    """测试 dataclass 定义"""

    def test_note_info_creation(self):
        """测试 NoteInfo dataclass 可以创建"""
        note_info = NoteInfo(
            title="异常处理",
            topics=["异常处理", "函数"],
            difficulty="medium"
        )
        assert note_info.title == "异常处理"
        assert note_info.topics == ["异常处理", "函数"]
        assert note_info.difficulty == "medium"

    def test_study_plan_creation(self):
        """测试 StudyPlan dataclass 可以创建"""
        plan = StudyPlan(
            week=6,
            title="异常处理",
            prerequisites=["函数", "文件"],
            priority="high",
            topics=["异常处理"],
            estimated_hours=7
        )
        assert plan.week == 6
        assert plan.title == "异常处理"
        assert plan.prerequisites == ["函数", "文件"]
        assert plan.priority == "high"
        assert plan.topics == ["异常处理"]
        assert plan.estimated_hours == 7

    def test_review_result_creation(self):
        """测试 ReviewResult dataclass 可以创建"""
        result = ReviewResult(
            passed=True,
            issues=[]
        )
        assert result.passed is True
        assert result.issues == []


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestAgentClasses:
    """测试 Agent 类存在且可实例化"""

    def test_reader_agent_instantiable(self):
        """测试 ReaderAgent 可以实例化"""
        agent = ReaderAgent()
        assert agent is not None
        assert hasattr(agent, 'read_note')

    def test_writer_agent_instantiable(self):
        """测试 WriterAgent 可以实例化"""
        agent = WriterAgent()
        assert agent is not None
        assert hasattr(agent, 'create_plan')

    def test_reviewer_agent_instantiable(self):
        """测试 ReviewerAgent 可以实例化"""
        agent = ReviewerAgent()
        assert agent is not None
        assert hasattr(agent, 'review_plan')


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestModuleFunctions:
    """测试模块函数存在且可调用"""

    def test_iterative_plan_generation_exists(self):
        """测试 iterative_plan_generation 函数存在"""
        assert callable(iterative_plan_generation)


class TestPythonEnvironment:
    """测试 Python 环境配置"""

    def test_python_version(self):
        """测试 Python 版本（要求 3.6+）"""
        assert sys.version_info >= (3, 6)

    def test_dataclass_available(self):
        """测试 dataclass 模块可用"""
        from dataclasses import dataclass
        assert dataclass is not None

    def test_pathlib_available(self):
        """测试 pathlib 模块可用"""
        from pathlib import Path
        assert Path is not None

    def test_logging_available(self):
        """测试 logging 模块可用"""
        import logging
        assert logging is not None


class TestDirectoryStructure:
    """测试目录结构是否正确"""

    def test_tests_directory_exists(self):
        """测试 tests 目录存在"""
        tests_dir = os.path.dirname(__file__)
        assert os.path.exists(tests_dir)
        assert os.path.isdir(tests_dir)

    def test_starter_code_directory_exists(self):
        """测试 starter_code 目录存在"""
        starter_dir = os.path.join(os.path.dirname(__file__), '..', 'starter_code')
        assert os.path.exists(starter_dir)
        assert os.path.isdir(starter_dir)

    def test_examples_directory_exists(self):
        """测试 examples 目录存在"""
        examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
        assert os.path.exists(examples_dir)
        assert os.path.isdir(examples_dir)


@pytest.mark.parametrize("module_name", [
    "dataclasses",
    "logging",
    "pathlib",
    "typing",
    "re",
])
def test_required_modules_importable(module_name):
    """参数化测试：所有必需模块都可以导入"""
    __import__(module_name)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
