"""测试退出码（exit codes）

这些测试验证学生对退出码概念的理解：
- sys.exit() 返回退出码
- 0 表示成功，非 0 表示失败
- 在子命令中使用退出码
- subprocess 测试退出码
- 标准输出和错误输出分离
"""

import pytest
import subprocess
import sys
import tempfile
import os

# 添加 starter_code 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))


class TestExitCodeBasics:
    """测试退出码基础"""

    def test_exit_zero_means_success(self):
        """测试退出码 0 表示成功"""
        # 创建一个简单的测试脚本
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import sys\nsys.exit(0)\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        assert result.returncode == 0

    def test_exit_nonzero_means_failure(self):
        """测试非 0 退出码表示失败"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import sys\nsys.exit(1)\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        assert result.returncode == 1

    def test_exit_with_different_codes(self):
        """测试不同的退出码"""
        for code in [0, 1, 2, 127, 130]:
            script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
            script.write(f'import sys\nsys.exit({code})\n')
            script.close()

            result = subprocess.run(
                [sys.executable, script.name],
                capture_output=True
            )

            os.unlink(script.name)
            assert result.returncode == code

    def test_no_exit_returns_zero(self):
        """测试没有 sys.exit() 时默认返回 0"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('print("正常执行")\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        assert result.returncode == 0


class TestExitCodesInFunctions:
    """测试函数返回退出码"""

    def test_function_returns_zero_on_success(self):
        """测试函数成功时返回 0"""
        def cmd_add(args):
            """添加任务"""
            if not args.title.strip():
                return 1
            return 0

        class Args:
            title = "测试任务"

        result = cmd_add(Args())
        assert result == 0

    def test_function_returns_nonzero_on_failure(self):
        """测试函数失败时返回非 0"""
        def cmd_add(args):
            """添加任务"""
            if not args.title.strip():
                return 1
            return 0

        class Args:
            title = ""

        result = cmd_add(Args())
        assert result == 1

    def test_function_returns_different_error_codes(self):
        """测试函数返回不同的错误码"""
        def cmd_done(args):
            """标记任务完成"""
            if args.id < 1:
                return 2  # 无效 ID
            if args.id > 100:
                return 3  # ID 不存在
            return 0

        class Args:
            id = 0

        result = cmd_done(Args())
        assert result == 2

        Args.id = 999
        result = cmd_done(Args())
        assert result == 3

        Args.id = 1
        result = cmd_done(Args())
        assert result == 0


