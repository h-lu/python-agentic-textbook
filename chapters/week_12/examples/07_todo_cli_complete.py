#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：完整的 todo-cli 工具（综合示例）

本示例演示：
1. 完整的子命令架构（add/list/done/delete/stats）
2. dataclass 数据模型（关联 Week 11 知识）
3. JSON 文件存储（关联 Week 10 知识）
4. 退出码（成功 0，失败 1）
5. logging 日志记录
6. --verbose 参数控制日志级别

运行方式：
    python3 chapters/week_12/examples/07_todo_cli_complete.py add "写作业" --priority high
    python3 chapters/week_12/examples/07_todo_cli_complete.py list --pending
    python3 chapters/week_12/examples/07_todo_cli_complete.py done 1
    python3 chapters/week_12/examples/07_todo_cli_complete.py delete 2
    python3 chapters/week_12/examples/07_todo_cli_complete.py stats
    python3 chapters/week_12/examples/07_todo_cli_complete.py --help

预期输出：
    - 不同子命令执行不同功能
    - 日志记录到 todo_cli.log
    - 退出码正确返回
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional


# =====================
# 数据模型（Week 11 知识）
# =====================

class TodoStatus(Enum):
    """待办事项状态"""
    PENDING = "pending"
    DONE = "done"


@dataclass
class Todo:
    """待办事项数据模型"""
    id: int
    title: str
    priority: str
    status: TodoStatus = TodoStatus.PENDING
    created_at: str = ""

    def __post_init__(self):
        """初始化后处理"""
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """转换为字典（处理 Enum）"""
        data = asdict(self)
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        """从字典恢复"""
        data = data.copy()
        if "status" in data and isinstance(data["status"], str):
            data["status"] = TodoStatus(data["status"])
        return cls(**data)


# =====================
# 配置日志（Week 12 知识）
# =====================

LOG_FILE = Path("todo_cli.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=LOG_FILE,
    encoding="utf-8"
)
logger = logging.getLogger(__name__)


# =====================
# 数据存储（Week 10 知识）
# =====================

DATA_FILE = Path("todo_cli.json")


def load_todos() -> List[Todo]:
    """加载待办事项列表"""
    if not DATA_FILE.exists():
        logger.info("数据文件不存在，返回空列表")
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        todos = [Todo.from_dict(item) for item in data]
        logger.info(f"加载了 {len(todos)} 个待办事项")
        return todos
    except json.JSONDecodeError as e:
        logger.error(f"数据文件格式错误：{e}")
        print(f"✗ 错误：数据文件格式错误", file=sys.stderr)
        sys.exit(1)


