"""
测试 Week 12 示例代码的基本功能

这个测试文件验证所有示例是否能正常运行。
"""

import subprocess
import sys


def run_example(filename, args):
    """运行示例文件并返回结果"""
    cmd = [sys.executable, filename] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=5
    )
    return result


def test_01_simple_argparse():
    """测试 01_simple_argparse.py"""
    result = run_example(
        "chapters/week_12/examples/01_simple_argparse.py",
        ["测试任务"]
    )
    assert result.returncode == 0
    assert "添加任务" in result.stdout
    print("✓ 01_simple_argparse.py 通过")


def test_02_optional_args():
    """测试 02_optional_args.py"""
    result = run_example(
        "chapters/week_12/examples/02_optional_args.py",
        ["写作业", "--priority", "high"]
    )
    assert result.returncode == 0
    assert "high" in result.stdout
    print("✓ 02_optional_args.py 通过")


def test_03_mutually_exclusive():
    """测试 03_mutually_exclusive.py"""
    result = run_example(
        "chapters/week_12/examples/03_mutually_exclusive.py",
        ["--pending"]
    )
    assert result.returncode == 0
    assert "未完成" in result.stdout
    print("✓ 03_mutually_exclusive.py 通过")


def test_04_subcommands():
    """测试 04_subcommands.py"""
    result = run_example(
        "chapters/week_12/examples/04_subcommands.py",
        ["add", "写作业", "--priority", "high"]
    )
    assert result.returncode == 0
    assert "添加任务" in result.stdout
    print("✓ 04_subcommands.py 通过")


def test_05_exit_codes():
    """测试 05_exit_codes.py - 成功情况"""
    result = run_example(
        "chapters/week_12/examples/05_exit_codes.py",
        ["写作业"]
    )
    assert result.returncode == 0
    print("✓ 05_exit_codes.py（成功）通过")


def test_05_exit_codes_failure():
    """测试 05_exit_codes.py - 失败情况"""
    result = run_example(
        "chapters/week_12/examples/05_exit_codes.py",
        [""]
    )
    assert result.returncode == 1
    assert "错误" in result.stderr
    print("✓ 05_exit_codes.py（失败）通过")


def test_06_logging():
    """测试 06_logging.py"""
    result = run_example(
        "chapters/week_12/examples/06_logging.py",
        ["写作业"]
    )
    assert result.returncode == 0
    assert "添加任务" in result.stdout
    print("✓ 06_logging.py 通过")


def test_07_todo_cli_complete():
    """测试完整的 todo-cli 工具"""
    # 测试 add
    result = run_example(
        "chapters/week_12/examples/07_todo_cli_complete.py",
        ["add", "测试任务", "--priority", "high"]
    )
    assert result.returncode == 0
    assert "添加待办事项" in result.stdout

    # 测试 list
    result = run_example(
        "chapters/week_12/examples/07_todo_cli_complete.py",
        ["list"]
    )
    assert result.returncode == 0
    assert "待办事项列表" in result.stdout

    # 测试 stats
    result = run_example(
        "chapters/week_12/examples/07_todo_cli_complete.py",
        ["stats"]
    )
    assert result.returncode == 0
    assert "统计" in result.stdout

    print("✓ 07_todo_cli_complete.py 通过")


def test_pyhelper_cli():
    """测试 PyHelper CLI"""
    # 测试 add
    result = subprocess.run(
        [sys.executable, "-m", "chapters.week_12.examples.pyhelper.cli",
         "add", "测试笔记", "--tags", "test"],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode == 0
    assert "笔记已添加" in result.stdout

    # 测试 stats
    result = subprocess.run(
        [sys.executable, "-m", "chapters.week_12.examples.pyhelper.cli", "stats"],
        capture_output=True,
        text=True,
        timeout=5
    )
    assert result.returncode == 0
    assert "统计" in result.stdout

    print("✓ PyHelper CLI 通过")


if __name__ == "__main__":
    print("=" * 50)
    print("测试 Week 12 示例代码")
    print("=" * 50)

    test_01_simple_argparse()
    test_02_optional_args()
    test_03_mutually_exclusive()
    test_04_subcommands()
    test_05_exit_codes()
    test_05_exit_codes_failure()
    test_06_logging()
    test_07_todo_cli_complete()
    test_pyhelper_cli()

    print("=" * 50)
    print("所有测试通过！")
    print("=" * 50)
