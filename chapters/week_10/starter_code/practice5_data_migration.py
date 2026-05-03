"""Week 10 练习 5：简单数据迁移工具。"""

import datetime
import json
from pathlib import Path


def detect_version(data):
    """检测数据版本，缺省按 v1 处理。"""
    if not isinstance(data, dict):
        return 0
    return int(data.get("version", 1))


def migrate_v1_to_v2(old_data):
    """把 v1 书单迁移为 v2 格式，并返回 (新数据, 报告)。"""
    books = []
    report = []
    today = datetime.date.today().isoformat()

    for item in old_data.get("books", []):
        books.append(
            {
                "title": item.get("name", ""),
                "author": item.get("writer", ""),
                "rating": 0,
                "tags": [],
                "added_date": today,
            }
        )
        report.append("name -> title, writer -> author")

    return {"books": books, "version": 2, "total_count": len(books)}, report


def migrate_data(input_path, output_path):
    """读取 JSON 数据，迁移到 v2 并写出。"""
    with Path(input_path).open("r", encoding="utf-8") as file:
        data = json.load(file)

    if detect_version(data) == 2:
        migrated, report = data, ["already version 2"]
    else:
        migrated, report = migrate_v1_to_v2(data)

    with Path(output_path).open("w", encoding="utf-8") as file:
        json.dump(migrated, file, ensure_ascii=False, indent=2)

    return migrated, report
