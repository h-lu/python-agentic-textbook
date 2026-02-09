"""
text_utils.py - PyHelper 文本处理模块

职责：负责笔记的搜索、过滤和标签提取

功能：
- search_notes()：按关键词搜索笔记内容
- filter_by_date()：按日期范围过滤笔记
- extract_tags()：用正则表达式从笔记中提取 #标签
- format_note_summary()：格式化笔记摘要

运行方式（测试）：
  python3 text_utils.py

导入方式：
  from text_utils import search_notes, filter_by_date, extract_tags
"""

import re
from datetime import datetime


def search_notes(notes, keyword):
    """按关键词搜索笔记内容

    使用字符串的 lower() 和 in 操作实现大小写不敏感的搜索。

    Args:
        notes: 笔记列表，每个笔记是字典，包含 'content' 和 'date'
        keyword: 搜索关键词

    Returns:
        匹配的笔记列表
    """
    # 边界检查：如果关键词是空字符串，直接返回空列表
    if not keyword or not keyword.strip():
        return []

    keyword = keyword.lower().strip()
    results = []

    for note in notes:
        content = note.get("content", "").lower()
        if keyword in content:
            results.append(note)

    return results


def filter_by_date(notes, start_date=None, end_date=None):
    """按日期范围过滤笔记

    Args:
        notes: 笔记列表
        start_date: 开始日期，格式 'YYYY-MM-DD'
        end_date: 结束日期，格式 'YYYY-MM-DD'

    Returns:
        在日期范围内的笔记列表
    """
    results = []

    for note in notes:
        note_date = note.get("date", "")

        # 解析笔记日期
        try:
            note_dt = datetime.strptime(note_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            continue  # 跳过日期格式不对的笔记

        # 检查是否在范围内
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                if note_dt < start_dt:
                    continue
            except ValueError:
                continue  # 开始日期格式错误，跳过

        if end_date:
            try:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                if note_dt > end_dt:
                    continue
            except ValueError:
                continue  # 结束日期格式错误，跳过

        results.append(note)

    return results


def extract_tags(content):
    """从笔记内容中提取 #标签

    标签格式：#单词（可以包含中文、字母、数字、下划线）
    例如：#Python #学习笔记 #week_10

    使用正则表达式匹配 # 开头的标签。

    Args:
        content: 笔记内容字符串

    Returns:
        标签列表（不含 # 符号）
    """
    if not content:
        return []

    # 正则匹配 #开头的标签
    # \w 匹配字母数字下划线，\u4e00-\u9fff 匹配中文字符
    pattern = r"#([\w\u4e00-\u9fff]+)"
    tags = re.findall(pattern, content)

    return tags


def format_note_summary(note):
    """格式化笔记摘要，用于列表显示

    Args:
        note: 笔记字典，包含 'date' 和 'content'

    Returns:
        格式化后的摘要字符串
    """
    date = note.get("date", "未知日期")
    content = note.get("content", "")

    # 截取前 50 个字符作为摘要
    summary = content[:50] + "..." if len(content) > 50 else content

    # 提取标签
    tags = extract_tags(content)
    tag_str = " ".join([f"#{t}" for t in tags]) if tags else ""

    return f"[{date}] {summary} {tag_str}"


# =====================
# 测试代码
# =====================

if __name__ == "__main__":
    print("=== 测试 text_utils 模块 ===")

    # 测试数据
    test_notes = [
        {"date": "2026-02-09", "content": "学了 JSON 和序列化 #Python #学习"},
        {"date": "2026-02-08", "content": "复习了字符串方法 #Python"},
        {"date": "2026-02-07", "content": "了解了数据导入导出 #JSON"},
        {"date": "2026-02-01", "content": "开始学习 Python #入门"},
    ]

    # 测试搜索
    print("\n--- 测试 search_notes ---")
    results = search_notes(test_notes, "JSON")
    print(f"搜索 'JSON': 找到 {len(results)} 条")
    for note in results:
        print(f"  - {format_note_summary(note)}")

    # 测试大小写不敏感
    results = search_notes(test_notes, "python")
    print(f"搜索 'python' (小写): 找到 {len(results)} 条")

    # 测试空关键词
    results = search_notes(test_notes, "")
    print(f"搜索空字符串: 返回 {len(results)} 条 (应该是 0)")

    results = search_notes(test_notes, "   ")
    print(f"搜索空格: 返回 {len(results)} 条 (应该是 0)")

    # 测试日期过滤
    print("\n--- 测试 filter_by_date ---")
    results = filter_by_date(test_notes, "2026-02-07", "2026-02-08")
    print(f"过滤 2026-02-07 到 2026-02-08: 找到 {len(results)} 条")
    for note in results:
        print(f"  - {format_note_summary(note)}")

    # 测试只指定开始日期
    results = filter_by_date(test_notes, start_date="2026-02-08")
    print(f"过滤 2026-02-08 之后: 找到 {len(results)} 条")

    # 测试只指定结束日期
    results = filter_by_date(test_notes, end_date="2026-02-05")
    print(f"过滤 2026-02-05 之前: 找到 {len(results)} 条")

    # 测试标签提取
    print("\n--- 测试 extract_tags ---")
    content = "今天学了 #Python 和 #JSON，感觉 #很棒"
    tags = extract_tags(content)
    print(f"内容: {content}")
    print(f"提取的标签: {tags}")

    # 测试英文标签
    content = "Working on #Python project with #json"
    tags = extract_tags(content)
    print(f"内容: {content}")
    print(f"提取的标签: {tags}")

    # 测试空内容
    tags = extract_tags("")
    print(f"空内容提取标签: {tags}")

    # 测试格式化摘要
    print("\n--- 测试 format_note_summary ---")
    long_note = {
        "date": "2026-02-09",
        "content": "今天学习了很多内容，包括 JSON、序列化、数据导入导出等等 #Python #学习笔记"
    }
    print(f"长笔记摘要: {format_note_summary(long_note)}")

    short_note = {
        "date": "2026-02-08",
        "content": "复习"
    }
    print(f"短笔记摘要: {format_note_summary(short_note)}")

    print("\n✓ 所有测试通过！")
