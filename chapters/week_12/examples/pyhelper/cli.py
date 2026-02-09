#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyHelper CLI 入口（Week 12：命令行工具）

本模块是 PyHelper 的命令行入口，演示：
1. argparse 子命令架构（add/list/search/export/stats）
2. 退出码的正确使用
3. logging 日志记录
4. --verbose 参数控制日志级别

基于 Week 11 的 dataclass 模型和 Week 10 的 JSON 存储。

运行方式：
    python3 -m chapters.week_12.examples.pyhelper.cli add "今天学了 argparse"
    python3 -m chapters.week_12.examples.pyhelper.cli list --pending
    python3 -m chapters.week_12.examples.pyhelper.cli search "argparse"
    python3 -m chapters.week_12.examples.pyhelper.cli export --format json
    python3 -m chapters.week_12.examples.pyhelper.cli stats

预期输出：
    - 不同子命令执行不同功能
    - 日志记录到 ~/.pyhelper/pyhelper.log
    - 返回正确的退出码
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional

# 导入 Week 11 的数据模型
# 注意：这里需要根据实际项目结构调整导入路径
# from .models import Note, NoteStatus

# 为了独立运行，这里重新定义模型（实际项目中应该导入）


# =====================
# 数据模型（Week 11）
# =====================

class NoteStatus(Enum):
    """笔记状态"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Note:
    """学习笔记（简化版 dataclass）"""
    def __init__(
        self,
        id: str,
        content: str,
        tags: List[str] = None,
        created_at: str = "",
        status: NoteStatus = NoteStatus.DRAFT
    ):
        self.id = id
        self.content = content
        self.tags = tags or []
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d")
        self.status = status

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at,
            "status": self.status.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """从字典恢复"""
        return cls(
            id=data["id"],
            content=data["content"],
            tags=data.get("tags", []),
            created_at=data.get("created_at", ""),
            status=NoteStatus(data.get("status", "draft"))
        )


# =====================
# 日志配置（Week 12）
# =====================

# 日志文件路径
LOG_DIR = Path.home() / ".pyhelper"
LOG_FILE = LOG_DIR / "pyhelper.log"

# 确保日志目录存在
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOG_FILE,
    encoding="utf-8"
)
logger = logging.getLogger(__name__)


# =====================
# 数据存储（Week 10）
# =====================

DATA_FILE = LOG_DIR / "notes.json"


def load_notes() -> List[Note]:
    """加载笔记列表"""
    if not DATA_FILE.exists():
        logger.info("数据文件不存在，返回空列表")
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        notes = [Note.from_dict(item) for item in data]
        logger.info(f"加载了 {len(notes)} 条笔记")
        return notes
    except json.JSONDecodeError as e:
        logger.error(f"数据文件格式错误：{e}")
        return []


def save_notes(notes: List[Note]) -> None:
    """保存笔记列表"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        data = [note.to_dict() for note in notes]
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"保存了 {len(notes)} 条笔记")


def generate_id() -> str:
    """生成笔记 ID"""
    return datetime.now().strftime("%Y%m%d-%H%M%S")


# =====================
# 核心功能函数
# =====================

def add_note(notes: List[Note], content: str, tags: List[str] = None) -> Note:
    """添加笔记"""
    note = Note(
        id=generate_id(),
        content=content,
        tags=tags or []
    )
    notes.append(note)
    return note


def filter_notes_by_status(notes: List[Note], status: NoteStatus) -> List[Note]:
    """按状态过滤笔记"""
    return [note for note in notes if note.status == status]


def search_notes(notes: List[Note], keyword: str) -> List[Note]:
    """搜索笔记（在内容和标签中查找）"""
    keyword_lower = keyword.lower()
    results = []
    for note in notes:
        if keyword_lower in note.content.lower():
            results.append(note)
        elif any(keyword_lower in tag.lower() for tag in note.tags):
            results.append(note)
    return results


def export_notes(notes: List[Note], output: str, format: str) -> None:
    """导出笔记"""
    output_path = Path(output)

    if format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            data = [note.to_dict() for note in notes]
            json.dump(data, f, ensure_ascii=False, indent=2)
    elif format == "csv":
        import csv
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Content", "Tags", "Created", "Status"])
            for note in notes:
                writer.writerow([
                    note.id,
                    note.content,
                    ",".join(note.tags),
                    note.created_at,
                    note.status.value
                ])


# =====================
# CLI 子命令处理函数
# =====================

def cmd_add(args):
    """添加学习笔记"""
    logger.info(f"添加笔记：{args.content}")

    notes = load_notes()

    # 添加笔记
    note = add_note(notes, args.content, args.tags)
    save_notes(notes)

    logger.info(f"笔记添加成功：{note.id}")
    print(f"✓ 笔记已添加：{note.id}")
    print(f"  内容：{note.content[:50]}...")
    return 0


