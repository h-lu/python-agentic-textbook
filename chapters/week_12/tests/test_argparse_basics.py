"""测试 argparse 基础功能

这些测试验证学生对 argparse 基础概念的理解：
- 位置参数（positional arguments）
- 可选参数（optional arguments）
- 短选项和长选项
- 参数类型转换
- 参数验证（choices、required）
- 帮助信息生成
"""

import pytest
import argparse
import sys
import os

# 添加 starter_code 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))

# 注意：这些测试假设 starter_code/solution.py 中提供了相应的函数
# 如果 solution.py 还未创建，测试会标记为 xfail


class TestPositionalArguments:
    """测试位置参数解析"""

    def test_parse_single_positional_arg(self):
        """测试解析单个位置参数"""
        # 创建解析器
        parser = argparse.ArgumentParser()
        parser.add_argument("title", help="任务标题")

        # 测试正常输入
        args = parser.parse_args(["写作业"])
        assert args.title == "写作业"

    def test_positional_arg_required(self):
        """测试位置参数是必需的"""
        parser = argparse.ArgumentParser()
        parser.add_argument("title", help="任务标题")

        # 测试缺少必需参数
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_multiple_positional_args(self):
        """测试多个位置参数按顺序解析"""
        parser = argparse.ArgumentParser()
        parser.add_argument("title", help="任务标题")
        parser.add_argument("priority", help="优先级")

        args = parser.parse_args(["写作业", "high"])
        assert args.title == "写作业"
        assert args.priority == "high"

    def test_positional_arg_with_quotes(self):
        """测试带引号的位置参数（包含空格）"""
        parser = argparse.ArgumentParser()
        parser.add_argument("title", help="任务标题")

        args = parser.parse_args(["完成 Week 12 作业"])
        assert args.title == "完成 Week 12 作业"


class TestOptionalArguments:
    """测试可选参数解析"""

    def test_optional_arg_with_default(self):
        """测试可选参数的默认值"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--priority", default="medium")

        args = parser.parse_args([])
        assert args.priority == "medium"

    def test_optional_arg_override_default(self):
        """测试覆盖默认值"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--priority", default="medium")

        args = parser.parse_args(["--priority", "high"])
        assert args.priority == "high"

    def test_short_option(self):
        """测试短选项（单横线）"""
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--priority", default="medium")

        args = parser.parse_args(["-p", "high"])
        assert args.priority == "high"

    def test_long_option(self):
        """测试长选项（双横线）"""
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--priority", default="medium")

        args = parser.parse_args(["--priority", "high"])
        assert args.priority == "high"

    def test_short_and_long_equivalent(self):
        """测试短选项和长选项等价"""
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--priority", default="medium")

        args1 = parser.parse_args(["-p", "high"])
        args2 = parser.parse_args(["--priority", "high"])

        assert args1.priority == args2.priority == "high"


class TestArgumentTypes:
    """测试参数类型转换"""

    def test_type_int(self):
        """测试整数类型参数"""
        parser = argparse.ArgumentParser()
        parser.add_argument("id", type=int)

        args = parser.parse_args(["42"])
        assert args.id == 42
        assert isinstance(args.id, int)

    def test_type_int_invalid_value(self):
        """测试无效的整数类型值"""
        parser = argparse.ArgumentParser()
        parser.add_argument("id", type=int)

        with pytest.raises(SystemExit):
            parser.parse_args(["abc"])

    def test_type_float(self):
        """测试浮点数类型参数"""
        parser = argparse.ArgumentParser()
        parser.add_argument("rate", type=float)

        args = parser.parse_args(["3.14"])
        assert args.rate == 3.14
        assert isinstance(args.rate, float)

    def test_multiple_type_args(self):
        """测试多个不同类型的参数"""
        parser = argparse.ArgumentParser()
        parser.add_argument("id", type=int)
        parser.add_argument("title", type=str)
        parser.add_argument("--rate", type=float, default=1.0)

        args = parser.parse_args(["1", "测试", "--rate", "2.5"])
        assert args.id == 1
        assert args.title == "测试"
        assert args.rate == 2.5


