#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：最简单的 argparse 程序（第 1 节）

本示例演示：
1. 如何创建 ArgumentParser
2. 如何添加位置参数（必需参数）
3. argparse 自动生成帮助信息
4. argparse 自动验证必需参数

运行方式：
    python3 chapters/week_12/examples/01_simple_argparse.py "写作业"
    python3 chapters/week_12/examples/01_simple_argparse.py --help
预期输出：
    - 添加任务信息
    - 帮助文档（使用 --help）
"""

import argparse


# =====================
# 创建解析器
# =====================

parser = argparse.ArgumentParser(
    description="任务管理工具",
    epilog="示例：python task.py '写作业'"
)


# =====================
# 添加位置参数（必需）
# =====================

parser.add_argument(
    "title",  # 位置参数名（不需要 -- 前缀）
    help="任务标题（必需）"
)


# =====================
# 解析参数
# =====================

args = parser.parse_args()


# =====================
# 使用参数
# =====================

print(f"添加任务：{args.title}")
print(f"任务长度：{len(args.title)} 个字符")
print()
print("提示：使用 --help 查看帮助信息")


# =====================
# 坏例子演示（放在后面）
# =====================

def bad_example_using_sys_argv():
    """
    坏例子：用 sys.argv 手写解析

    问题：
    1. 需要手动检查参数个数
    2. 没有自动帮助信息
    3. 错误提示不友好
    4. 参数多了会很乱
    """
    import sys

    print("\n" + "=" * 50)
    print("【坏例子】用 sys.argv 手写解析")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("用法：python task.py <任务标题>", file=sys.stderr)
        sys.exit(1)

    title = sys.argv[1]
    print(f"添加任务：{title}")
    print("\n问题：")
    print("  - 需要手动检查参数个数")
    print("  - 没有 --help 帮助")
    print("  - 添加更多参数会很复杂")


if __name__ == "__main__":
    # 正确方式：使用 argparse
    print("=" * 50)
    print("【正确方式】使用 argparse")
    print("=" * 50)
    print()

    # 演示坏例子（可选）
    # bad_example_using_sys_argv()
