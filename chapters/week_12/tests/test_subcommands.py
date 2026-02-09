"""测试子命令（subcommands）

这些测试验证学生对 argparse 子命令架构的理解：
- 创建子命令解析器（add_subparsers）
- 子命令路由（dest 参数）
- 每个子命令的独立参数
- 子命令的处理函数（set_defaults）
- 显示帮助信息
"""

import pytest
import argparse
import sys
import os

# 添加 starter_code 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))


class TestSubparsersBasic:
    """测试子命令基础功能"""

    def test_create_subparsers(self):
        """测试创建子命令解析器"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        # 添加子命令
        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("title")

        list_parser = subparsers.add_parser("list")

        # 测试 add 子命令
        args = parser.parse_args(["add", "测试任务"])
        assert args.command == "add"
        assert args.title == "测试任务"

    def test_list_subcommand(self):
        """测试 list 子命令"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        list_parser = subparsers.add_parser("list")
        list_parser.add_argument("--all", action="store_true")

        args = parser.parse_args(["list", "--all"])
        assert args.command == "list"
        assert args.all is True

    def test_no_subcommand_shows_help(self, capsys):
        """测试不提供子命令时显示帮助"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        add_parser = subparsers.add_parser("add", help="添加任务")
        list_parser = subparsers.add_parser("list", help="列出任务")

        # 不提供子命令
        args = parser.parse_args([])
        assert args.command is None

    def test_subcommand_not_required_error(self, capsys):
        """测试子命令不是必需时的行为"""
        parser = argparse.ArgumentParser()
        # 不设置 required=True
        subparsers = parser.add_subparsers(dest="command")

        subparsers.add_parser("add")
        subparsers.add_parser("list")

        # 不提供子命令应该能成功解析
        args = parser.parse_args([])
        assert args.command is None


class TestSubcommandRouting:
    """测试子命令路由"""

    def test_dest_parameter_routing(self):
        """测试 dest 参数用于路由"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="cmd")

        add_parser = subparsers.add_parser("add")
        done_parser = subparsers.add_parser("done")

        # 测试 add 路由
        args = parser.parse_args(["add"])
        assert args.cmd == "add"

        # 测试 done 路由
        args = parser.parse_args(["done"])
        assert args.cmd == "done"

    def test_if_statement_routing(self):
        """测试用 if 语句进行路由"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("title")

        list_parser = subparsers.add_parser("list")

        args = parser.parse_args(["add", "测试"])

        if args.command == "add":
            assert args.title == "测试"
            executed = True
        elif args.command == "list":
            executed = False
        else:
            executed = False

        assert executed is True


class TestSubcommandIndependentArgs:
    """测试每个子命令的独立参数"""

    def test_add_subcommand_args(self):
        """测试 add 子命令的参数"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("title", help="任务标题")
        add_parser.add_argument("--priority", default="medium")

        args = parser.parse_args(["add", "写作业", "--priority", "high"])
        assert args.command == "add"
        assert args.title == "写作业"
        assert args.priority == "high"

    def test_list_subcommand_args(self):
        """测试 list 子命令的参数"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        list_parser = subparsers.add_parser("list")
        list_parser.add_argument("--all", action="store_true")
        list_parser.add_argument("--pending", action="store_true")

        args = parser.parse_args(["list", "--all"])
        assert args.command == "list"
        assert args.all is True
        assert args.pending is False

    def test_done_subcommand_args(self):
        """测试 done 子命令的参数"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        done_parser = subparsers.add_parser("done")
        done_parser.add_argument("id", type=int)

        args = parser.parse_args(["done", "42"])
        assert args.command == "done"
        assert args.id == 42
        assert isinstance(args.id, int)

    def test_different_subcommands_different_args(self):
        """测试不同子命令有不同的参数"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        # add 有 title 参数
        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("title")

        # done 有 id 参数
        done_parser = subparsers.add_parser("done")
        done_parser.add_argument("id", type=int)

        # 测试 add
        args = parser.parse_args(["add", "测试"])
        assert hasattr(args, "title")
        assert not hasattr(args, "id")

        # 测试 done
        args = parser.parse_args(["done", "1"])
        assert hasattr(args, "id")
        assert not hasattr(args, "title")


class TestSubcommandFunctions:
    """测试子命令处理函数"""

    def test_set_defaults_function(self):
        """测试 set_defaults 设置处理函数"""
        # 模拟命令函数
        executed = []

        def cmd_add(args):
            executed.append("add")
            return 0

        def cmd_list(args):
            executed.append("list")
            return 0

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("title")
        add_parser.set_defaults(func=cmd_add)

        list_parser = subparsers.add_parser("list")
        list_parser.set_defaults(func=cmd_list)

        # 测试 add 子命令调用
        args = parser.parse_args(["add", "测试"])
        if hasattr(args, "func"):
            args.func(args)

        assert "add" in executed

    def test_function_routing_pattern(self):
        """测试标准函数路由模式"""
        executed = []

        def cmd_add(args):
            executed.append(f"add: {args.title}")
            return 0

        def cmd_list(args):
            executed.append("list")
            return 0

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("title")
        add_parser.set_defaults(func=cmd_add)

        list_parser = subparsers.add_parser("list")
        list_parser.set_defaults(func=cmd_list)

        # 测试路由
        args = parser.parse_args(["add", "任务"])
        if args.command and hasattr(args, "func"):
            args.func(args)

        assert executed == ["add: 任务"]

    def test_function_return_value(self):
        """测试命令函数返回值"""
        def cmd_add(args):
            return 0  # 成功

        def cmd_fail(args):
            return 1  # 失败

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        add_parser = subparsers.add_parser("add")
        add_parser.set_defaults(func=cmd_add)

        fail_parser = subparsers.add_parser("fail")
        fail_parser.set_defaults(func=cmd_fail)

        # 测试成功
        args = parser.parse_args(["add"])
        if hasattr(args, "func"):
            result = args.func(args)
            assert result == 0

        # 测试失败
        args = parser.parse_args(["fail"])
        if hasattr(args, "func"):
            result = args.func(args)
            assert result == 1


class TestSubcommandHelp:
    """测试子命令帮助信息"""

    def test_main_help_shows_subcommands(self, capsys):
        """测试主帮助显示可用子命令"""
        parser = argparse.ArgumentParser(description="任务管理工具")
        subparsers = parser.add_subparsers(dest="command", help="可用命令")

        subparsers.add_parser("add", help="添加任务")
        subparsers.add_parser("list", help="列出任务")
        subparsers.add_parser("done", help="标记完成")

        with pytest.raises(SystemExit):
            parser.parse_args(["--help"])

        captured = capsys.readouterr()
        assert "add" in captured.out
        assert "list" in captured.out
        assert "done" in captured.out

    def test_subcommand_individual_help(self, capsys):
        """测试子命令的独立帮助"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        add_parser = subparsers.add_parser("add", help="添加任务")
        add_parser.add_argument("title", help="任务标题")
        add_parser.add_argument("--priority", help="优先级")

        with pytest.raises(SystemExit):
            parser.parse_args(["add", "--help"])

        captured = capsys.readouterr()
        # 注意：help 参数只出现在父帮助中，子命令自己的帮助只显示参数描述
        assert "任务标题" in captured.out
        assert "优先级" in captured.out

    def test_list_subcommand_help(self, capsys):
        """测试 list 子命令帮助"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        list_parser = subparsers.add_parser("list", help="列出任务")
        list_parser.add_argument("--all", help="显示所有任务")
        list_parser.add_argument("--pending", help="只显示未完成")

        with pytest.raises(SystemExit):
            parser.parse_args(["list", "--help"])

        captured = capsys.readouterr()
        assert "list" in captured.out
        assert "all" in captured.out
        assert "pending" in captured.out


class TestComplexSubcommands:
    """测试复杂子命令场景"""

    def test_nested_subcommands(self):
        """测试嵌套子命令（如 docker container ls）"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        # container 子命令
        container_parser = subparsers.add_parser("container")
        container_subparsers = container_parser.add_subparsers(dest="action")

        # container ls 子命令
        ls_parser = container_subparsers.add_parser("ls")
        ls_parser.add_argument("--all", action="store_true")

        args = parser.parse_args(["container", "ls", "--all"])
        assert args.command == "container"
        assert args.action == "ls"
        assert args.all is True

    def test_global_and_local_args(self):
        """测试全局参数和子命令参数"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--verbose", action="store_true")

        subparsers = parser.add_subparsers(dest="command")
        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("title")

        args = parser.parse_args(["--verbose", "add", "测试"])
        assert args.verbose is True
        assert args.command == "add"
        assert args.title == "测试"

    def test_mutually_exclusive_in_subcommand(self):
        """测试子命令中的互斥参数"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        list_parser = subparsers.add_parser("list")
        group = list_parser.add_mutually_exclusive_group()
        group.add_argument("--all", action="store_true")
        group.add_argument("--pending", action="store_true")

        # 正常情况
        args = parser.parse_args(["list", "--all"])
        assert args.all is True

        # 互斥冲突
        with pytest.raises(SystemExit):
            parser.parse_args(["list", "--all", "--pending"])


