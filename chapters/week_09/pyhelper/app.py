"""Week 09 PyHelper: search and filters."""

try:
    from .records import filter_by_date_range, filter_by_keyword
    from .text_utils import extract_tags
except ImportError:
    from records import filter_by_date_range, filter_by_keyword
    from text_utils import extract_tags


def demo_records() -> list[dict]:
    return [
        {"date": "2026-05-10", "content": "学习正则表达式 #regex"},
        {"date": "2026-05-11", "content": "用关键词搜索 PyHelper 笔记 #search"},
    ]


def main() -> None:
    records = demo_records()
    print("搜索 PyHelper：", filter_by_keyword(records, "pyhelper"))
    print("日期过滤：", filter_by_date_range(records, "2026-05-11", "2026-05-11"))
    print("标签：", extract_tags(records[0]["content"]))


if __name__ == "__main__":
    main()
