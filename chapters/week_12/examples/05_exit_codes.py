#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：退出码（第 4 节）

本示例演示：
1. 如何用 sys.exit() 返回退出码
2. 退出码约定：0 表示成功，非 0 表示失败
3. 错误消息输出到 stderr
4. 在子命令架构中使用退出码

运行方式：
    python3 chapters/week_12/examples/05_exit_codes.py "写作业" && echo "成功"
    python3 chapters/week_12/examples/05_exit_codes.py "" && echo "不会执行"
    echo $?
预期输出：
    - 成功时退出码为 0
    - 失败时退出码为 1
    - && 和 || 可以根据退出码决定是否执行
"""

import sys
import argparse


# =====================
# 创建解析器
# =====================

parser = argparse.ArgumentParser(description="任务管理工具")
parser.add_argument("title", help="任务标题")
args = parser.parse_args()


# =====================
# 业务逻辑（带退出码）
# =====================

# 验证输入
if not args.title.strip():
    # 错误消息输出到 stderr
    print("✗ 错误：任务标题不能为空", file=sys.stderr)
    sys.exit(1)  # 返回非 0 退出码表示失败


# 模拟添加任务
print(f"✓ 添加任务：{args.title}")
sys.exit(0)  # 返回 0 退出码表示成功


# =====================
# 坏例子演示
# =====================

def bad_example_no_exit_code():
    """
    坏例子：不返回退出码

    问题：
    1. 脚本无法判断命令是否成功
    2. 即使出错，退出码仍是 0
    3. 自动化流程会误判为成功
    """
    print("\n" + "=" * 50)
    print("【坏例子】不返回退出码")
    print("=" * 50)

    parser_bad = argparse.ArgumentParser()
    parser_bad.add_argument("title")
    args_bad = parser_bad.parse_args([""])

    if not args_bad.title.strip():
        print("✗ 错误：任务标题不能为空", file=sys.stderr)
        # 忘记写 sys.exit(1)
        # 程序继续执行，最终退出码为 0（默认）

    print("\n问题：")
    print("  - 即使出错，退出码仍是 0")
    print("  - 脚本中：python bad.py '' && echo '成功' 会打印'成功'")
    print("  - 应该在出错时调用 sys.exit(1)")


def bad_example_print_to_stdout():
    """
    坏例子：错误消息输出到 stdout

    问题：
    1. 脚本无法区分正常输出和错误消息
    2. 重定向 stdout 时，错误消息也会被重定向
    3. 日志系统无法正确捕获错误
    """
    print("\n" + "=" * 50)
    print("【坏例子】错误消息输出到 stdout")
    print("=" * 50)

    # 坏方式：错误消息用 print()（默认输出到 stdout）
    print("✗ 错误：任务标题不能为空")  # 输出到 stdout

    print("\n问题：")
    print("  - 脚本：python bad.py 2>/dev/null 仍会显示错误")
    print("  - 应该输出到 stderr：print(..., file=sys.stderr)")
    print("  - 这样脚本可以分别捕获 stdout 和 stderr")


def bad_example_too_many_exit_codes():
    """
    坏例子：过度设计退出码

    问题：
    1. 退出码太多，难以记忆
    2. 不同工具的退出码含义不统一
    3. 大多数情况下只需要 0 和 1
    """
    print("\n" + "=" * 50)
    print("【坏例子】过度设计退出码")
    print("=" * 50)

    print("过度设计的退出码：")
    print("  1 - 标题为空")
    print("  2 - 标题太长")
    print("  3 - 标题包含非法字符")
    print("  4 - 优先级无效")
    print("  ... (10+ 个退出码)")

    print("\n问题：")
    print("  - 三个月后自己也记不住")
    print("  - 其他开发者难以理解")
    print("  - 大多数情况：0 成功，1 失败 就够了")


def good_example_subcommands_with_exit_codes():
    """
    好例子：在子命令架构中使用退出码
    """
    print("\n" + "=" * 50)
    print("【好例子】子命令 + 退出码")
    print("=" * 50)

    def cmd_add(args):
        if not args.title.strip():
            print("✗ 错误：任务标题不能为空", file=sys.stderr)
            return 1
        print(f"✓ 添加任务：{args.title}")
        return 0

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=cmd_add)

    # 模拟调用
    print("add 子命令返回退出码：")
    print("  - 成功：0")
    print("  - 失败：1")
    print("  - 主流程：sys.exit(args.func(args))")


if __name__ == "__main__":
    # 主流程已经在上面执行
    # 坏例子需要单独调用
    pass
