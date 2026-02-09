"""Week 10: JSON 与序列化 - 学生作业参考实现

本模块包含 JSON 相关功能的完整实现，供学生参考。

运行方式:
  python3 solution.py
"""

import json
import datetime
from pathlib import Path
from typing import Any, Optional


# ==================== 1. JSON 基础操作 ====================

def parse_json_string(json_str: str) -> Any:
    """将 JSON 字符串解析为 Python 对象

    Args:
        json_str: JSON 格式的字符串

    Returns:
        解析后的 Python 对象（字典、列表等）

    Raises:
        json.JSONDecodeError: 当 JSON 格式不正确时
    """
    return json.loads(json_str)


def to_json_string(obj: Any, indent: Optional[int] = None, ensure_ascii: bool = True) -> str:
    """将 Python 对象序列化为 JSON 字符串

    Args:
        obj: 要序列化的 Python 对象
        indent: 缩进空格数，None 表示不格式化
        ensure_ascii: 是否将非 ASCII 字符转义为 \uXXXX

    Returns:
        JSON 格式的字符串
    """
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii)


def to_json_string_with_chinese(obj: Any, indent: Optional[int] = None) -> str:
    """将 Python 对象序列化为 JSON 字符串，保留中文字符

    Args:
        obj: 要序列化的 Python 对象
        indent: 缩进空格数

    Returns:
        JSON 格式的字符串（中文字符原样输出）
    """
    return json.dumps(obj, indent=indent, ensure_ascii=False)


# ==================== 2. 文件读写 ====================

def save_to_json_file(obj: Any, filepath: str, indent: int = 2, ensure_ascii: bool = False) -> None:
    """将 Python 对象保存到 JSON 文件

    Args:
        obj: 要保存的 Python 对象
        filepath: 文件路径
        indent: 缩进空格数
        ensure_ascii: 是否转义非 ASCII 字符
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=ensure_ascii)


def load_from_json_file(filepath: str) -> Any:
    """从 JSON 文件加载 Python 对象

    Args:
        filepath: JSON 文件路径

    Returns:
        解析后的 Python 对象

    Raises:
        FileNotFoundError: 文件不存在时
        json.JSONDecodeError: JSON 格式不正确时
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_load_from_json_file(filepath: str, default: Any = None) -> Any:
    """安全地从 JSON 文件加载，出错时返回默认值

    Args:
        filepath: JSON 文件路径
        default: 出错时返回的默认值

    Returns:
        解析后的 Python 对象，或默认值
    """
    try:
        return load_from_json_file(filepath)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


# ==================== 3. 序列化边界情况 ====================

def _datetime_serializer(obj: Any) -> str:
    """自定义序列化函数，处理日期时间对象"""
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def serialize_with_datetime(obj: dict) -> str:
    """序列化包含日期时间的字典

    自定义 default 函数处理 datetime.date 和 datetime.datetime 对象

    Args:
        obj: 可能包含日期时间的字典

    Returns:
        JSON 字符串

    Raises:
        TypeError: 当包含无法序列化的对象时
    """
    return json.dumps(obj, default=_datetime_serializer, ensure_ascii=False)


def _datetime_deserializer(dct: dict) -> dict:
    """自定义反序列化函数，将日期字符串转换回日期对象"""
    for key in ["date", "created_at", "updated_at"]:
        if key in dct and isinstance(dct[key], str):
            try:
                if "T" in dct[key]:
                    dct[key] = datetime.datetime.fromisoformat(dct[key])
                else:
                    dct[key] = datetime.date.fromisoformat(dct[key])
            except ValueError:
                pass
    return dct


def deserialize_with_datetime(json_str: str) -> dict:
    """反序列化 JSON 字符串，将日期字符串转换回日期对象

    使用 object_hook 自动识别并转换 ISO 格式的日期字符串

    Args:
        json_str: JSON 字符串

    Returns:
        解析后的字典，包含日期对象
    """
    return json.loads(json_str, object_hook=_datetime_deserializer)


def is_json_serializable(obj: Any) -> bool:
    """检查对象是否可以被 JSON 序列化

    Args:
        obj: 要检查的对象

    Returns:
        是否可以序列化
    """
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False


# ==================== 4. 异常处理 ====================

