"""
示例：JSON 基础语法与 Python 的 json 模块

本示例演示：
1. JSON 与 Python 字典的区别
2. json.dumps() / json.loads() 的使用
3. JSON 语法规则（双引号、布尔值、null）
4. 常见错误示例

运行方式：python3 chapters/week_10/examples/02_json_basics.py
预期输出：展示 JSON 序列化和反序列化的过程
"""

import json


# =====================
# 1. 字典 vs JSON 字符串
# =====================

print("=== 1. 字典 vs JSON 字符串 ===\n")

# Python 字典
note_dict = {
    "date": "2026-02-01",
    "content": "学习了 JSON 格式",
    "tags": ["Python", "JSON"],
    "rating": 5,
    "finished": True
}

print(f"Python 字典类型: {type(note_dict)}")
print(f"内容: {note_dict}")
print()

# 序列化：字典 → JSON 字符串
json_str = json.dumps(note_dict)
print(f"json.dumps() 后类型: {type(json_str)}")
print(f"JSON 字符串: {json_str}")
print()

# 反序列化：JSON 字符串 → 字典
parsed_dict = json.loads(json_str)
print(f"json.loads() 后类型: {type(parsed_dict)}")
print(f"解析后的字典: {parsed_dict}")
print()


# =====================
# 2. 美化输出
# =====================

print("=== 2. 美化 JSON 输出 ===\n")

# 使用 indent 参数美化输出
pretty_json = json.dumps(note_dict, indent=2, ensure_ascii=False)
print("带缩进和中文支持的 JSON：")
print(pretty_json)
print()


# =====================
# 3. JSON 语法规则
# =====================

print("=== 3. JSON 语法规则 ===\n")

# Python 和 JSON 的区别示例
python_data = {
    "name": '小北',           # Python 允许单引号
    "active": True,          # Python 是 True
    "score": None,           # Python 是 None
    "items": [1, 2, 3,],     # Python 允许尾随逗号
}

json_str_strict = json.dumps(python_data, ensure_ascii=False)
print("JSON 输出（注意变化）：")
print(json_str_strict)
print()
print("关键区别：")
print("- 字符串必须是双引号")
print("- True → true, False → false")
print("- None → null")
print("- 尾随逗号会被移除")
print()


# =====================
# 4. 文件读写
# =====================

print("=== 4. JSON 文件读写 ===\n")

import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmpdir:
    data_file = Path(tmpdir) / "notes.json"

    # 写入 JSON 文件
    notes = [
        {"date": "2026-02-01", "content": "学习了 JSON", "rating": 5},
        {"date": "2026-02-02", "content": "练习了序列化", "rating": 4},
    ]

    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

    print(f"已保存到文件: {data_file}")
    print("文件内容：")
    print(data_file.read_text())

    # 从 JSON 文件读取
    with open(data_file, "r", encoding="utf-8") as f:
        loaded_notes = json.load(f)

    print(f"从文件读取了 {len(loaded_notes)} 条笔记")
    print()


# =====================
# 5. 常见错误示例
# =====================

print("=== 5. 常见错误示例 ===\n")

# 错误 1：使用单引号（Python 允许，JSON 不允许）
print("错误 1：JSON 中使用单引号")
bad_json_1 = "{'key': 'value'}"
try:
    json.loads(bad_json_1)
except json.JSONDecodeError as e:
    print(f"  解析失败: {e}")
print()

# 错误 2：缺少引号
print("错误 2：键没有引号")
bad_json_2 = '{key: "value"}'
try:
    json.loads(bad_json_2)
except json.JSONDecodeError as e:
    print(f"  解析失败: {e}")
print()

# 错误 3：尾随逗号
print("错误 3：对象中有尾随逗号")
bad_json_3 = '{"a": 1, "b": 2,}'
try:
    json.loads(bad_json_3)
except json.JSONDecodeError as e:
    print(f"  解析失败: {e}")
print()

# 错误 4：使用了 Python 的 True/False/None
print("错误 4：使用 Python 的 True/False/None")
bad_json_4 = '{"active": True, "score": None}'
try:
    json.loads(bad_json_4)
except json.JSONDecodeError as e:
    print(f"  解析失败: {e}")
print()

# 正确的写法
print("正确的 JSON 写法：")
good_json = '{"active": true, "score": null}'
parsed = json.loads(good_json)
print(f"  解析成功: {parsed}")
print()


# =====================
# 6. 对比总结
# =====================

print("=== Python vs JSON 对比 ===\n")
print("| 特性          | Python          | JSON           |")
print("|---------------|-----------------|----------------|")
print("| 字符串引号    | 单引号或双引号  | 必须是双引号   |")
print("| 布尔值        | True / False    | true / false   |")
print("| 空值          | None            | null           |")
print("| 尾随逗号      | 允许            | 不允许         |")
print("| 注释          | 支持            | 不支持         |")
print("| 键的类型      | 任何不可变类型  | 必须是字符串   |")
