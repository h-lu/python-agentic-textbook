"""Week 10 练习 4：防御性 JSON 数据加载。"""

import json
from pathlib import Path


def safe_load_json(filepath):
    """尝试多种编码加载 JSON，失败返回 None。"""
    path = Path(filepath)
    if not path.exists():
        return None

    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            with path.open("r", encoding=encoding) as file:
                data = json.load(file)
            return data if isinstance(data, (dict, list)) else None
        except UnicodeDecodeError:
            continue
        except (OSError, json.JSONDecodeError):
            return None

    return None


def validate_book_data(data):
    """验证单本书数据，返回 (是否有效, 错误列表)。"""
    errors = []
    if not isinstance(data, dict):
        return False, ["不是字典类型"]

    if not isinstance(data.get("title"), str) or not data.get("title"):
        errors.append("title 必须是非空字符串")
    if not isinstance(data.get("author"), str) or not data.get("author"):
        errors.append("author 必须是非空字符串")

    rating = data.get("rating")
    if rating is not None and (not isinstance(rating, int) or not 1 <= rating <= 5):
        errors.append("rating 必须是 1-5 的整数")

    return len(errors) == 0, errors


def load_books_collection(filepath):
    """加载书籍列表，只保留有效记录。"""
    data = safe_load_json(filepath)
    if not isinstance(data, list):
        return []

    valid_books = []
    for item in data:
        is_valid, _errors = validate_book_data(item)
        if is_valid:
            valid_books.append(item)
    return valid_books
