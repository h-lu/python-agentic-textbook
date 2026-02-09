"""
storage.py - PyHelper 存储模块

职责：负责学习记录的文件读写操作

功能：
- save_learning_log()：保存学习记录到文件
- load_learning_log()：从文件加载学习记录

运行方式（测试）：
  python3 storage.py

导入方式：
  from storage import save_learning_log, load_learning_log
"""

import json
from pathlib import Path


def save_learning_log(records, file_path):
    """
    保存学习记录到 JSON 文件

    Args:
        records: 学习记录列表（每个记录是字典）
        file_path: 文件路径（Path 对象或字符串）

    Returns:
        True 如果保存成功

    Raises:
        TypeError: 如果 records 不是列表
        ValueError: 如果记录格式无效
    """
    if not isinstance(records, list):
        raise TypeError("records 必须是列表")

    # 验证记录格式
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("每条记录必须是字典")
        if "date" not in record or "content" not in record:
            raise ValueError("记录必须包含 'date' 和 'content' 字段")

    file_path = Path(file_path)
    file_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def load_learning_log(file_path):
    """
    从 JSON 文件加载学习记录

    Args:
        file_path: 文件路径（Path 对象或字符串）

    Returns:
        学习记录列表，如果文件不存在则返回空列表

    Raises:
        ValueError: 如果文件内容不是有效的 JSON 或格式错误
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return []

    try:
        content = file_path.read_text(encoding="utf-8")
        if not content.strip():
            return []

        records = json.loads(content)

        if not isinstance(records, list):
            raise ValueError("文件内容必须是列表")

        return records

    except json.JSONDecodeError as e:
        raise ValueError(f"无效的 JSON 格式: {e}")


# =====================
# 测试代码
# =====================

if __name__ == "__main__":
    print("=== 测试 storage 模块 ===")

    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test_log.json"

        # 测试保存
        records = [
            {"date": "2026-02-09", "content": "学了 pytest 基础", "mood": "开心"},
            {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"}
        ]
        save_learning_log(records, test_file)
        print(f"✓ 已保存 {len(records)} 条记录")

        # 测试加载
        loaded = load_learning_log(test_file)
        print(f"✓ 已加载 {len(loaded)} 条记录")

        # 验证数据
        assert loaded == records, "数据不一致"
        print("✓ 数据验证通过")

        # 测试加载不存在的文件
        empty = load_learning_log(Path(tmpdir) / "not_exist.json")
        assert empty == [], "应该返回空列表"
        print("✓ 加载不存在的文件返回空列表")

    print("\n✓ 所有测试通过！")