def parse_json_safe(json_str: str, default: Any = None) -> Any:
    """安全地解析 JSON 字符串

    Args:
        json_str: JSON 字符串
        default: 解析失败时返回的默认值

    Returns:
        解析后的对象，或默认值
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return default


def validate_json_structure(data: Any, schema: dict) -> tuple[bool, Optional[str]]:
    """验证 JSON 数据结构是否符合预期

    简单实现，检查必需字段和类型

    Args:
        data: 要验证的数据
        schema: 结构定义，例如 {"required": ["name"], "types": {"name": str}}

    Returns:
        (是否通过, 错误信息)
    """
    required = schema.get("required", [])
    types = schema.get("types", {})

    # 检查必需字段
    for field in required:
        if field not in data:
            return False, f"缺少必需字段: {field}"

    # 检查类型
    for field, expected_type in types.items():
        if field in data and not isinstance(data[field], expected_type):
            return False, f"字段 {field} 类型错误，期望 {expected_type}"

    return True, None


def get_json_error_info(json_str: str) -> Optional[dict]:
    """获取 JSON 解析错误的详细信息

    Args:
        json_str: JSON 字符串

    Returns:
        错误信息字典，或 None（如果解析成功）
    """
    try:
        json.loads(json_str)
        return None
    except json.JSONDecodeError as e:
        return {
            "msg": str(e),
            "lineno": e.lineno,
            "colno": e.colno,
            "pos": e.pos
        }


# ==================== 5. PyHelper 功能 ====================

def migrate_note(note: dict) -> dict:
    """将旧版本笔记迁移到最新版本

    v1 -> v2: 添加 tags 字段（如果不存在）
    v1 -> v2: 添加 created_at 字段（如果不存在，使用 date 字段）

    Args:
        note: 笔记字典

    Returns:
        迁移后的笔记字典
    """
    # 确保是字典
    if not isinstance(note, dict):
        return {"date": "", "content": str(note), "tags": [], "created_at": ""}

    # v1 -> v2: 添加 tags 字段
    note.setdefault("tags", [])

    # v1 -> v2: 添加 created_at 字段
    if "created_at" not in note:
        note["created_at"] = note.get("date", "")

    return note


def migrate_notes(notes: list) -> list:
    """批量迁移笔记到最新版本

    Args:
        notes: 笔记列表

    Returns:
        迁移后的笔记列表
    """
    return [migrate_note(note) for note in notes]


def export_notes(notes: list, filepath: str, format: str = "json") -> int:
    """导出笔记到文件

    Args:
        notes: 笔记列表
        filepath: 输出文件路径
        format: 导出格式，支持 "json" 或 "txt"

    Returns:
        导出的笔记数量

    Raises:
        ValueError: 不支持的格式
    """
    filepath = Path(filepath)

    if format == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)

    elif format == "txt":
        with open(filepath, "w", encoding="utf-8") as f:
            for note in notes:
                f.write(f"日期: {note.get('date', '未知')}\n")
                f.write(f"内容: {note.get('content', '')}\n")
                if note.get('tags'):
                    f.write(f"标签: {', '.join(note['tags'])}\n")
                f.write("-" * 40 + "\n")
    else:
        raise ValueError(f"不支持的格式: {format}")

    return len(notes)


def import_notes(filepath: str, existing_notes: list = None) -> tuple[list, int]:
    """从文件导入笔记

    Args:
        filepath: JSON 文件路径
        existing_notes: 已有的笔记列表（用于去重）

    Returns:
        (合并后的笔记列表, 新增的笔记数量)

    Raises:
        FileNotFoundError: 文件不存在时
        json.JSONDecodeError: JSON 格式不正确时
    """
    if existing_notes is None:
        existing_notes = []

    with open(filepath, "r", encoding="utf-8") as f:
        new_notes = json.load(f)

    if not isinstance(new_notes, list):
        raise ValueError("文件内容必须是列表")

    # 去重（根据日期+内容）
    existing_keys = {(n.get("date"), n.get("content")) for n in existing_notes}
    added = 0

    for note in new_notes:
        key = (note.get("date"), note.get("content"))
        if key not in existing_keys:
            existing_notes.append(note)
            existing_keys.add(key)
            added += 1

    return existing_notes, added


def detect_version(notes: list) -> int:
    """检测笔记数据的版本

    v1: 没有 tags 字段
    v2: 有 tags 字段

    Args:
        notes: 笔记列表

    Returns:
        检测到的版本号（1 或 2），空列表返回 2
    """
    if not notes:
        return 2

    first_note = notes[0]
    if not isinstance(first_note, dict):
        return 1

    return 2 if "tags" in first_note else 1


# ==================== 6. 数据验证工具 ====================

def validate_note(note: dict) -> tuple[bool, Optional[str]]:
    """验证单条笔记的有效性

    Args:
        note: 笔记字典

    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(note, dict):
        return False, "笔记必须是字典"

    if "date" not in note:
        return False, "缺少 date 字段"

    if "content" not in note:
        return False, "缺少 content 字段"

    if not isinstance(note.get("content"), str):
        return False, "content 必须是字符串"

    return True, None


def filter_valid_notes(notes: list) -> list:
    """过滤掉无效的笔记

    Args:
        notes: 笔记列表

    Returns:
        有效的笔记列表
    """
    valid = []
    for note in notes:
        is_valid, _ = validate_note(note)
        if is_valid:
            valid.append(note)
    return valid


# ==================== 测试代码 ====================

if __name__ == "__main__":
    print("=== Week 10 作业参考实现测试 ===\n")

    # 测试 JSON 基础操作
    print("--- 测试 JSON 基础操作 ---")
    data = {"name": "小北", "age": 20}
    json_str = to_json_string(data)
    print(f"序列化: {json_str}")

    parsed = parse_json_string(json_str)
    print(f"反序列化: {parsed}")

    chinese_str = to_json_string_with_chinese({"msg": "你好"})
    print(f"保留中文: {chinese_str}")

    # 测试文件读写
    print("\n--- 测试文件读写 ---")
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.json"
        save_to_json_file(data, str(test_file))
        loaded = load_from_json_file(str(test_file))
        print(f"保存后读取: {loaded}")

    # 测试日期序列化
    print("\n--- 测试日期序列化 ---")
    data_with_date = {"name": "测试", "date": datetime.date(2026, 2, 9)}
    json_with_date = serialize_with_datetime(data_with_date)
    print(f"带日期的 JSON: {json_with_date}")

    # 测试异常处理
    print("\n--- 测试异常处理 ---")
    result = parse_json_safe('{"invalid"}', default={})
    print(f"安全解析无效 JSON: {result}")

    # 测试数据迁移
    print("\n--- 测试数据迁移 ---")
    old_note = {"date": "2026-02-09", "content": "旧格式笔记"}
    migrated = migrate_note(old_note)
    print(f"旧笔记: {old_note}")
    print(f"迁移后: {migrated}")

    print("\n✓ 所有测试通过！")
