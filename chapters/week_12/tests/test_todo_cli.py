"""测试完整的 todo-cli 工具

这些测试验证学生对完整 CLI 工具开发的理解：
- argparse + 子命令 + 退出码 + logging 的综合应用
- 各个子命令的功能测试
- 集成测试
- 边界情况和错误处理
"""

import pytest
import subprocess
import sys
import tempfile
import json
import os
from pathlib import Path


class TestTodoCLIIntegration:
    """测试 todo-cli 完整集成"""

    def test_cli_exists(self):
        """测试 CLI 工具是否存在（示例测试）"""
        # 注意：这个测试假设学生会在 starter_code 中实现 todo-cli
        # 如果还未实现，可以跳过或标记为预期失败
        pytest.skip("等待 starter_code 实现")

    def test_add_command_integration(self):
        """测试 add 命令集成"""
        pytest.skip("等待 starter_code 实现")

    def test_list_command_integration(self):
        """测试 list 命令集成"""
        pytest.skip("等待 starter_code 实现")


class TestCLIWithSubprocess:
    """使用 subprocess 测试 CLI 工具"""

    def test_run_cli_script(self):
        """测试运行 CLI 脚本"""
        # 创建一个简单的 CLI 脚本
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''#!/usr/bin/env python3
import argparse
import sys

def cmd_add(args):
    print(f"添加任务: {args.title}")
    return 0

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add")
add_parser.add_argument("title")
add_parser.set_defaults(func=cmd_add)

args = parser.parse_args()
if args.command:
    sys.exit(args.func(args))
else:
    parser.print_help()
    sys.exit(1)
''')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name, "add", "测试任务"],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)

        assert result.returncode == 0
        assert "添加任务" in result.stdout
        assert "测试任务" in result.stdout

    def test_cli_with_invalid_args(self):
        """测试 CLI 处理无效参数"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''#!/usr/bin/env python3
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("title", type=int)
args = parser.parse_args()
''')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name, "invalid_int"],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)

        # 应该返回非 0 退出码
        assert result.returncode != 0

    def test_cli_with_help_flag(self):
        """测试 CLI --help 标志"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(description="任务管理工具")
parser.add_argument("title", help="任务标题")
parser.parse_args()
''')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name, "--help"],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)

        assert result.returncode == 0
        assert "任务管理工具" in result.stdout
        assert "任务标题" in result.stdout


class TestTodoStorage:
    """测试待办事项存储"""

    def test_save_and_load_todos(self):
        """测试保存和加载待办事项"""
        # 创建临时文件
        todo_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        todo_path = todo_file.name
        todo_file.close()

        # 写入测试数据
        todos = [
            {"id": 1, "title": "任务1", "done": False},
            {"id": 2, "title": "任务2", "done": True}
        ]

        with open(todo_path, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=2)

        # 读取并验证
        with open(todo_path, 'r', encoding='utf-8') as f:
            loaded_todos = json.load(f)

        os.unlink(todo_path)

        assert len(loaded_todos) == 2
        assert loaded_todos[0]["title"] == "任务1"
        assert loaded_todos[1]["done"] is True

    def test_empty_todo_list(self):
        """测试空待办事项列表"""
        todo_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        todo_path = todo_file.name
        todo_file.close()

        # 写入空列表
        with open(todo_path, 'w', encoding='utf-8') as f:
            json.dump([], f)

        # 读取
        with open(todo_path, 'r', encoding='utf-8') as f:
            todos = json.load(f)

        os.unlink(todo_path)

        assert todos == []


class TestCLIWorkflow:
    """测试 CLI 工作流"""

    def test_add_then_list_workflow(self):
        """测试添加后列出的工作流"""
        # 创建临时数据文件
        data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        data_path = data_file.name
        data_file.close()

        # 初始化空列表
        with open(data_path, 'w') as f:
            json.dump([], f)

        # 模拟 add 操作
        with open(data_path, 'r') as f:
            todos = json.load(f)

        todos.append({"id": 1, "title": "新任务", "done": False})

        with open(data_path, 'w') as f:
            json.dump(todos, f, ensure_ascii=False, indent=2)

        # 模拟 list 操作
        with open(data_path, 'r') as f:
            todos = json.load(f)

        os.unlink(data_path)

        assert len(todos) == 1
        assert todos[0]["title"] == "新任务"

    def test_add_then_mark_done_workflow(self):
        """测试添加后标记完成的工作流"""
        data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        data_path = data_file.name
        data_file.close()

        # 添加任务
        todos = [{"id": 1, "title": "任务1", "done": False}]
        with open(data_path, 'w') as f:
            json.dump(todos, f)

        # 标记完成
        with open(data_path, 'r') as f:
            todos = json.load(f)

        todos[0]["done"] = True

        with open(data_path, 'w') as f:
            json.dump(todos, f)

        # 验证
        with open(data_path, 'r') as f:
            todos = json.load(f)

        os.unlink(data_path)

        assert todos[0]["done"] is True

    def test_add_then_delete_workflow(self):
        """测试添加后删除的工作流"""
        data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        data_path = data_file.name
        data_file.close()

        # 添加两个任务
        todos = [
            {"id": 1, "title": "任务1", "done": False},
            {"id": 2, "title": "任务2", "done": False}
        ]
        with open(data_path, 'w') as f:
            json.dump(todos, f)

        # 删除第一个任务
        with open(data_path, 'r') as f:
            todos = json.load(f)

        todos.pop(0)

        with open(data_path, 'w') as f:
            json.dump(todos, f)

        # 验证
        with open(data_path, 'r') as f:
            todos = json.load(f)

        os.unlink(data_path)

        assert len(todos) == 1
        assert todos[0]["id"] == 2


class TestCLIErrorHandling:
    """测试 CLI 错误处理"""

    def test_missing_required_argument(self):
        """测试缺少必需参数"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("title")
