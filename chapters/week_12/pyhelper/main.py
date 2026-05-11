import argparse
from pathlib import Path
try:
    from .encouragement import advice_for_mood, build_welcome
    from .records import add_record, list_records, search_records, stats
    from .storage import export_json, load_records, save_records
except ImportError:
    from encouragement import advice_for_mood, build_welcome
    from records import add_record, list_records, search_records, stats
    from storage import export_json, load_records, save_records

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pyhelper", description="PyHelper 命令行学习助手")
    sub = parser.add_subparsers(dest="command")
    add = sub.add_parser("add", help="新增学习记录")
    add.add_argument("content")
    add.add_argument("--date", required=True)
    ls = sub.add_parser("list", help="列出学习记录")
    search = sub.add_parser("search", help="搜索学习记录")
    search.add_argument("keyword")
    search.add_argument("--start")
    search.add_argument("--end")
    sub.add_parser("export", help="导出 JSON")
    sub.add_parser("stats", help="查看统计")
    advice = sub.add_parser("advice", help="按心情给建议")
    advice.add_argument("mood")
    return parser

def run(argv: list[str] | None = None) -> str:
    args = build_parser().parse_args(argv)
    records = load_records()
    if args.command == "add":
        if not add_record(records, args.date, args.content):
            return "日期或内容不合法。"
        save_records(records)
        return "已记录。"
    if args.command == "list":
        return "\n".join(list_records(records)) or "暂无记录。"
    if args.command == "search":
        return "\n".join(list_records(search_records(records, args.keyword, args.start, args.end))) or "没有匹配记录。"
    if args.command == "export":
        return export_json(records)
    if args.command == "stats":
        return stats(records)
    if args.command == "advice":
        return advice_for_mood(args.mood)
    return build_welcome("同学")

def main() -> None:
    print(run())

if __name__ == "__main__":
    main()
