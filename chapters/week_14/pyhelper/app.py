"""Week 14 PyHelper v1.0: final CLI package."""

import argparse
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

DATA_FILE = Path(os.environ.get("PYHELPER_DATA_FILE", Path.home() / ".pyhelper_v1_records.json"))


@dataclass
class Note:
    content: str
    date: str = field(default_factory=lambda: date.today().isoformat())
    tags: list[str] = field(default_factory=list)
    reviewed: bool = False


def load_notes() -> list[Note]:
    if not DATA_FILE.exists():
        return []
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [Note(**item) for item in raw]


def save_notes(notes: list[Note]) -> None:
    DATA_FILE.write_text(json.dumps([asdict(n) for n in notes], ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_add(args: argparse.Namespace) -> int:
    notes = load_notes()
    notes.append(Note(content=args.content, tags=args.tag or []))
    save_notes(notes)
    print("PyHelper: 已添加")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    for i, note in enumerate(load_notes(), start=1):
        tags = " ".join("#" + t for t in note.tags)
        print(f"{i}. {note.date} {note.content} {tags}".strip())
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    for note in load_notes():
        if args.keyword.lower() in note.content.lower():
            print(f"{note.date}: {note.content}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    notes = load_notes()
    reviewed = sum(1 for note in notes if note.reviewed)
    print(f"总记录：{len(notes)}；已审查：{reviewed}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pyhelper", description="PyHelper v1.0 学习助手")
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add")
    p_add.add_argument("content")
    p_add.add_argument("--tag", action="append")
    p_add.set_defaults(func=cmd_add)
    p_list = sub.add_parser("list")
    p_list.set_defaults(func=cmd_list)
    p_search = sub.add_parser("search")
    p_search.add_argument("keyword")
    p_search.set_defaults(func=cmd_search)
    p_stats = sub.add_parser("stats")
    p_stats.set_defaults(func=cmd_stats)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
