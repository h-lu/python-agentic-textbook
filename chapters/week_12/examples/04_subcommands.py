#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：子命令架构（第 3 节）

本示例演示：
1. 如何用 add_subparsers() 创建子命令
2. 每个子命令有独立的参数
3. 用 dest="command" 获取用户选择的子命令
4. 用 set_defaults(func=...) 路由到处理函数

运行方式：
    python3 chapters/week_12/examples/04_subcommands.py
    python3 chapters/week_12/examples/04_subcommands.py add "写作业" --priority high
    python3 chapters/week_12/examples/04_subcommands.py list --pending
    python3 chapters/week_12/examples/04_subcommands.py done 1
    python3 chapters/week_12/examples/04_subcommands.py add --help
预期输出：
    - 不同子命令执行不同功能
    - 每个子命令有独立的帮助文档
"""

import argparse
import sys


# =====================
# 子命令处理函数
# =====================

def cmd_add(args):
    """添加任务"""
    print(f"✓ 添加任务：{args.title}")
    print(f"  优先级：{args.priority}")
    return 0  # 成功退出码


def cmd_list(args):
    """列出任务"""
    if args.all:
        print("列出所有任务")
    elif args.pending:
        print("列出来完成任务")
    else:
        print("列出所有任务（默认）")

    # 模拟数据
    print("  1. 写作业（进行中）")
    print("  2. 复习（未开始）")
    return 0


def cmd_done(args):
    """标记任务完成"""
    # 模拟：检查任务 ID 是否存在
    if args.id < 1 or args.id > 100:
        print(f"✗ 错误：任务 ID {args.id} 不存在", file=sys.stderr)
        return 1  # 失败退出码

    print(f"✓ 标记任务 {args.id} 为完成")
    return 0


def cmd_delete(args):
    """删除任务"""
    if args.id < 1 or args.id > 100:
        print(f"✗ 错误：任务 ID {args.id} 不存在", file=sys.stderr)
        return 1

    print(f"✓ 删除任务 {args.id}")
    return 0


# =====================
# 创建主解析器
# =====================

parser = argparse.ArgumentParser(
    description="todo-cli - 命令行待办事项工具",
    epilog="示例：python todo.py add '写作业' --priority high"
)

# 创建子命令解析器
subparsers = parser.add_subparsers(
    dest="command",  # 把子命令名存到 args.command
    help="可用子命令"
)


# =====================
# 添加 'add' 子命令
# =====================

add_parser = subparsers.add_parser(
    "add",
    help="添加新任务"
)
add_parser.add_argument(
    "title",
    help="任务标题"
)
add_parser.add_argument(
    "--priority",
    choices=["low", "medium", "high"],
    default="medium",
    help="任务优先级"
)
add_parser.set_defaults(func=cmd_add)  # 路由到 cmd_add 函数


# =====================
# 添加 'list' 子命令
# =====================

list_parser = subparsers.add_parser(
    "list",
    help="列出任务"
)
group = list_parser.add_mutually_exclusive_group()
group.add_argument(
    "--all",
    action="store_true",
    help="显示所有任务"
)
group.add_argument(
    "--pending",
    action="store_true",
    help="只显示未完成任务"
)
list_parser.set_defaults(func=cmd_list)


# =====================
# 添加 'done' 子命令
# =====================

done_parser = subparsers.add_parser(
    "done",
    help="标记任务为完成"
)
done_parser.add_argument(
    "id",
    type=int,  # 自动转换为整数
    help="任务 ID"
)
done_parser.set_defaults(func=cmd_done)


# =====================
# 添加 'delete' 子命令
# =====================

delete_parser = subparsers.add_parser(
    "delete",
    help="删除任务"
)
delete_parser.add_argument(
    "id",
    type=int,
    help="任务 ID"
)
delete_parser.set_defaults(func=cmd_delete)


# =====================
# 解析并执行
# =====================

args = parser.parse_args()

# 如果用户没有提供子命令，显示帮助
if args.command is None:
    parser.print_help()
    sys.exit(1)

# 调用对应的处理函数
exit_code = args.func(args)
sys.exit(exit_code)


# =====================
# 坏例子演示（单独运行查看）
# =====================

def bad_example_if_chain():
    """
    坏例子：用 if 链条处理子命令

    问题：
    1. if args.command == "add" 重复多次
    2. 子命令逻辑分散在主流程中
    3. 不易于测试和维护
    """
    print("\n" + "=" * 50)
    print("【坏例子】用 if 链条处理子命令")
    print("=" * 50)

    parser_bad = argparse.ArgumentParser()
    subparsers_bad = parser_bad.add_subparsers(dest="command")

    add_parser = subparsers_bad.add_parser("add")
    add_parser.add_argument("title")

    list_parser = subparsers_bad.add_parser("list")

    args_bad = parser_bad.parse_args(["add", "写作业"])

    # 坏方式：if 链条
    if args_bad.command == "add":
        print(f"添加任务：{args_bad.title}")
    elif args_bad.command == "list":
        print("列出任务")
    # ... 更多 elif

    print("\n问题：")
    print("  - 子命令逻辑分散在 if 链条中")
    print("  - 难以单独测试某个子命令")
    print("  - 用 set_defaults(func=cmd_add) 路由到函数")


def bad_example_no_subparsers():
    """
    坏例子：不用子命令，用单一命令 + 参数

    问题：
    1. 命令不清晰：todo.py --action add --title "写作业"
    2. 不符合 CLI 工具习惯（应该是 todo.py add "写作业"）
    3. 帮助文档混乱
    """
    print("\n" + "=" * 50)
    print("【坏例子】不用子命令")
    print("=" * 50)

    parser_bad = argparse.ArgumentParser()
    parser_bad.add_argument("--action", choices=["add", "list", "done"])
    parser_bad.add_argument("--title")
    parser_bad.add_argument("--id", type=int)

    args_bad = parser_bad.parse_args(["--action", "add", "--title", "写作业"])

    if args_bad.action == "add":
        print(f"添加任务：{args_bad.title}")

    print("\n问题：")
    print("  - 命令冗长：todo.py --action add --title '写作业'")
    print("  - 应该简洁：todo.py add '写作业'")
    print("  - 用子命令架构符合 CLI 工具习惯")


if __name__ == "__main__":
    # 坏例子需要在命令行中显式调用
    # if "--show-bad" in sys.argv:
    #     bad_example_if_chain()
    #     bad_example_no_subparsers()
    pass