def save_todos(todos: List[Todo]) -> None:
    """保存待办事项列表"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        data = [todo.to_dict() for todo in todos]
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"保存了 {len(todos)} 个待办事项")


def get_next_id(todos: List[Todo]) -> int:
    """获取下一个可用的 ID"""
    if not todos:
        return 1
    return max(todo.id for todo in todos) + 1


# =====================
# 子命令处理函数
# =====================

def cmd_add(args):
    """添加待办事项"""
    logger.info(f"尝试添加待办事项：{args.title}")

    # 加载现有数据
    todos = load_todos()

    # 创建新待办事项
    new_todo = Todo(
        id=get_next_id(todos),
        title=args.title,
        priority=args.priority
    )

    # 保存
    todos.append(new_todo)
    save_todos(todos)

    logger.info(f"待办事项添加成功：{new_todo.id}")
    print(f"✓ 添加待办事项 [{new_todo.id}]：{new_todo.title}")
    print(f"  优先级：{new_todo.priority}")
    return 0


def cmd_list(args):
    """列出待办事项"""
    logger.info("列出待办事项")

    todos = load_todos()

    # 过滤
    if args.pending:
        todos = [t for t in todos if t.status == TodoStatus.PENDING]
        logger.info(f"过滤未完成：{len(todos)} 个")
    elif args.done:
        todos = [t for t in todos if t.status == TodoStatus.DONE]
        logger.info(f"过滤已完成：{len(todos)} 个")

    # 显示
    if not todos:
        print("没有待办事项")
        return 0

    print("待办事项列表：")
    print("=" * 50)
    for todo in todos:
        status_icon = "✓" if todo.status == TodoStatus.DONE else "○"
        print(f"{status_icon} [{todo.id}] {todo.title}")
        print(f"     优先级：{todo.priority} | 创建时间：{todo.created_at}")

    print(f"\n共 {len(todos)} 个待办事项")
    return 0


def cmd_done(args):
    """标记待办事项为完成"""
    logger.info(f"标记待办事项为完成：{args.id}")

    todos = load_todos()

    # 查找待办事项
    todo = None
    for t in todos:
        if t.id == args.id:
            todo = t
            break

    if todo is None:
        logger.error(f"待办事项 {args.id} 不存在")
        print(f"✗ 错误：待办事项 {args.id} 不存在", file=sys.stderr)
        return 1

    # 更新状态
    todo.status = TodoStatus.DONE
    save_todos(todos)

    logger.info(f"待办事项 {args.id} 已标记为完成")
    print(f"✓ 标记待办事项 [{args.id}] 为完成")
    return 0


def cmd_delete(args):
    """删除待办事项"""
    logger.info(f"删除待办事项：{args.id}")

    todos = load_todos()

    # 查找待办事项
    todo_index = None
    for i, t in enumerate(todos):
        if t.id == args.id:
            todo_index = i
            break

    if todo_index is None:
        logger.error(f"待办事项 {args.id} 不存在")
        print(f"✗ 错误：待办事项 {args.id} 不存在", file=sys.stderr)
        return 1

    # 删除
    deleted_todo = todos.pop(todo_index)
    save_todos(todos)

    logger.info(f"待办事项 {args.id} 已删除")
    print(f"✓ 删除待办事项 [{args.id}]：{deleted_todo.title}")
    return 0


def cmd_stats(args):
    """显示统计信息"""
    logger.info("生成统计信息")

    todos = load_todos()

    total = len(todos)
    pending = len([t for t in todos if t.status == TodoStatus.PENDING])
    done = len([t for t in todos if t.status == TodoStatus.DONE])

    high_priority = len([t for t in todos if t.priority == "high" and t.status == TodoStatus.PENDING])

    print("Todo CLI 统计")
    print("=" * 50)
    print(f"总待办事项：{total}")
    print(f"  - 未完成：{pending}")
    print(f"  - 已完成：{done}")
    print(f"高优先级未完成：{high_priority}")

    if args.json:
        stats = {
            "total": total,
            "pending": pending,
            "done": done,
            "high_priority_pending": high_priority
        }
        print("\nJSON 格式：")
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    return 0


# =====================
# 创建主解析器
# =====================

parser = argparse.ArgumentParser(
    description="todo-cli - 命令行待办事项工具",
    epilog="示例：python todo_cli.py add '写作业' --priority high"
)

# 全局参数
parser.add_argument(
    "--verbose",
    action="store_true",
    help="显示详细日志"
)

# 创建子命令
subparsers = parser.add_subparsers(dest="command", help="可用子命令")


# =====================
# 添加子命令
# =====================

# add
add_parser = subparsers.add_parser("add", help="添加待办事项")
add_parser.add_argument("title", help="待办事项标题")
add_parser.add_argument(
    "--priority",
    choices=["low", "medium", "high"],
    default="medium",
    help="优先级"
)
add_parser.set_defaults(func=cmd_add)

# list
list_parser = subparsers.add_parser("list", help="列出版办事项")
group = list_parser.add_mutually_exclusive_group()
group.add_argument("--pending", action="store_true", help="只显示未完成")
group.add_argument("--done", action="store_true", help="只显示已完成")
list_parser.set_defaults(func=cmd_list)

# done
done_parser = subparsers.add_parser("done", help="标记为完成")
done_parser.add_argument("id", type=int, help="待办事项 ID")
done_parser.set_defaults(func=cmd_done)

# delete
delete_parser = subparsers.add_parser("delete", help="删除待办事项")
delete_parser.add_argument("id", type=int, help="待办事项 ID")
delete_parser.set_defaults(func=cmd_delete)

# stats
stats_parser = subparsers.add_parser("stats", help="统计信息")
stats_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
stats_parser.set_defaults(func=cmd_stats)


# =====================
# 解析并执行
# =====================

args = parser.parse_args()

# 调整日志级别
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


# =====================
# 总结
# =====================

"""
本示例综合运用了本周和之前的知识：

Week 12（本周）：
  - argparse：命令行参数解析
  - 子命令：add/list/done/delete/stats
  - 退出码：0 成功，1 失败
  - logging：日志记录到文件

Week 11（上周）：
  - dataclass：Todo 数据模型
  - Enum：TodoStatus 状态管理
  - 类型提示：List[Todo] 等

Week 10（之前）：
  - JSON 序列化：to_dict() / from_dict()
  - 文件读写：load_todos() / save_todos()

这是一个完整、可用的 CLI 工具，可以作为 PyHelper 的参考。
"""
