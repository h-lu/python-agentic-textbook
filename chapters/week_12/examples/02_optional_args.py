#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：可选参数与默认值（第 2 节）

本示例演示：
1. 可选参数（--option 格式）
2. 短选项和长选项（-p 和 --priority）
3. 参数默认值
4. choices 限制参数取值范围

运行方式：
    python3 chapters/week_12/examples/02_optional_args.py "写作业"
    python3 chapters/week_12/examples/02_optional_args.py "写作业" --priority high
    python3 chapters/week_12/examples/02_optional_args.py "写作业" -p high -t "Python,作业"
    python3 chapters/week_12/examples/02_optional_args.py "写作业" --priority ultra
预期输出：
    - 添加任务及优先级、标签信息
    - 非法优先级值会报错
"""

import argparse


# =====================
# 创建解析器
# =====================

parser = argparse.ArgumentParser(
    description="任务管理工具",
    epilog="示例：python task.py '写作业' --priority high"
)


# =====================
# 位置参数（必需）
# =====================

parser.add_argument(
    "title",
    help="任务标题（必需）"
)


# =====================
# 可选参数：短选项和长选项
# =====================

# -p 是短选项（敲起来快）
# --priority 是长选项（可读性强）
# 两者等价，用户可以任意选择
parser.add_argument(
    "-p",
    "--priority",
    help="任务优先级",
    choices=["low", "medium", "high"],  # 限制取值范围
    default="medium"  # 默认值
)


# =====================
# 可选参数：标签
# =====================

parser.add_argument(
    "-t",
    "--tags",
    help="任务标签（多个用逗号分隔）",
    default=""
)


# =====================
# 解析并使用
# =====================

args = parser.parse_args()

print("=" * 50)
print("添加任务")
print("=" * 50)
print(f"标题：    {args.title}")
print(f"优先级：  {args.priority}")

if args.tags:
    tags_list = [tag.strip() for tag in args.tags.split(",")]
    print(f"标签：    {', '.join(tags_list)}")
else:
    print("标签：    无")

print()


# =====================
# 坏例子演示
# =====================

def bad_example_no_choices():
    """
    坏例子：不限制参数取值范围

    问题：
    1. 用户可以输入任何值（包括拼写错误）
    2. 程序需要手动验证输入合法性
    3. 错误处理代码散落在各处
    """
    print("\n" + "=" * 50)
    print("【坏例子】不用 choices 限制范围")
    print("=" * 50)

    parser_bad = argparse.ArgumentParser()
    parser_bad.add_argument("--priority", default="medium")
    args_bad = parser_bad.parse_args([])

    print(f"优先级：{args_bad.priority}")
    print("\n问题：")
    print("  - 用户可以输入 'ultra'、'hige' 等错误值")
    print("  - 程序需要手动验证：if priority not in ['low', 'medium', 'high']")
    print("  - 用 choices=[...] 让 argparse 自动验证")


def bad_example_no_default():
    """
    坏例子：不设置默认值

    问题：
    1. 用户必须提供参数，不够灵活
    2. args.priority 可能是 None，需要额外判断
    """
    print("\n" + "=" * 50)
    print("【坏例子】不设置默认值")
    print("=" * 50)

    parser_bad = argparse.ArgumentParser()
    parser_bad.add_argument("--priority")  # 没有 default
    args_bad = parser_bad.parse_args([])

    print(f"优先级：{args_bad.priority}")
    print("\n问题：")
    print("  - 用户不传参数时，值为 None")
    print("  - 后续代码需要判断 if args.priority is None")
    print("  - 用 default='medium' 设置合理默认值")


if __name__ == "__main__":
    # 演示坏例子（可选）
    if "--show-bad" in __import__("sys").argv:
        bad_example_no_choices()
        bad_example_no_default()
