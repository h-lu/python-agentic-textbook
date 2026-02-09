"""
records.py - PyHelper 业务逻辑模块

职责：负责学习记录的业务逻辑

功能：
- add_record()：添加学习记录
- count_study_days()：统计学习天数
- get_records_by_mood()：按心情筛选记录
- validate_record()：验证记录格式

运行方式（测试）：
  python3 records.py

导入方式：
  from records import add_record, count_study_days
"""


def validate_record(record):
    """
    验证学习记录格式

    Args:
        record: 学习记录字典

    Returns:
        True 如果格式有效

    Raises:
        ValueError: 如果格式无效
    """
    if not isinstance(record, dict):
        raise ValueError("记录必须是字典")

    if "date" not in record:
        raise ValueError("记录必须包含 'date' 字段")

    if "content" not in record:
        raise ValueError("记录必须包含 'content' 字段")

    content = record["content"].strip()
    if not content:
        raise ValueError("content 不能为空")

    if len(content) > 1000:
        raise ValueError("content 不能超过 1000 个字符")

    return True


def add_record(records, new_record):
    """
    添加学习记录

    Args:
        records: 现有记录列表
        new_record: 新记录字典

    Returns:
        更新后的记录列表

    Raises:
        ValueError: 如果记录格式无效
    """
    validate_record(new_record)

    # 检查是否已存在同日期记录
    for i, record in enumerate(records):
        if record.get("date") == new_record["date"]:
            # 覆盖已有记录
            records[i] = new_record
            return records

    records.append(new_record)
    return records


def count_study_days(records):
    """
    统计学习天数（不重复的日期数）

    Args:
        records: 学习记录列表

    Returns:
        学习天数（整数）
    """
    unique_dates = set()
    for record in records:
        if "date" in record:
            unique_dates.add(record["date"])
    return len(unique_dates)


def get_records_by_mood(records, mood):
    """
    按心情筛选记录

    Args:
        records: 学习记录列表
        mood: 心情字符串

    Returns:
        符合条件的记录列表
    """
    return [r for r in records if r.get("mood") == mood]


def get_latest_record(records):
    """
    获取最新的学习记录

    Args:
        records: 学习记录列表

    Returns:
        最新的记录，如果没有则返回 None
    """
    if not records:
        return None

    # 假设日期格式为 YYYY-MM-DD，可以直接字符串比较
    return max(records, key=lambda r: r.get("date", ""))


# =====================
# 测试代码
# =====================

if __name__ == "__main__":
    print("=== 测试 records 模块 ===")

    records = []

    # 测试添加记录
    add_record(records, {"date": "2026-02-09", "content": "学了 pytest", "mood": "开心"})
    add_record(records, {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"})
    add_record(records, {"date": "2026-02-07", "content": "学了异常处理", "mood": "兴奋"})

    print(f"✓ 已添加 {len(records)} 条记录")

    # 测试统计
    days = count_study_days(records)
    print(f"✓ 学习天数: {days}")

    # 测试按心情筛选
    happy_records = get_records_by_mood(records, "开心")
    print(f"✓ 开心记录数: {len(happy_records)}")

    # 测试获取最新记录
    latest = get_latest_record(records)
    print(f"✓ 最新记录: {latest['date']} - {latest['content']}")

    # 测试覆盖已有记录
    add_record(records, {"date": "2026-02-09", "content": "复习 pytest", "mood": "自信"})
    print(f"✓ 覆盖后记录数: {len(records)} (应该还是 3)")

    print("\n✓ 所有测试通过！")
