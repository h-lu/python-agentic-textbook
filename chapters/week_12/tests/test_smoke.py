"""冒烟测试（Smoke Tests）

这些是基础的冒烟测试，用于验证基本功能是否正常工作。
如果这些测试失败，说明实现存在严重问题。

注意：这些测试会在 starter_code/solution.py 实现后启用。
目前它们会跳过或标记为预期失败。
"""

import pytest
import sys
import os

# 添加 starter_code 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))

# 尝试导入 solution.py 中的函数
# 如果文件不存在或未实现，这些导入会失败
try:
    from solution import (
        create_parser,
        cmd_add,
        cmd_list,
        cmd_done,
        cmd_delete,
        cmd_stats,
        main
    )
    SOLUTION_AVAILABLE = True
except ImportError:
    SOLUTION_AVAILABLE = False


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestSmokeTests:
    """冒烟测试：验证基本功能存在"""

    def test_create_parser_returns_parser(self):
        """测试 create_parser 返回 ArgumentParser"""
        import argparse

        parser = create_parser()
        assert isinstance(parser, argparse.ArgumentParser)

    def test_parser_has_subcommands(self):
        """测试解析器有子命令"""
        parser = create_parser()

        # 尝试解析 add 命令
        args = parser.parse_args(["add", "测试任务"])
        assert args.command == "add"

    def test_cmd_add_function_exists(self):
        """测试 cmd_add 函数存在且可调用"""
        assert callable(cmd_add)

    def test_cmd_list_function_exists(self):
        """测试 cmd_list 函数存在且可调用"""
        assert callable(cmd_list)

    def test_cmd_done_function_exists(self):
        """测试 cmd_done 函数存在且可调用"""
        assert callable(cmd_done)

    def test_cmd_delete_function_exists(self):
        """测试 cmd_delete 函数存在且可调用"""
        assert callable(cmd_delete)

    def test_cmd_stats_function_exists(self):
        """测试 cmd_stats 函数存在且可调用"""
        assert callable(cmd_stats)

    def test_main_function_exists(self):
        """测试 main 函数存在且可调用"""
        assert callable(main)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestBasicFunctionality:
    """测试基本功能是否正常工作"""

    def test_help_shows_usage(self, capsys):
        """测试帮助信息显示用法"""
        import sys

        parser = create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--help"])

    def test_add_command_parsing(self):
        """测试 add 命令参数解析"""
        parser = create_parser()

        args = parser.parse_args(["add", "测试任务", "--priority", "high"])

        assert args.command == "add"
        assert args.title == "测试任务"
        assert args.priority == "high"

    def test_list_command_parsing(self):
        """测试 list 命令参数解析"""
        parser = create_parser()

        args = parser.parse_args(["list", "--all"])

        assert args.command == "list"
        assert args.all is True

    def test_done_command_parsing(self):
        """测试 done 命令参数解析"""
        parser = create_parser()

        args = parser.parse_args(["done", "1"])

        assert args.command == "done"
        assert args.id == 1

    def test_delete_command_parsing(self):
        """测试 delete 命令参数解析"""
        parser = create_parser()

        args = parser.parse_args(["delete", "1"])

        assert args.command == "delete"
        assert args.id == 1


class TestPythonEnvironment:
    """测试 Python 环境配置"""

    def test_python_version(self):
        """测试 Python 版本"""
        # 要求 Python 3.6+
        assert sys.version_info >= (3, 6)

    def test_argparse_available(self):
        """测试 argparse 模块可用"""
        import argparse
        assert argparse is not None

    def test_logging_available(self):
        """测试 logging 模块可用"""
        import logging
        assert logging is not None

    def test_subprocess_available(self):
        """测试 subprocess 模块可用"""
        import subprocess
        assert subprocess is not None

    def test_json_available(self):
        """测试 json 模块可用"""
        import json
        assert json is not None

    def test_pathlib_available(self):
        """测试 pathlib 模块可用"""
        from pathlib import Path
        assert Path is not None


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


class TestImportStructure:
    """测试导入结构"""

    def test_import_argparse(self):
        """测试可以导入 argparse"""
        import argparse
        parser = argparse.ArgumentParser()
        assert parser is not None

    def test_import_logging(self):
        """测试可以导入 logging"""
        import logging
        logger = logging.getLogger(__name__)
        assert logger is not None

    def test_import_sys(self):
        """测试可以导入 sys"""
        import sys
        assert hasattr(sys, 'exit')
        assert hasattr(sys, 'argv')


@pytest.mark.parametrize("module_name", [
    "argparse",
    "logging",
    "subprocess",
    "json",
    "pathlib",
    "sys",
    "tempfile",
    "os",
])
def test_required_modules_importable(module_name):
    """参数化测试：所有必需模块都可以导入"""
    __import__(module_name)


if __name__ == "__main__":
    # 可以直接运行此文件进行快速测试
    pytest.main([__file__, "-v"])