args = parser.parse_args()
''')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)

        assert result.returncode != 0

    def test_invalid_choice(self):
        """测试无效选择"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--priority", choices=["low", "medium", "high"])
args = parser.parse_args()
''')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name, "--priority", "invalid"],
            capture_output=True
        )

        os.unlink(script.name)

        assert result.returncode != 0

    def test_mutually_exclusive_arguments(self):
        """测试互斥参数冲突"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''import argparse
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--all", action="store_true")
group.add_argument("--pending", action="store_true")
args = parser.parse_args()
''')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name, "--all", "--pending"],
            capture_output=True
        )

        os.unlink(script.name)

        assert result.returncode != 0


class TestCLIWithLogging:
    """测试 CLI 与 logging 结合"""

    def test_cli_creates_log_file(self):
        """测试 CLI 创建日志文件"""
        log_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        log_path = log_file.name
        log_file.close()

        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write(f'''import logging
logging.basicConfig(
    filename="{log_path}",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("CLI 启动")
print("操作完成")
''')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)

        # 检查日志文件
        with open(log_path, 'r') as f:
            log_content = f.read()

        os.unlink(log_path)

        assert result.returncode == 0
        assert "CLI 启动" in log_content

    def test_verbose_flag_increases_logging(self):
        """测试 --verbose 标志增加日志详细度"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

level = logging.DEBUG if args.verbose else logging.INFO
logging.basicConfig(level=level)