class TestArgumentValidation:
    """测试参数验证"""

    def test_choices_validation(self):
        """测试 choices 限制参数值"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--priority",
                          choices=["low", "medium", "high"],
                          default="medium")

        # 有效的选择
        args = parser.parse_args(["--priority", "high"])
        assert args.priority == "high"

        # 无效的选择
        with pytest.raises(SystemExit):
            parser.parse_args(["--priority", "ultra"])

    def test_required_optional_arg(self):
        """测试必需的可选参数（required=True）"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--title", required=True)

        # 缺少必需参数
        with pytest.raises(SystemExit):
            parser.parse_args([])

        # 提供必需参数
        args = parser.parse_args(["--title", "测试"])
        assert args.title == "测试"

    def test_action_store_true(self):
        """测试 store_true action"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--verbose", action="store_true")

        # 不提供参数时为 False
        args = parser.parse_args([])
        assert args.verbose is False

        # 提供参数时为 True
        args = parser.parse_args(["--verbose"])
        assert args.verbose is True

    def test_action_store_false(self):
        """测试 store_false action"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--quiet", action="store_false", default=True)

        # 不提供参数时为默认值 True
        args = parser.parse_args([])
        assert args.quiet is True

        # 提供参数时为 False
        args = parser.parse_args(["--quiet"])
        assert args.quiet is False

    def test_nargs_variable(self):
        """测试可变数量参数（nargs='*'）"""
        parser = argparse.ArgumentParser()
        parser.add_argument("tags", nargs="*")

        # 零个参数
        args = parser.parse_args([])
        assert args.tags == []

        # 多个参数
        args = parser.parse_args(["python", "django", "pytest"])
        assert args.tags == ["python", "django", "pytest"]

    def test_nargs_fixed(self):
        """测试固定数量参数（nargs=2）"""
        parser = argparse.ArgumentParser()
        parser.add_argument("coords", nargs=2, type=float)

        args = parser.parse_args(["1.5", "2.5"])
        assert args.coords == [1.5, 2.5]

        # 参数数量不对
        with pytest.raises(SystemExit):
            parser.parse_args(["1.5"])


class TestMutuallyExclusiveGroups:
    """测试互斥参数组"""

    def test_mutually_exclusive_success(self):
        """测试互斥组：只提供一个参数"""
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--all", action="store_true")
        group.add_argument("--pending", action="store_true")

        args = parser.parse_args(["--all"])
        assert args.all is True
        assert args.pending is False

    def test_mutually_exclusive_conflict(self):
        """测试互斥组：同时提供两个参数应失败"""
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--all", action="store_true")
        group.add_argument("--pending", action="store_true")

        # 同时提供两个互斥参数
        with pytest.raises(SystemExit):
            parser.parse_args(["--all", "--pending"])

    def test_mutually_exclusive_none(self):
        """测试互斥组：不提供任何参数"""
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--all", action="store_true")
        group.add_argument("--pending", action="store_true")

        args = parser.parse_args([])
        assert args.all is False
        assert args.pending is False


class TestHelpGeneration:
    """测试帮助信息生成"""

    def test_help_argument(self, capsys):
        """测试 -h/--help 自动生成帮助"""
        parser = argparse.ArgumentParser(description="任务管理工具")
        parser.add_argument("title", help="任务标题")
        parser.add_argument("--priority", help="任务优先级")

        # 测试 --help
        with pytest.raises(SystemExit):
            parser.parse_args(["--help"])

        captured = capsys.readouterr()
        assert "任务管理工具" in captured.out
        assert "任务标题" in captured.out
        assert "任务优先级" in captured.out

    def test_usage_on_error(self, capsys):
        """测试错误时显示用法信息"""
        parser = argparse.ArgumentParser()
        parser.add_argument("title")

        # 缺少必需参数
        with pytest.raises(SystemExit):
            parser.parse_args([])

        captured = capsys.readouterr()
        # argparse 错误信息输出到 stderr
        assert "usage" in captured.err.lower() or "error" in captured.err.lower()


class TestEdgeCases:
    """测试边界情况"""

    def test_empty_string_value(self):
        """测试空字符串作为参数值"""
        parser = argparse.ArgumentParser()
        parser.add_argument("title")

        args = parser.parse_args([""])
        assert args.title == ""

    def test_unicode_characters(self):
        """测试 Unicode 字符"""
        parser = argparse.ArgumentParser()
        parser.add_argument("title")

        args = parser.parse_args(["学习中文 🎉"])
        assert args.title == "学习中文 🎉"

    def test_very_long_argument(self):
        """测试超长参数"""
        parser = argparse.ArgumentParser()
        parser.add_argument("title")

        long_text = "A" * 10000
        args = parser.parse_args([long_text])
        assert args.title == long_text

    def test_special_characters(self):
        """测试特殊字符"""
        parser = argparse.ArgumentParser()
        parser.add_argument("title")

        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        args = parser.parse_args([special_chars])
        assert args.title == special_chars


@pytest.mark.parametrize("input_value,expected", [
    ("42", 42),
    ("0", 0),
    ("-1", -1),
    ("1000000", 1000000),
])
def test_int_type_conversion_parametrized(input_value, expected):
    """参数化测试：整数类型转换"""
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int)

    args = parser.parse_args([input_value])
    assert args.number == expected


@pytest.mark.parametrize("input_value,should_fail", [
    ("low", False),
    ("medium", False),
    ("high", False),
    ("ultra", True),
    ("critical", True),
    ("", True),
])
def test_choices_validation_parametrized(input_value, should_fail):
    """参数化测试：choices 验证"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--priority", choices=["low", "medium", "high"])

    if should_fail:
        with pytest.raises(SystemExit):
            parser.parse_args(["--priority", input_value])
    else:
        args = parser.parse_args(["--priority", input_value])
        assert args.priority == input_value
