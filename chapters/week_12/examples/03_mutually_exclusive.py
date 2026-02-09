#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：互斥参数组（第 2 节）

本示例演示：
1. 如何创建互斥参数组
2. action="store_true" 的用法
3. argparse 自动检测参数冲突

运行方式：
    python3 chapters/week_12/examples/03_mutually_exclusive.py
    python3 chapters/week_12/examples/03_mutually_exclusive.py --all
    python3 chapters/week_12/examples/03_mutually_exclusive.py --pending
    python3 chapters/week_12/examples/03_mutually_exclusive.py --all --pending
预期输出：
    - 列出不同状态的任务
    - 同时使用互斥参数会报错
"""

import argparse


# =====================
# 创建解析器
# =====================

parser = argparse.ArgumentParser(
    description="任务列表工具"
)


# =====================
# 创建互斥参数组
# =====================

# 互斥组中的参数不能同时使用
group = parser.add_mutually_exclusive_group()

group.add_argument(
    "--all",
    action="store_true",  # 有这个参数就是 True，没有就是 False
    help="显示所有任务"
)

group.add_argument(
    "--pending",
    action="store_true",
    help="只显示未完成任务"
)

group.add_argument(
    "--done",
    action="store_true",
    help="只显示已完成任务"
)


# =====================
# 解析并执行
# =====================

args = parser.parse_args()

print("=" * 50)
print("任务列表")
print("=" * 50)

if args.all:
    print("模式：显示所有任务")
    print("  1. 写作业（已完成）")
    print("  2. 复习（进行中）")
    print("  3. 预习（未开始）")
elif args.pending:
    print("模式：只显示未完成任务")
    print("  2. 复习（进行中）")
    print("  3. 预习（未开始）")
elif args.done:
    print("模式：只显示已完成任务")
    print("  1. 写作业（已完成）")
else:
    # 默认行为：显示所有任务
    print("模式：显示所有任务（默认）")
    print("  1. 写作业（已完成）")
    print("  2. 复习（进行中）")
    print("  3. 预习（未开始）")

print()
print("提示：使用 --help 查看帮助")


# =====================
# 坏例子演示
# =====================

def bad_example_no_mutually_exclusive():
    """
    坏例子：不用互斥组，手动检查冲突

    问题：
    1. 需要写很多 if 语句检查组合
    2. 容易漏掉某些情况
    3. 错误提示不够友好
    """
    print("\n" + "=" * 50)
    print("【坏例子】不用互斥组，手动检查")
    print("=" * 50)

    parser_bad = argparse.ArgumentParser()
    parser_bad.add_argument("--all", action="store_true")
    parser_bad.add_argument("--pending", action="store_true")
    args_bad = parser_bad.parse_args([])

    # 手动检查冲突
    if args_bad.all and args_bad.pending:
        print("错误：--all 和 --pending 不能同时使用", file=__import__("sys").stderr)
    elif args_bad.all:
        print("显示所有任务")
    elif args_bad.pending:
        print("显示未完成任务")
    else:
        print("显示所有任务（默认）")

    print("\n问题：")
    print("  - 需要手动检查所有可能的冲突组合")
    print("  - 3 个参数有 C(3,2)=3 种冲突组合需要检查")
    print("  - 用 add_mutually_exclusive_group() 自动处理")


def bad_example_wrong_action():
    """
    坏例子：不用 action="store_true"

    问题：
    1. 用户必须提供参数值（如 --all True）
    2. 不符合命令行工具的习惯用法
    """
    print("\n" + "=" * 50)
    print("【坏例子】不用 action='store_true'")
    print("=" * 50)

    parser_bad = argparse.ArgumentParser()
    parser_bad.add_argument("--all")  # 没有 action="store_true"
    args_bad = parser_bad.parse_args(["--all", "True"])

    print(f"args.all = {args.bad}")
    print("\n问题：")
    print("  - 用户必须敲：python task.py --all True")
    print("  - 不符合习惯：应该直接敲 python task.py --all")
    print("  - 用 action='store_true' 自动处理布尔值")


if __name__ == "__main__":
    # 演示坏例子（可选）
    if "--show-bad" in __import__("sys").argv:
        bad_example_no_mutually_exclusive()
        bad_example_wrong_action()
