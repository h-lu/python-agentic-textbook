#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Week 12 作业参考实现

本文件是作业的参考实现，当你在作业中遇到困难时可以查看。
请注意：
1. 这只是基础要求的实现，进阶部分需要你自己完成
2. 不要直接复制，理解后用自己的方式实现
3. 可以在此基础上添加你自己的改进

作业要求：
1. 用 argparse 创建 CLI 工具，支持 add/list/done 三个子命令
2. 用 dataclass 定义 Task 模型
3. 用 JSON 文件存储数据
4. 返回正确的退出码（成功 0，失败 1）
5. 用 logging 记录操作日志

进阶挑战：
1. 添加 delete 子命令
2. 添加 stats 子命令
3. 实现 --verbose 参数控制日志级别
4. 添加优先级支持（--priority 参数）
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List


# =====================
# 数据模型
# =====================

@dataclass
class Task:
    """待办事项数据模型"""
    title: str
    priority: str = "medium"
    completed: bool = False
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """转换为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """从字典恢复"""
        return cls(**data)


# =====================
# 日志配置
# =====================

LOG_FILE = Path("todo.log")

# 确保日志文件可以被创建
# logging.basicConfig 会在文件不存在时自动创建

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=LOG_FILE,
    encoding="utf-8"
)
logger = logging.getLogger(__name__)


# =====================
# 数据存储
# =====================

DATA_FILE = Path("todo.json")


def load_tasks() -> List[Task]:
    """加载待办事项列表"""
    if not DATA_FILE.exists():
        logger.info("数据文件不存在，返回空列表")
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        tasks = [Task.from_dict(item) for item in data]
        logger.info(f"加载了 {len(tasks)} 个待办事项")
        return tasks
    except json.JSONDecodeError as e:
        logger.error(f"数据文件格式错误：{e}")
        return []


def save_tasks(tasks: List[Task]) -> None:
    """保存待办事项列表"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        data = [task.to_dict() for task in tasks]
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"保存了 {len(tasks)} 个待办事项")


# =====================
# 子命令处理函数
# =====================

def cmd_add(args):
    """添加待办事项"""
    logger.info(f"添加待办事项：{args.title}")

    # 加载现有数据
    tasks = load_tasks()

    # 验证输入
    if not args.title.strip():
        logger.warning("待办事项标题为空")
        print("✗ 错误：待办事项标题不能为空", file=sys.stderr)
        return 1

    # 创建新待办事项
    new_task = Task(
        title=args.title,
        priority=args.priority
    )

    # 保存
    tasks.append(new_task)
    save_tasks(tasks)

    logger.info(f"待办事项添加成功")
    print(f"✓ 添加待办事项：{new_task.title}")
    print(f"  优先级：{new_task.priority}")
    return 0


def cmd_list(args):
    """列出待办事项"""
    logger.info("列出待办事项")

    tasks = load_tasks()

    # 过滤
    if args.pending:
        tasks = [t for t in tasks if not t.completed]
        logger.info(f"过滤未完成：{len(tasks)} 个")
    elif args.done:
        tasks = [t for t in tasks if t.completed]
        logger.info(f"过滤已完成：{len(tasks)} 个")

    # 显示
    if not tasks:
        print("没有待办事项")
        return 0

    print("待办事项列表：")
    print("=" * 50)
    for i, task in enumerate(tasks, 1):
        status_icon = "✓" if task.completed else "○"
        print(f"{status_icon} [{i}] {task.title}")
        print(f"     优先级：{task.priority} | 创建：{task.created_at}")

    print(f"\n共 {len(tasks)} 个待办事项")
    return 0


def cmd_done(args):
    """标记待办事项为完成"""
    logger.info(f"标记待办事项为完成：{args.index}")

    tasks = load_tasks()

    # 验证索引
    if args.index < 1 or args.index > len(tasks):
        logger.error(f"索引 {args.index} 超出范围")
        print(f"✗ 错误：索引 {args.index} 超出范围", file=sys.stderr)
        return 1

    # 标记完成
    task = tasks[args.index - 1]
    task.completed = True
    save_tasks(tasks)

    logger.info(f"待办事项已标记为完成")
    print(f"✓ 标记待办事项为完成：{task.title}")
    return 0


# =====================
# 主入口
# =====================

def main():
    """主入口函数"""
    # 创建解析器
    parser = argparse.ArgumentParser(
        description="todo-cli - 命令行待办事项工具",
        epilog="示例：python solution.py add '写作业' --priority high"
    )

    # 全局参数（进阶）
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细日志"
    )

    # 创建子命令
    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # add 子命令
    add_parser = subparsers.add_parser("add", help="添加待办事项")
    add_parser.add_argument("title", help="待办事项标题")
    add_parser.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="优先级"
    )
    add_parser.set_defaults(func=cmd_add)

    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出待办事项")
    group = list_parser.add_mutually_exclusive_group()
    group.add_argument("--pending", action="store_true", help="只显示未完成")
    group.add_argument("--done", action="store_true", help="只显示已完成")
    list_parser.set_defaults(func=cmd_list)

    # done 子命令
    done_parser = subparsers.add_parser("done", help="标记为完成")
    done_parser.add_argument("index", type=int, help="待办事项索引")
    done_parser.set_defaults(func=cmd_done)

    # 解析参数
    args = parser.parse_args()

    # 调整日志级别（进阶）
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("verbose 模式已启用")

    # 执行
    if args.command:
        exit_code = args.func(args)
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
