"""
示例：防御性数据编程——处理各种边界情况

本示例演示：
1. 捕获 JSONDecodeError
2. 数据验证和清洗
3. Schema 验证的概念
4. 优雅降级策略

运行方式：python3 chapters/week_10/examples/05_defensive_programming.py
预期输出：展示各种错误处理场景
"""

import json
from pathlib import Path
import tempfile


# =====================
# 1. 安全的导入函数
# =====================

def safe_import_books(filepath):
    """
    安全地导入书单，处理各种错误情况

    防御性编程的几个层次：
    1. 前置检查：文件是否存在？
    2. 异常捕获：用 try/except 捕获特定的 JSON 解析错误
    3. 数据验证：解析成功后，验证数据结构是否符合预期
    4. 优雅降级：遇到问题时返回空列表，而不是崩溃
    """
    filepath = Path(filepath)

    # 前置检查
    if not filepath.exists():
        print(f"错误: 文件 {filepath} 不存在")
        return []

    # 检查文件大小（防止读取过大的文件）
    max_size = 10 * 1024 * 1024  # 10MB
    if filepath.stat().st_size > max_size:
        print(f"错误: 文件太大 ({filepath.stat().st_size} 字节)")
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            books = json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误: JSON 格式不正确 - {e}")
        return []
    except UnicodeDecodeError as e:
        print(f"错误: 文件编码问题 - {e}")
        return []
    except Exception as e:
        print(f"错误: 未知错误 - {e}")
        return []

    # 数据结构验证
    if not isinstance(books, list):
        print("错误: JSON 根元素必须是数组")
        return []

    # 过滤掉无效的记录
    valid_books = []
    for i, book in enumerate(books):
        if not isinstance(book, dict):
            print(f"警告: 第 {i} 项不是字典，已跳过")
            continue
        if "title" not in book:
            print(f"警告: 第 {i} 项缺少 title 字段，已跳过")
            continue
        valid_books.append(book)

    print(f"成功导入 {len(valid_books)} 本书（共 {len(books)} 项）")
    return valid_books


# =====================
# 2. Schema 验证
# =====================

def validate_book_schema(book):
    """
    验证单条书记录是否符合 Schema

    Schema 定义：
    - title: 字符串，必填
    - author: 字符串，可选
    - rating: 整数，1-5，可选
    - tags: 字符串列表，可选
    """
    errors = []

    # 检查类型
    if not isinstance(book, dict):
        return ["记录必须是字典"]

    # 检查必填字段
    if "title" not in book:
        errors.append("缺少必填字段: title")
    elif not isinstance(book["title"], str):
        errors.append("title 必须是字符串")
    elif not book["title"].strip():
        errors.append("title 不能为空")

    # 检查可选字段类型
    if "author" in book and not isinstance(book["author"], str):
        errors.append("author 必须是字符串")

    if "rating" in book:
        if not isinstance(book["rating"], int):
            errors.append("rating 必须是整数")
        elif not 1 <= book["rating"] <= 5:
            errors.append("rating 必须在 1-5 之间")

    if "tags" in book:
        if not isinstance(book["tags"], list):
            errors.append("tags 必须是列表")
        else:
            for tag in book["tags"]:
                if not isinstance(tag, str):
                    errors.append(f"tags 中的 '{tag}' 不是字符串")

    return errors


def import_with_schema_validation(filepath):
    """
    导入书单并进行 Schema 验证
    """
    filepath = Path(filepath)

    if not filepath.exists():
        print(f"错误: 文件不存在")
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            books = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return []

    if not isinstance(books, list):
        print("错误: 根元素必须是列表")
        return []

    valid_books = []
    for i, book in enumerate(books):
        errors = validate_book_schema(book)
        if errors:
            print(f"第 {i} 项验证失败: {'; '.join(errors)}")
        else:
            valid_books.append(book)

    print(f"验证通过: {len(valid_books)}/{len(books)}")
    return valid_books


# =====================
# 3. 数据清洗
# =====================

def clean_book_data(book):
    """
    清洗单条书记录

    - 去除字符串字段的前后空格
    - 统一 rating 为整数
    - 确保 tags 是列表
    - 移除未知字段
    """
    cleaned = {}

    # 清洗 title（必填）
    if "title" in book and isinstance(book["title"], str):
        cleaned["title"] = book["title"].strip()

    # 清洗 author
    if "author" in book:
        if isinstance(book["author"], str):
            cleaned["author"] = book["author"].strip()
        else:
            cleaned["author"] = str(book["author"])

    # 清洗 rating
    if "rating" in book:
        try:
            rating = int(book["rating"])
            cleaned["rating"] = max(1, min(5, rating))  # 限制在 1-5
        except (ValueError, TypeError):
            pass  # 跳过无效的 rating

    # 清洗 tags
    if "tags" in book:
        if isinstance(book["tags"], list):
            cleaned["tags"] = [str(t).strip() for t in book["tags"] if t]
        elif isinstance(book["tags"], str):
            # 如果是字符串，按逗号分割
            cleaned["tags"] = [t.strip() for t in book["tags"].split(",") if t.strip()]

    return cleaned