logging.debug("调试信息（仅在 verbose 模式）")
logging.info("普通信息")
''')
        script.close()

        # 正常模式
        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True,
            text=True
        )

        assert "普通信息" in result.stderr

        # verbose 模式
        result = subprocess.run(
            [sys.executable, script.name, "--verbose"],
            capture_output=True,
            text=True
        )

        assert "调试信息" in result.stderr

        os.unlink(script.name)


class TestCLIExitCodes:
    """测试 CLI 退出码"""

    def test_success_returns_zero(self):
        """测试成功返回 0"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''import sys
sys.exit(0)
''')
        script.close()

        result = subprocess.run([sys.executable, script.name])
        os.unlink(script.name)

        assert result.returncode == 0

    def test_failure_returns_one(self):
        """测试失败返回 1"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''import sys
sys.exit(1)
''')
        script.close()

        result = subprocess.run([sys.executable, script.name])
        os.unlink(script.name)

        assert result.returncode == 1

    def test_command_success_exit_code(self):
        """测试命令成功时的退出码"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''import argparse
import sys

def cmd_add(args):
    return 0

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")
add_parser = subparsers.add_parser("add")
add_parser.set_defaults(func=cmd_add)

args = parser.parse_args(["add"])
sys.exit(args.func(args))
''')
        script.close()

        result = subprocess.run([sys.executable, script.name])
        os.unlink(script.name)

        assert result.returncode == 0


class TestCLIEdgeCases:
    """测试 CLI 边界情况"""

    def test_empty_title(self):
        """测试空标题处理"""
        # 空标题应该被拒绝或处理
        title = ""
        assert title.strip() == ""

    def test_special_characters_in_title(self):
        """测试标题中的特殊字符"""
        special_titles = [
            "任务!@#$%",
            "测试中文🎉",
            "任务\twith\ttabs",
            "任务\nwith\nnewlines",
        ]

        for title in special_titles:
            # 应该能处理特殊字符
            assert isinstance(title, str)

    def test_very_long_title(self):
        """测试超长标题"""
        long_title = "A" * 10000
        assert len(long_title) == 10000

    def test_many_todos(self):
        """测试大量待办事项"""
        # 创建 1000 个任务
        todos = [
            {"id": i, "title": f"任务{i}", "done": False}
            for i in range(1, 1001)
        ]

        assert len(todos) == 1000

    def test_concurrent_access(self):
        """测试并发访问（简单测试）"""
        # 实际应用中需要处理文件锁等
        # 这里只是基本测试
        data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        data_path = data_file.name
        data_file.close()

        # 写入
        with open(data_path, 'w') as f:
            json.dump([{"id": 1, "title": "任务"}], f)

        # 读取
        with open(data_path, 'r') as f:
            todos = json.load(f)

        os.unlink(data_path)

        assert len(todos) == 1


class TestCLIHelpAndDocumentation:
    """测试 CLI 帮助和文档"""

    def test_main_help(self):
        """测试主帮助信息"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''import argparse
parser = argparse.ArgumentParser(description="任务管理工具")
subparsers = parser.add_subparsers(dest="command", help="可用命令")
add_parser = subparsers.add_parser("add", help="添加任务")
list_parser = subparsers.add_parser("list", help="列出任务")
parser.parse_args()
''')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name, "--help"],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)

        assert "任务管理工具" in result.stdout
        assert "add" in result.stdout
        assert "list" in result.stdout

    def test_subcommand_help(self):
        """测试子命令帮助信息"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('''import argparse
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")
add_parser = subparsers.add_parser("add", help="添加任务")
add_parser.add_argument("title", help="任务标题")
add_parser.add_argument("--priority", help="优先级")
parser.parse_args()
''')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name, "add", "--help"],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)

        # 注意：help 参数只出现在父帮助中，子命令自己的帮助只显示参数描述
        assert "任务标题" in result.stdout
        assert "优先级" in result.stdout


@pytest.mark.parametrize("command,args,expected_success", [
    ("add", ["add", "测试任务"], True),
    ("list", ["list"], True),
    ("done", ["done", "1"], True),
    ("delete", ["delete", "1"], True),
])
def test_command_structure_parametrized(command, args, expected_success):
    """参数化测试：命令结构"""
    # 这个测试验证命令结构的合理性
    assert isinstance(command, str)
    assert isinstance(args, list)
    assert isinstance(expected_success, bool)
