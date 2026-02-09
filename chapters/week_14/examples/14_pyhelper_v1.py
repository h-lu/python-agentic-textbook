#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyHelper v1.0.0 - 命令行学习助手（最终发布版本）

本书超级线的终点：从 Week 01 的 print() 到 Week 14 的完整 CLI 工具。

本版本整合了 14 周的所有核心知识：
- Week 11: dataclass 数据模型（Note, NoteStatus, StudyPlan）
- Week 10: JSON 存储（序列化/反序列化）
- Week 12: argparse CLI（子命令、参数解析、退出码）
- Week 12: logging 日志（级别、格式、文件）
- Week 06: 异常处理（try/except、优雅降级）
- Week 13: agent team（reader/writer/reviewer 协作）

功能清单：
- add: 添加学习笔记
- list: 列出笔记（支持过滤）
- search: 搜索笔记（关键词）
- export: 导出笔记（JSON/CSV/Markdown）
- stats: 统计信息
- plan generate: 生成学习计划（agent team）
- plan show: 显示学习计划

运行方式：
    python3 chapters/week_14/examples/14_pyhelper_v1.py add "今天学了代码收敛"
    python3 chapters/week_14/examples/14_pyhelper_v1.py list
    python3 chapters/week_14/examples/14_pyhelper_v1.py search "代码"
    python3 chapters/week_14/examples/14_pyhelper_v1.py export --format json
    python3 chapters/week_14/examples/14_pyhelper_v1.py stats
    python3 chapters/week_14/examples/14_pyhelper_v1.py plan generate

预期输出：
    - 不同子命令执行对应功能
    - 日志记录到 ~/.pyhelper/pyhelper.log
    - 返回正确的退出码（0=成功，1=失败）
"""

import argparse
import csv
import json
import logging
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict


# =====================
# 数据模型（Week 11）
# =====================

class NoteStatus(Enum):
    """笔记状态枚举"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