class TestStdoutVsStderr:
    """测试标准输出和错误输出分离"""

    def test_print_to_stdout(self):
        """测试 print 输出到 stdout"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import sys\nprint("正常输出")\nsys.exit(0)\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)
        assert result.returncode == 0
        assert "正常输出" in result.stdout
        assert "" == result.stderr.strip()

    def test_print_to_stderr(self):
        """测试 print 输出到 stderr"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import sys\nprint("错误消息", file=sys.stderr)\nsys.exit(1)\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)
        assert result.returncode == 1
        assert "错误消息" in result.stderr
        assert "" == result.stdout.strip()

    def test_both_stdout_and_stderr(self):
        """测试同时输出到 stdout 和 stderr"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import sys\n')
        script.write('print("正常信息")\n')
        script.write('print("错误信息", file=sys.stderr)\n')
        script.write('sys.exit(1)\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)
        assert result.returncode == 1
        assert "正常信息" in result.stdout
        assert "错误信息" in result.stderr


class TestExitCodesWithArgparse:
    """测试 argparse 与退出码结合"""

    def test_missing_required_arg_exits_with_error(self):
        """测试缺少必需参数时退出"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import argparse\n')
        script.write('parser = argparse.ArgumentParser()\n')
        script.write('parser.add_argument("title", required=True)\n')
        script.write('parser.parse_args()\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        # argparse 遇到错误会退出并返回非 0
        assert result.returncode != 0

    def test_invalid_choice_exits_with_error(self):
        """测试无效选择时退出"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import argparse\n')
        script.write('parser = argparse.ArgumentParser()\n')
        script.write('parser.add_argument("--priority", choices=["low", "high"])\n')
        script.write('parser.parse_args(["--priority", "medium"])\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        assert result.returncode != 0


class TestExitCodesInSubcommands:
    """测试子命令中的退出码"""

    def test_subcommand_success_exits_zero(self):
        """测试子命令成功时退出码为 0"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import argparse\n')
        script.write('import sys\n\n')
        script.write('def cmd_add(args):\n')
        script.write('    print(f"添加任务: {args.title}")\n')
        script.write('    return 0\n\n')
        script.write('parser = argparse.ArgumentParser()\n')
        script.write('subparsers = parser.add_subparsers(dest="command")\n')
        script.write('add_parser = subparsers.add_parser("add")\n')
        script.write('add_parser.add_argument("title")\n')
        script.write('add_parser.set_defaults(func=cmd_add)\n\n')
        script.write('args = parser.parse_args(["add", "测试"])\n')
        script.write('if args.command:\n')
        script.write('    sys.exit(args.func(args))\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)
        assert result.returncode == 0
        assert "添加任务" in result.stdout

    def test_subcommand_failure_exits_one(self):
        """测试子命令失败时退出码为 1"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import argparse\n')
        script.write('import sys\n\n')
        script.write('def cmd_add(args):\n')
        script.write('    if not args.title:\n')
        script.write('        print("错误: 标题为空", file=sys.stderr)\n')
        script.write('        return 1\n')
        script.write('    return 0\n\n')
        script.write('parser = argparse.ArgumentParser()\n')
        script.write('subparsers = parser.add_subparsers(dest="command")\n')
        script.write('add_parser = subparsers.add_parser("add")\n')
        script.write('add_parser.add_argument("title")\n')
        script.write('add_parser.set_defaults(func=cmd_add)\n\n')
        script.write('args = parser.parse_args(["add", ""])\n')
        script.write('if args.command:\n')
        script.write('    sys.exit(args.func(args))\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)
        assert result.returncode == 1
        assert "错误" in result.stderr

    def test_no_subcommand_exits_with_error(self):
        """测试不提供子命令时退出"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import argparse\n')
        script.write('import sys\n\n')
        script.write('parser = argparse.ArgumentParser()\n')
        script.write('subparsers = parser.add_subparsers(dest="command")\n')
        script.write('subparsers.add_parser("add")\n\n')
        script.write('args = parser.parse_args()\n')
        script.write('if args.command:\n')
        script.write('    sys.exit(0)\n')
        script.write('else:\n')
        script.write('    print("错误: 缺少子命令", file=sys.stderr)\n')
        script.write('    sys.exit(1)\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True,
            text=True
        )

        os.unlink(script.name)
        assert result.returncode == 1
        assert "缺少子命令" in result.stderr


class TestExitCodesInScripts:
    """测试脚本中的退出码使用"""

    def test_bash_if_condition_with_exit_code(self):
        """测试 bash 脚本中的退出码判断"""
        # 创建一个返回 0 的脚本
        success_script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        success_script.write('import sys\nsys.exit(0)\n')
        success_script.close()

        # 创建一个返回 1 的脚本
        fail_script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        fail_script.write('import sys\nsys.exit(1)\n')
        fail_script.close()

        # 创建 bash 脚本
        bash_script = tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False)
        bash_script.write(f'#!/bin/bash\n')
        bash_script.write(f'{sys.executable} {success_script.name}\n')
        bash_script.write(f'if [ $? -eq 0 ]; then\n')
        bash_script.write(f'    echo "success"\n')
        bash_script.write(f'else\n')
        bash_script.write(f'    echo "fail"\n')
        bash_script.write(f'fi\n')
        bash_script.close()

        # 运行 bash 脚本
        result = subprocess.run(
            ['bash', bash_script.name],
            capture_output=True,
            text=True
        )

        os.unlink(success_script.name)
        os.unlink(fail_script.name)
        os.unlink(bash_script.name)

        assert result.returncode == 0
        assert "success" in result.stdout


class TestExitCodePatterns:
    """测试退出码常见模式"""

    @pytest.mark.parametrize("error_code,error_type", [
        (0, "success"),
        (1, "general_error"),
        (2, "misuse"),
        (126, "cannot_execute"),
        (127, "command_not_found"),
        (130, "interrupted"),
    ])
    def test_common_exit_codes(self, error_code, error_type):
        """测试常见退出码"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write(f'import sys\nsys.exit({error_code})\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        assert result.returncode == error_code

    def test_custom_exit_codes(self):
        """测试自定义退出码"""
        # 应用可以定义自己的退出码含义
        # 比如：2=文件不存在，3=权限不足
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import sys\n')
        script.write('# 文件不存在返回 2\n')
        script.write('sys.exit(2)\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        assert result.returncode == 2


class TestExitCodeEdgeCases:
    """测试退出码边界情况"""

    def test_negative_exit_code(self):
        """测试负数退出码"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import sys\nsys.exit(-1)\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        # 负数会被转换为正数
        assert result.returncode != 0

    def test_large_exit_code(self):
        """测试大数值退出码"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import sys\nsys.exit(255)\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        assert result.returncode == 255

    def test_exit_with_string(self):
        """测试 sys.exit() 传入字符串"""
        script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script.write('import sys\nsys.exit("错误消息")\n')
        script.close()

        result = subprocess.run(
            [sys.executable, script.name],
            capture_output=True
        )

        os.unlink(script.name)
        # 传入字符串会返回 1
        assert result.returncode == 1
        # result.stderr is bytes when text=False
        assert "错误消息" in result.stderr.decode('utf-8', errors='ignore')


@pytest.mark.parametrize("input_value,expected_exit_code", [
    ("valid_task", 0),
    ("", 1),
    ("   ", 1),
])
def test_exit_code_based_on_input(input_value, expected_exit_code):
    """参数化测试：根据输入返回不同的退出码"""
    script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
    script.write('import argparse\n')
    script.write('import sys\n\n')
    script.write('def cmd_add(args):\n')
    script.write('    if not args.title.strip():\n')
    script.write('        return 1\n')
    script.write('    return 0\n\n')
    script.write('parser = argparse.ArgumentParser()\n')
    script.write('parser.add_argument("title")\n')
    script.write('args = parser.parse_args()\n')
    script.write('sys.exit(cmd_add(args))\n')
    script.close()

    result = subprocess.run(
        [sys.executable, script.name, input_value],
        capture_output=True
    )

    os.unlink(script.name)
    assert result.returncode == expected_exit_code
