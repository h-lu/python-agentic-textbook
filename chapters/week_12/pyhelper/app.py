"""Week 12 PyHelper: argparse CLI."""

import argparse
import json
import os
from pathlib import Path

DATA_FILE = Path(os.environ.get("PYHELPER_DATA_FILE", Path.home() / ".pyhelper_week12_records.json"))


def load_records() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_records(records: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_add(args: argparse.Namespace) -> int:
    records = load_records()
    records.append({"date": args.date, "content": args.content})
    save_records(records)
    print("已添加学习记录")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    for item in load_records():
        print(f"{item['date']}: {item['content']}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    for item in load_records():
        if args.keyword in item["content"]:
            print(f"{item['date']}: {item['content']}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    print(f"记录数：{len(load_records())}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pyhelper", description="PyHelper 学习记录 CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add")
    p_add.add_argument("content")
    p_add.add_argument("--date", default="2026-05-11")
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
