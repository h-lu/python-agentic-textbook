"""
示例：序列化与反序列化——处理复杂数据结构

本示例演示：
1. 嵌套数据结构的序列化
2. 日期时间的自定义序列化处理
3. 自定义序列化函数
4. pickle 与 JSON 的对比

运行方式：python3 chapters/week_10/examples/03_serialization.py
预期输出：展示复杂数据的序列化过程
"""

import json
import datetime
from pathlib import Path


# =====================
# 1. 嵌套数据结构
# =====================

print("=== 1. 嵌套数据结构的序列化 ===\n")

# 复杂的书单数据
book = {
    "title": "Python 编程：从入门到实践",
    "author": "Eric Matthes",
    "rating": 5,
    "tags": ["Python", "编程入门", "实践"],
    "notes": [
        {"date": "2026-02-01", "content": "第 1 章介绍了变量和字符串"},
        {"date": "2026-02-03", "content": "第 3 章的函数部分很有启发"}
    ],
    "finished": False,
    "metadata": {
        "publisher": "人民邮电出版社",
        "year": 2020,
        "pages": 476
    }
}

# 序列化
json_str = json.dumps(book, indent=2, ensure_ascii=False)
print("嵌套数据序列化成功：")
print(json_str)
print()

# 反序列化
parsed_book = json.loads(json_str)
print(f"反序列化后访问嵌套数据：")
print(f"  书名: {parsed_book['title']}")
print(f"  第一条笔记: {parsed_book['notes'][0]['content']}")
print(f"  出版社: {parsed_book['metadata']['publisher']}")
print()


# =====================
# 2. 日期时间的序列化问题
# =====================

print("=== 2. 日期时间的序列化问题 ===\n")

# 包含日期对象的数据
book_with_date = {
    "title": "某本书",
    "added_date": datetime.date(2026, 2, 9),  # 日期对象
    "updated_at": datetime.datetime(2026, 2, 9, 14, 30, 0)  # 日期时间对象
}

print("尝试直接序列化包含日期对象的数据...")
try:
    json.dumps(book_with_date)
except TypeError as e:
    print(f"✗ 失败: {e}")
print()


# =====================
# 3. 自定义序列化处理
# =====================

print("=== 3. 自定义序列化处理 ===\n")

def custom_serializer(obj):
    """
    自定义序列化函数
    处理 Python 的特殊类型，转换为 JSON 可序列化的类型
    """
    if isinstance(obj, datetime.date):
        # 日期对象转换为 ISO 格式字符串
        return obj.isoformat()
    if isinstance(obj, datetime.datetime):
        # 日期时间对象转换为 ISO 格式字符串
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


# 使用 default 参数进行自定义序列化
json_with_date = json.dumps(
    book_with_date,
    default=custom_serializer,
    indent=2,
    ensure_ascii=False
)
print("使用自定义序列化函数：")
print(json_with_date)
print()


# =====================
# 4. 自定义反序列化
# =====================

print("=== 4. 自定义反序列化 ===\n")

def custom_deserializer(dct):
    """
    自定义反序列化函数
    将特定格式的字符串转换回 Python 对象
    """
    # 检查是否包含日期字段，尝试转换
    for key in ["added_date", "date", "updated_at", "created_at"]:
        if key in dct and isinstance(dct[key], str):
            try:
                # 尝试解析为日期
                if "T" in dct[key] or " " in dct[key]:
                    # 可能是 datetime
                    dct[key] = datetime.datetime.fromisoformat(dct[key].replace(" ", "T"))
                else:
                    # 可能是 date
                    dct[key] = datetime.date.fromisoformat(dct[key])
            except ValueError:
                pass  # 不是日期格式，保持原样
    return dct


# 反序列化
parsed_with_date = json.loads(json_with_date, object_hook=custom_deserializer)
print("反序列化后：")
print(f"  added_date 类型: {type(parsed_with_date['added_date'])}")
print(f"  added_date 值: {parsed_with_date['added_date']}")
print()


# =====================
# 5. JSON vs Pickle 对比
# =====================

print("=== 5. JSON vs Pickle 对比 ===\n")

import pickle
import tempfile

with tempfile.TemporaryDirectory() as tmpdir:
    # 测试数据
    test_data = {"name": "测试", "items": [1, 2, 3], "active": True}

    # JSON 序列化
    json_file = Path(tmpdir) / "data.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    # Pickle 序列化
    pickle_file = Path(tmpdir) / "data.pkl"
    with open(pickle_file, "wb") as f:
        pickle.dump(test_data, f)

    print("文件对比：")
    print(f"  JSON 文件大小: {json_file.stat().st_size} 字节")
    print(f"  Pickle 文件大小: {pickle_file.stat().st_size} 字节")
    print()

    print("文件内容对比：")
    print(f"  JSON (文本可读): {json_file.read_text()[:50]}...")
    print(f"  Pickle (二进制): {pickle_file.read_bytes()[:30]}...")
    print()

print("对比总结：")
print("| 特性        | JSON                    | Pickle                  |")
print("|-------------|-------------------------|-------------------------|")
print("| 可读性      | 纯文本，人类可读        | 二进制，不可读          |")
print("| 跨语言      | 支持                    | 仅 Python               |")
print("| 安全性      | 安全                    | 不安全（可能执行代码）  |")
print("| 数据类型    | 基本类型                | 几乎所有 Python 对象    |")
print("| 适用场景    | 数据交换、API、配置     | 临时缓存、进程间通信    |")
print()


# =====================
# 6. 实用工具函数
# =====================

print("=== 6. 实用工具函数 ===\n")

def save_with_metadata(data, filepath, version="1.0"):
    """
    保存数据，自动添加元信息

    Args:
        data: 要保存的数据
        filepath: 文件路径
        version: 数据版本
    """
    wrapper = {
        "_metadata": {
            "version": version,
            "created_at": datetime.datetime.now().isoformat(),
            "data_type": type(data).__name__,
            "item_count": len(data) if hasattr(data, "__len__") else None
        },
        "data": data
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(wrapper, f, indent=2, ensure_ascii=False, default=custom_serializer)

    print(f"数据已保存到 {filepath}")
    print(f"版本: {version}")


# 测试
with tempfile.TemporaryDirectory() as tmpdir:
    test_file = Path(tmpdir) / "wrapped_data.json"
    books = [
        {"title": "书 1", "rating": 5},
        {"title": "书 2", "rating": 4},
    ]
    save_with_metadata(books, test_file, version="2.0")
    print()
    print("文件内容：")
    print(test_file.read_text())