def cmd_list(args):
    """列出笔记"""
    logger.info("列出笔记")

    notes = load_notes()

    # 过滤
    if args.pending:
        notes = filter_notes_by_status(notes, NoteStatus.DRAFT)
    elif args.published:
        notes = filter_notes_by_status(notes, NoteStatus.PUBLISHED)

    # 显示
    if not notes:
        print("没有笔记")
        return 0

    print("笔记列表：")
    print("=" * 60)
    for note in notes:
        status_icon = {
            NoteStatus.DRAFT: "○",
            NoteStatus.PUBLISHED: "✓",
            NoteStatus.ARCHIVED: "◉"
        }[note.status]

        print(f"{status_icon} [{note.id}] {note.content[:50]}...")
        if note.tags:
            print(f"     标签：{', '.join(note.tags)}")
        print(f"     创建：{note.created_at}")

    print(f"\n共 {len(notes)} 条笔记")
    return 0


def cmd_search(args):
    """搜索笔记"""
    logger.info(f"搜索笔记：{args.keyword}")

    notes = load_notes()
    results = search_notes(notes, args.keyword)

    if not results:
        print(f"没有找到包含 '{args.keyword}' 的笔记")
        return 0

    print(f"找到 {len(results)} 条匹配笔记：")
    print("=" * 60)
    for note in results:
        print(f"[{note.id}] {note.content[:60]}...")
        if note.tags:
            print(f"     标签：{', '.join(note.tags)}")

    return 0


def cmd_export(args):
    """导出笔记"""
    logger.info(f"导出笔记：{args.format}")

    notes = load_notes()

    # 导出
    export_notes(notes, args.output, args.format)

    logger.info(f"笔记已导出到 {args.output}")
    print(f"✓ 已导出 {len(notes)} 条笔记到 {args.output}")
    return 0


def cmd_stats(args):
    """显示统计信息"""
    logger.info("生成统计")

    notes = load_notes()

    total = len(notes)
    draft = len(filter_notes_by_status(notes, NoteStatus.DRAFT))
    published = len(filter_notes_by_status(notes, NoteStatus.PUBLISHED))
    archived = len(filter_notes_by_status(notes, NoteStatus.ARCHIVED))

    # 统计标签
    all_tags = {}
    for note in notes:
        for tag in note.tags:
            all_tags[tag] = all_tags.get(tag, 0) + 1

    print("PyHelper 统计")
    print("=" * 60)
    print(f"总笔记数：{total}")
    print(f"  - 草稿：{draft}")
    print(f"  - 已发布：{published}")
    print(f"  - 已归档：{archived}")

    if all_tags:
        print(f"\n热门标签：")
        for tag, count in sorted(all_tags.items(), key=lambda x: -x[1])[:5]:
            print(f"  - {tag}: {count}")

    if args.json:
        stats = {
            "total": total,
            "draft": draft,
            "published": published,
            "archived": archived,
            "top_tags": dict(sorted(all_tags.items(), key=lambda x: -x[1])[:5])
        }
        print("\nJSON 格式：")
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    return 0


# =====================
# 主入口
# =====================

def main():
    """主入口函数"""
    # 创建解析器
    parser = argparse.ArgumentParser(
        description="PyHelper - 命令行学习助手",
        epilog="示例：python pyhelper.py add '今天学了 argparse'"
    )

    # 全局参数
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细日志"
    )

    # 创建子命令
    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # add 子命令
    add_parser = subparsers.add_parser("add", help="添加学习笔记")
    add_parser.add_argument("content", help="笔记内容")
    add_parser.add_argument("--tags", nargs="*", help="标签（多个）")
    add_parser.set_defaults(func=cmd_add)

    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出笔记")
    group = list_parser.add_mutually_exclusive_group()
    group.add_argument("--pending", action="store_true", help="只显示草稿")
    group.add_argument("--published", action="store_true", help="只显示已发布")
    list_parser.set_defaults(func=cmd_list)

    # search 子命令
    search_parser = subparsers.add_parser("search", help="搜索笔记")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.set_defaults(func=cmd_search)

    # export 子命令
    export_parser = subparsers.add_parser("export", help="导出笔记")
    export_parser.add_argument("--output", "-o", default="backup.json", help="输出文件")
    export_parser.add_argument("--format", choices=["json", "csv"], default="json", help="导出格式")
    export_parser.set_defaults(func=cmd_export)

    # stats 子命令
    stats_parser = subparsers.add_parser("stats", help="统计信息")
    stats_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    stats_parser.set_defaults(func=cmd_stats)

    # 解析参数
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


if __name__ == "__main__":
    main()