@dataclass
class Note:
    """学习笔记（dataclass 数据模型）"""
    id: str
    content: str
    tags: List[str]
    created_at: str
    status: NoteStatus

    def to_dict(self) -> dict:
        """转换为字典（用于 JSON 序列化）"""
        return {
            "id": self.id,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at,
            "status": self.status.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """从字典恢复（用于 JSON 反序列化）"""
        return cls(
            id=data["id"],
            content=data["content"],
            tags=data.get("tags", []),
            created_at=data.get("created_at", datetime.now().strftime("%Y-%m-%d")),
            status=NoteStatus(data.get("status", "draft"))
        )


@dataclass
class StudyPlan:
    """学习计划（dataclass 数据模型）"""
    week: int
    title: str
    prerequisites: List[str]
    priority: str  # high/medium/low
    topics: List[str]
    estimated_hours: int

    def to_dict(self) -> dict:
        """转换为字典"""
        return asdict(self)


# =====================
# 日志配置（Week 12）
# =====================

LOG_DIR = Path.home() / ".pyhelper"
LOG_FILE = LOG_DIR / "pyhelper.log"
DATA_FILE = LOG_DIR / "notes.json"
PLAN_FILE = LOG_DIR / "plan.json"

# 确保目录存在
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

def load_notes() -> List[Note]:
    """加载笔记列表（JSON 反序列化）"""
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
    except Exception as e:
        logger.error(f"加载数据失败：{e}")
        return []


def save_notes(notes: List[Note]) -> None:
    """保存笔记列表（JSON 序列化）"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            data = [note.to_dict() for note in notes]
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"保存了 {len(notes)} 条笔记")
    except Exception as e:
        logger.error(f"保存数据失败：{e}")
        raise


def generate_id() -> str:
    """生成笔记 ID（基于时间戳）"""
    return datetime.now().strftime("%Y%m%d-%H%M%S")


# =====================
# Agent Team（Week 13）
# =====================

class ReaderAgent:
    """reader agent：读取并分析笔记文件"""

    def read_note(self, file_path: Path) -> Optional[Dict]:
        """读取笔记文件并提取关键信息"""
        logger.info(f"读取笔记：{file_path}")

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"读取失败：{e}")
            return None

        # 提取周次（从文件名）
        week_match = re.search(r'week(\d+)', file_path.name, re.IGNORECASE)
        week = int(week_match.group(1)) if week_match else 0

        # 提取标题（第一个 # 标题）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem

        # 简化版：提取主题
        topics = []
        if "异常" in content or "Exception" in content:
            topics.append("异常处理")
        if "测试" in content or "test" in content.lower():
            topics.append("测试")
        if "函数" in content or "def " in content:
            topics.append("函数")
        if "文件" in content or "file" in content.lower():
            topics.append("文件")
        if "JSON" in content or "json" in content.lower():
            topics.append("JSON")
        if "dataclass" in content:
            topics.append("dataclass")
        if "argparse" in content:
            topics.append("argparse")

        # 根据主题数量推断难度
        difficulty = "hard" if len(topics) >= 3 else "medium" if len(topics) >= 1 else "easy"

        return {
            "week": week,
            "title": title,
            "topics": topics,
            "difficulty": difficulty
        }


class WriterAgent:
    """writer agent：根据笔记分析生成学习计划"""

    def create_plan(self, analysis: Dict, all_topics: List[str]) -> StudyPlan:
        """根据笔记分析生成学习计划"""
        week = analysis["week"]
        title = analysis["title"]
        topics = analysis["topics"]
        difficulty = analysis["difficulty"]

        logger.info(f"生成学习计划：Week {week} - {title}")

        # 推断前置知识
        prerequisites = self._infer_prerequisites(week, all_topics)

        # 推断优先级
        priority = "high" if difficulty == "hard" else "medium"

        # 估算学习时长
        hours_map = {"easy": 4, "medium": 7, "hard": 10}
        estimated_hours = hours_map.get(difficulty, 7)

        return StudyPlan(
            week=week,
            title=title,
            prerequisites=prerequisites,
            priority=priority,
            topics=topics,
            estimated_hours=estimated_hours
        )

    def _infer_prerequisites(self, week: int, all_topics: List[str]) -> List[str]:
        """推断前置知识（简化版）"""
        prereq_map = {
            1: [],
            2: ["变量"],
            3: ["变量", "if/else"],
            4: ["变量", "循环"],
            5: ["变量", "文件"],
            6: ["函数", "文件"],
            7: ["异常处理"],
            8: ["异常处理", "函数"],
            9: ["测试"],
            10: ["JSON", "文件"],
            11: ["dataclass", "类型提示"],
            12: ["argparse", "logging"],
            13: ["agent team", "review checklist"],
            14: ["所有前置知识"],
        }
        return [p for p in prereq_map.get(week, []) if p in all_topics]


def generate_study_plans(notes_dir: str, output: str) -> int:
    """为所有笔记生成学习计划（agent team 流水线）"""
    logger.info("开始生成学习计划")

    notes_path = Path(notes_dir)
    if not notes_path.exists():
        logger.error(f"笔记目录不存在：{notes_dir}")
        print(f"错误：笔记目录不存在：{notes_dir}")
        return 1

    # 收集所有笔记文件
    note_files = sorted(notes_path.glob("week*.md"))

    if not note_files:
        logger.error(f"未找到笔记文件：{notes_dir}")
        print(f"错误：未找到笔记文件（week*.md）")
        return 1

    # 提取所有主题
    all_topics = [
        "变量", "if/else", "循环", "函数", "文件",
        "异常处理", "测试", "JSON", "dataclass", "类型提示",
        "argparse", "logging", "agent team", "review checklist"
    ]

    # 创建 agent
    reader = ReaderAgent()
    writer = WriterAgent()

    # 为每个笔记生成计划
    plans = []
    for note_file in note_files:
        try:
            analysis = reader.read_note(note_file)
            if analysis:
                plan = writer.create_plan(analysis, all_topics)
                plans.append(plan)
        except Exception as e:
            logger.error(f"处理 {note_file.name} 失败：{e}")
            continue

    # 导出为 JSON
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plans_dict = [plan.to_dict() for plan in plans]
    output_path.write_text(
        json.dumps(plans_dict, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    logger.info(f"✓ 学习计划已生成：{output_path}")
    logger.info(f"  共 {len(plans)} 周")
    total_hours = sum(p.estimated_hours for p in plans)
    logger.info(f"  总时长：{total_hours} 小时")

    print(f"✓ 学习计划已生成：{output_path}")
    print(f"  共 {len(plans)} 周，总时长：{total_hours} 小时")

    return 0


# =====================
# 核心功能函数
# =====================

def add_note(notes: List[Note], content: str, tags: List[str] = None) -> Note:
    """添加学习笔记"""
    note = Note(
        id=generate_id(),
        content=content,
        tags=tags or [],
        created_at=datetime.now().strftime("%Y-%m-%d"),
        status=NoteStatus.DRAFT
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
    elif format == "markdown":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# 学习笔记\n\n")
            for note in notes:
                status_icon = {
                    NoteStatus.DRAFT: "○",
                    NoteStatus.PUBLISHED: "✓",
                    NoteStatus.ARCHIVED: "◉"
                }[note.status]

                f.write(f"## {status_icon} {note.content[:50]}...\n\n")
                f.write(f"**ID**: {note.id}\n\n")
                f.write(f"**创建时间**: {note.created_at}\n\n")
                if note.tags:
                    f.write(f"**标签**: {', '.join(note.tags)}\n\n")
                f.write(f"**内容**: {note.content}\n\n")
                f.write("---\n\n")


# =====================
# CLI 子命令处理函数
# =====================

def cmd_add(args):
    """添加学习笔记"""
    logger.info(f"添加笔记：{args.content}")

    try:
        notes = load_notes()
        note = add_note(notes, args.content, args.tags)
        save_notes(notes)

        logger.info(f"笔记添加成功：{note.id}")
        print(f"✓ 笔记已添加：{note.id}")
        print(f"  内容：{note.content[:50]}...")
        return 0
    except Exception as e:
        logger.error(f"添加笔记失败：{e}")
        print(f"错误：添加笔记失败 - {e}")
        return 1


def cmd_list(args):
    """列出笔记"""
    logger.info("列出笔记")

    try:
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
    except Exception as e:
        logger.error(f"列出笔记失败：{e}")
        print(f"错误：列出笔记失败 - {e}")
        return 1


def cmd_search(args):
    """搜索笔记"""
    logger.info(f"搜索笔记：{args.keyword}")

    try:
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
    except Exception as e:
        logger.error(f"搜索笔记失败：{e}")
        print(f"错误：搜索笔记失败 - {e}")
        return 1


def cmd_export(args):
    """导出笔记"""
    logger.info(f"导出笔记：{args.format}")

    try:
        notes = load_notes()
        export_notes(notes, args.output, args.format)

        logger.info(f"笔记已导出到 {args.output}")
        print(f"✓ 已导出 {len(notes)} 条笔记到 {args.output}")
        return 0
    except Exception as e:
        logger.error(f"导出笔记失败：{e}")
        print(f"错误：导出笔记失败 - {e}")
        return 1


def cmd_stats(args):
    """显示统计信息"""
    logger.info("生成统计")

    try:
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
    except Exception as e:
        logger.error(f"生成统计失败：{e}")
        print(f"错误：生成统计失败 - {e}")
        return 1


def cmd_plan_generate(args):
    """生成学习计划"""
    return generate_study_plans(args.notes_dir, args.output)


def cmd_plan_show(args):
    """显示学习计划"""
    logger.info(f"显示学习计划：Week {args.week}")

    try:
        if not PLAN_FILE.exists():
            print("错误：学习计划不存在，请先运行 'pyhelper plan generate'")
            return 1

        with open(PLAN_FILE, "r", encoding="utf-8") as f:
            plans = json.load(f)

        # 查找指定周
        if args.week:
            plan = next((p for p in plans if p["week"] == args.week), None)
            if not plan:
                print(f"错误：未找到 Week {args.week} 的学习计划")
                return 1

            print(f"学习计划：Week {plan['week']} - {plan['title']}")
            print("=" * 60)
            print(f"主题：{', '.join(plan['topics'])}")
            print(f"前置知识：{', '.join(plan['prerequisites']) if plan['prerequisites'] else '无'}")
            print(f"优先级：{plan['priority']}")
            print(f"预估时长：{plan['estimated_hours']} 小时")
        else:
            # 显示所有计划
            print("学习计划：")
            print("=" * 60)
            for plan in plans:
                print(f"Week {plan['week']}: {plan['title']}")
                print(f"  主题：{', '.join(plan['topics'])}")
                print(f"  时长：{plan['estimated_hours']} 小时")
                print(f"  优先级：{plan['priority']}")

        return 0
    except Exception as e:
        logger.error(f"显示学习计划失败：{e}")
        print(f"错误：显示学习计划失败 - {e}")
        return 1


# =====================
# 主入口（Week 12: argparse）
# =====================

def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="PyHelper v1.0.0 - 命令行学习助手",
        epilog="示例：python 14_pyhelper_v1.py add '今天学了代码收敛'"
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
    export_parser.add_argument(
        "--format",
        choices=["json", "csv", "markdown"],
        default="json",
        help="导出格式"
    )
    export_parser.set_defaults(func=cmd_export)

    # stats 子命令
    stats_parser = subparsers.add_parser("stats", help="统计信息")
    stats_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    stats_parser.set_defaults(func=cmd_stats)

    # plan 子命令
    plan_parser = subparsers.add_parser("plan", help="学习计划管理")
    plan_subparsers = plan_parser.add_subparsers(dest="plan_command", help="计划子命令")

    # plan generate
    generate_parser = plan_subparsers.add_parser("generate", help="生成学习计划")
    generate_parser.add_argument("--notes-dir", "-n", default="notes", help="笔记目录")
    generate_parser.add_argument("--output", "-o", default=str(PLAN_FILE), help="输出文件")
    generate_parser.set_defaults(func=cmd_plan_generate)

    # plan show
    show_parser = plan_subparsers.add_parser("show", help="显示学习计划")
    show_parser.add_argument("--week", "-w", type=int, help="周次")
    show_parser.set_defaults(func=cmd_plan_show)

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


# =====================
# 总结
# =====================

"""
PyHelper v1.0.0 - 从 Week 01 到 Week 14 的完整演进

核心知识整合：
  - Week 01: print(), 字符串
  - Week 02: input(), if/else
  - Week 03: 函数, 返回值
  - Week 04: 列表, 字典, 遍历
  - Week 05: 文件读写, pathlib
  - Week 06: try/except, 异常处理
  - Week 07: 模块化, import
  - Week 08: pytest, 测试
  - Week 09: 字符串方法, 正则
  - Week 10: JSON, 序列化
  - Week 11: dataclass, 类型提示
  - Week 12: argparse, logging
  - Week 13: agent team, review
  - Week 14: 代码收敛, 发布

技术栈：
  - 数据模型：dataclass (Note, NoteStatus, StudyPlan)
  - 存储：JSON (notes.json, plan.json)
  - CLI：argparse (子命令、参数、互斥组)
  - 日志：logging (文件、级别、格式)
  - 异常：try/except (优雅降级)
  - Agent：reader/writer 协作

命令清单：
  - pyhelper add "内容" [--tags ...]
  - pyhelper list [--pending|--published]
  - pyhelper search "关键词"
  - pyhelper export --format json --output file.json
  - pyhelper stats [--json]
  - pyhelper plan generate [--notes-dir dir] [--output file]
  - pyhelper plan show [--week N]

目录结构：
  ~/.pyhelper/
    ├── notes.json       # 笔记数据
    ├── plan.json        # 学习计划
    └── pyhelper.log     # 日志文件

这是全书的终点，也是你作为开发者的起点。
继续探索，保持好奇！
"""
