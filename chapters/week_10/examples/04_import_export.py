"""
示例：数据导入导出——让数据自由流动

本示例演示：
1. 设计导入导出接口
2. 支持多种格式（JSON、CSV、文本）
3. 处理编码问题
4. 数据版本兼容性处理

运行方式：python3 chapters/week_10/examples/04_import_export.py
预期输出：展示数据导入导出的完整流程
"""

import json
import csv
from pathlib import Path
import tempfile


# =====================
# 1. 基础导入导出功能
# =====================

def export_books(books, filepath, format="json"):
    """
    导出书单到文件

    Args:
        books: 书单列表，每个元素是字典
        filepath: 输出文件路径
        format: 导出格式，支持 "json" 或 "csv"

    Raises:
        ValueError: 如果格式不支持
    """
    filepath = Path(filepath)

    if format == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(books, f, indent=2, ensure_ascii=False)

    elif format == "csv":
        # CSV 导出（简化版，只导出基本字段）
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            if books:
                # 使用第一条记录的键作为表头
                fieldnames = list(books[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(books)

    elif format == "txt":
        # 导出为易读的文本格式
        with open(filepath, "w", encoding="utf-8") as f:
            for book in books:
                f.write(f"书名: {book.get('title', '未知')}\n")
                f.write(f"作者: {book.get('author', '未知')}\n")
                f.write(f"评分: {book.get('rating', 'N/A')}\n")
                f.write("-" * 40 + "\n")

    else:
        raise ValueError(f"不支持的格式: {format}")

    print(f"✓ 已导出 {len(books)} 本书到 {filepath} (格式: {format})")


def import_books(filepath):
    """
    从 JSON 文件导入书单

    Args:
        filepath: JSON 文件路径

    Returns:
        书单列表

    Raises:
        FileNotFoundError: 如果文件不存在
        ValueError: 如果 JSON 格式不正确
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        books = json.load(f)

    # 简单的数据验证
    if not isinstance(books, list):
        raise ValueError("JSON 根元素必须是数组")

    print(f"✓ 已导入 {len(books)} 本书")
    return books


# =====================
# 2. 处理编码问题
# =====================

def import_with_encoding_fallback(filepath):
    """
    更健壮的导入函数，自动处理编码

    尝试多种编码读取文件，处理不同系统生成的文件
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    # 尝试多种编码
    encodings = ["utf-8", "utf-8-sig", "gbk", "latin-1"]
    content = None

    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
            print(f"✓ 成功用 {enc} 编码读取")
            break
        except UnicodeDecodeError:
            continue
    else:
        raise UnicodeDecodeError(f"无法解码文件，尝试了: {encodings}")

    # 解析 JSON
    return json.loads(content)


# =====================
# 3. 数据版本兼容性
# =====================

def migrate_book_data(book, from_version=1):
    """
    将旧版本数据迁移到最新版本

    数据迁移示例：
    - v1: 只有 title 和 author
    - v2: 添加了 rating 字段
    - v3: 添加了 tags 字段
    """
    # v1 → v2：添加 rating 字段，默认为 0
    if from_version < 2:
        book.setdefault("rating", 0)

    # v2 → v3：添加 tags 字段，默认为空列表
    if from_version < 3:
        book.setdefault("tags", [])

    # v3 → v4：添加 status 字段，根据 finished 推断
    if from_version < 4:
        if "finished" in book:
            book["status"] = "finished" if book["finished"] else "reading"
        else:
            book.setdefault("status", "unread")

    return book


def import_with_migration(filepath):
    """
    导入书单，自动进行数据迁移

    支持带版本信息的包装格式
    """
    data = import_with_encoding_fallback(filepath)

    # 检查是否是包装格式（有 _metadata 和 data）
    if isinstance(data, dict) and "_metadata" in data and "data" in data:
        metadata = data["_metadata"]
        books = data["data"]
        version = metadata.get("version", "1.0")
        from_version = int(version.split(".")[0])
        print(f"检测到版本 {version} 的数据")
    else:
        # 旧格式，假设是 v1
        books = data
        from_version = 1
        print("检测到旧格式数据 (v1)")

    # 迁移数据
    migrated_books = [migrate_book_data(book.copy(), from_version) for book in books]

    if from_version < 4:
        print(f"✓ 已迁移 {len(migrated_books)} 条数据到最新版本")

    return migrated_books


# =====================
# 4. 演示
# =====================

if __name__ == "__main__":
    print("=== 数据导入导出演示 ===\n")

    # 测试数据
    sample_books = [
        {
            "title": "Python 编程：从入门到实践",
            "author": "Eric Matthes",
            "rating": 5,
            "tags": ["Python", "入门"],
            "finished": True
        },
        {
            "title": "流畅的 Python",
            "author": "Luciano Ramalho",
            "rating": 5,
            "tags": ["Python", "进阶"],
            "finished": False
        },
        {
            "title": "Python 标准库",
            "author": "Doug Hellmann",
            "rating": 4,
            "tags": ["Python", "参考"],
            "finished": False
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. 导出为 JSON
        print("--- 1. 导出为 JSON ---")
        json_file = Path(tmpdir) / "books.json"
        export_books(sample_books, json_file, format="json")
        print(f"文件内容预览:")
        content = json_file.read_text()
        print(content[:300] + "...\n")

        # 2. 导出为 CSV
        print("--- 2. 导出为 CSV ---")
        csv_file = Path(tmpdir) / "books.csv"
        export_books(sample_books, csv_file, format="csv")
        print(f"文件内容:")
        print(csv_file.read_text())

        # 3. 导出为文本
        print("--- 3. 导出为文本 ---")
        txt_file = Path(tmpdir) / "books.txt"
        export_books(sample_books, txt_file, format="txt")
        print(f"文件内容:")
        print(txt_file.read_text())

        # 4. 导入 JSON
        print("--- 4. 从 JSON 导入 ---")
        imported = import_books(json_file)
        print(f"成功导入 {len(imported)} 本书")
        print(f"第一本书: {imported[0]['title']}\n")

        # 5. 数据迁移演示
        print("--- 5. 数据迁移演示 ---")

        # 创建旧格式数据
        old_books = [
            {"title": "旧书 1", "author": "作者 A"},  # v1 格式
            {"title": "旧书 2", "author": "作者 B", "rating": 3},  # v2 格式
        ]

        old_file = Path(tmpdir) / "old_books.json"
        with open(old_file, "w", encoding="utf-8") as f:
            json.dump(old_books, f)

        print("旧格式数据:")
        for book in old_books:
            print(f"  {book}")

        print("\n导入并迁移后:")
        migrated = import_with_migration(old_file)
        for book in migrated:
            print(f"  {book}")

        # 6. 带版本信息的包装格式
        print("\n--- 6. 带版本信息的包装格式 ---")
        wrapped_data = {
            "_metadata": {
                "version": "2.0",
                "created_at": "2026-02-09T10:00:00",
                "item_count": len(sample_books)
            },
            "data": sample_books
        }

        wrapped_file = Path(tmpdir) / "wrapped_books.json"
        with open(wrapped_file, "w", encoding="utf-8") as f:
            json.dump(wrapped_data, f, indent=2, ensure_ascii=False)

        print("导入包装格式:")
        imported_wrapped = import_with_migration(wrapped_file)
        print(f"成功导入 {len(imported_wrapped)} 本书\n")

    print("=" * 50)
    print("导入导出设计要点：")
    print("1. 接口清晰：export_* / import_* 函数")
    print("2. 支持多种格式：JSON、CSV、文本")
    print("3. 处理编码：自动检测和回退")
    print("4. 版本兼容：数据迁移函数")
    print("5. 数据验证：检查格式和类型")