def import_and_clean(filepath):
    """
    导入并清洗数据
    """
    raw_books = safe_import_books(filepath)
    cleaned_books = [clean_book_data(book) for book in raw_books]
    # 过滤掉没有 title 的记录
    cleaned_books = [b for b in cleaned_books if "title" in b]
    print(f"清洗后: {len(cleaned_books)} 本有效书籍")
    return cleaned_books


# =====================
# 4. 演示
# =====================

if __name__ == "__main__":
    print("=== 防御性数据编程演示 ===\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        # 场景 1：正常的 JSON
        print("--- 场景 1：正常的 JSON ---")
        normal_file = Path(tmpdir) / "normal.json"
        normal_data = [
            {"title": "Python 入门", "author": "张三", "rating": 5},
            {"title": "Java 基础", "author": "李四", "rating": 4},
        ]
        with open(normal_file, "w", encoding="utf-8") as f:
            json.dump(normal_data, f)

        result = safe_import_books(normal_file)
        print(f"导入结果: {len(result)} 本书\n")

        # 场景 2：损坏的 JSON
        print("--- 场景 2：损坏的 JSON ---")
        broken_file = Path(tmpdir) / "broken.json"
        broken_content = '''[
  {"title": "书 1", "author": "作者 1"},
  {"title": "书 2", "author": "作者 2"
]'''
        broken_file.write_text(broken_content)

        result = safe_import_books(broken_file)
        print(f"导入结果: {len(result)} 本书（应该为 0，因为 JSON 损坏）\n")

        # 场景 3：包含无效数据的 JSON
        print("--- 场景 3：包含无效数据的 JSON ---")
        mixed_file = Path(tmpdir) / "mixed.json"
        mixed_data = [
            {"title": "有效书籍", "author": "作者 A", "rating": 5},
            {"author": "缺少 title"},  # 无效：缺少 title
            "这不是字典",  # 无效：不是字典
            {"title": "", "author": "空标题"},  # 有效（但 title 为空）
            {"title": "有效书籍 2", "rating": 3},
        ]
        with open(mixed_file, "w", encoding="utf-8") as f:
            json.dump(mixed_data, f)

        result = safe_import_books(mixed_file)
        print(f"导入结果: {len(result)} 本书\n")

        # 场景 4：Schema 验证
        print("--- 场景 4：Schema 验证 ---")
        schema_file = Path(tmpdir) / "schema_test.json"
        schema_data = [
            {"title": "有效书籍", "rating": 5},
            {"title": "rating 类型错误", "rating": "五星"},  # rating 应该是整数
            {"title": "rating 超出范围", "rating": 10},  # rating 应该在 1-5
            {"author": "缺少 title"},  # 缺少 title
            {"title": "tags 类型错误", "tags": "Python, 编程"},  # tags 应该是列表
        ]
        with open(schema_file, "w", encoding="utf-8") as f:
            json.dump(schema_data, f)

        result = import_with_schema_validation(schema_file)
        print(f"通过验证: {len(result)} 本书\n")

        # 场景 5：数据清洗
        print("--- 场景 5：数据清洗 ---")
        dirty_file = Path(tmpdir) / "dirty.json"
        dirty_data = [
            {"title": "  有空格的书  ", "author": "  作者  ", "rating": "5"},
            {"title": "tags 是字符串", "tags": "Python, 编程, 学习"},
            {"title": "rating 超出范围", "rating": 10},
            {"no_title": "这条记录会被过滤"},
        ]
        with open(dirty_file, "w", encoding="utf-8") as f:
            json.dump(dirty_data, f)

        print("原始数据:")
        for book in dirty_data:
            print(f"  {book}")

        print("\n清洗后:")
        result = import_and_clean(dirty_file)
        for book in result:
            print(f"  {book}")

        # 场景 6：不存在的文件
        print("\n--- 场景 6：不存在的文件 ---")
        result = safe_import_books(Path(tmpdir) / "not_exist.json")
        print(f"导入结果: {len(result)} 本书\n")

    print("=" * 50)
    print("防御性编程要点：")
    print("1. 前置检查：文件是否存在、大小是否合理")
    print("2. 异常捕获：捕获特定的异常类型")
    print("3. 数据验证：验证数据结构和类型")
    print("4. 数据清洗：清理和标准化数据")
    print("5. 优雅降级：出错时返回默认值，不崩溃")