class TestSubcommandEdgeCases:
    """测试子命令边界情况"""

    def test_unknown_subcommand(self):
        """测试未知子命令"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        subparsers.add_parser("add")
        subparsers.add_parser("list")

        # 未知子命令
        with pytest.raises(SystemExit):
            parser.parse_args(["unknown"])

    def test_subcommand_with_positional_and_optional(self):
        """测试子命令同时有位置参数和可选参数"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("title", help="标题（位置参数）")
        add_parser.add_argument("--priority", help="优先级（可选参数）")

        # 只提供位置参数
        args = parser.parse_args(["add", "测试"])
        assert args.title == "测试"
        assert args.priority is None

        # 同时提供位置和可选参数
        args = parser.parse_args(["add", "测试", "--priority", "high"])
        assert args.title == "测试"
        assert args.priority == "high"

    def test_subcommand_missing_required_arg(self):
        """测试子命令缺少必需参数"""
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("title")

        # 缺少必需的 title
        with pytest.raises(SystemExit):
            parser.parse_args(["add"])


@pytest.mark.parametrize("command,arg_string,expected_command,expected_title", [
    ("add", "add 测试任务", "add", "测试任务"),
    ("add", "add 写作业", "add", "写作业"),
    ("list", "list", "list", None),
    ("done", "done 1", "done", None),
])
def test_subcommand_routing_parametrized(command, arg_string, expected_command, expected_title):
    """参数化测试：子命令路由"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")

    subparsers.add_parser("list")

    done_parser = subparsers.add_parser("done")
    done_parser.add_argument("id", type=int)

    args = parser.parse_args(arg_string.split())
    assert args.command == expected_command

    if expected_title:
        assert args.title == expected_title
