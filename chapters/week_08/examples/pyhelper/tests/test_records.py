"""
records.py 的 pytest 测试

本测试文件演示：
1. 使用 conftest.py 中的共享 fixture
2. 参数化测试覆盖边界情况
3. 测试异常抛出

运行方式：
  cd chapters/week_08/examples/pyhelper
  pytest tests/test_records.py -v

预期输出：
  所有测试通过，包括参数化测试的多组数据
"""

import pytest
from pathlib import Path

# 导入被测模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from records import (
    add_record,
    count_study_days,
    get_records_by_mood,
    get_latest_record,
    validate_record
)


# ========== 使用共享 fixture 的测试 ==========

def test_add_record(sample_records):
    """
    使用 conftest.py 中的 sample_records fixture

    sample_records 包含 3 条记录
    """
    new_record = {"date": "2026-02-10", "content": "学了 TDD", "mood": "期待"}

    result = add_record(sample_records, new_record)

    assert len(result) == 4
    assert result[-1] == new_record


def test_count_study_days(sample_records):
    """使用 sample_records 测试统计功能"""
    result = count_study_days(sample_records)

    assert result == 3  # 3 条记录，3 个不同日期


def test_count_study_days_empty(empty_records):
    """使用 empty_records fixture 测试空列表"""
    result = count_study_days(empty_records)

    assert result == 0


# ========== 业务逻辑测试 ==========

def test_add_record_overwrite_existing(sample_records):
    """测试添加已存在的日期会覆盖"""
    original_count = len(sample_records)

    # 添加一个已存在的日期
    new_record = {"date": "2026-02-09", "content": "复习 pytest", "mood": "自信"}
    result = add_record(sample_records, new_record)

    # 记录数不变，但内容更新
    assert len(result) == original_count
    assert result[0]["content"] == "复习 pytest"
    assert result[0]["mood"] == "自信"


def test_get_records_by_mood(sample_records):
    """测试按心情筛选"""
    happy_records = get_records_by_mood(sample_records, "开心")

    assert len(happy_records) == 1
    assert happy_records[0]["date"] == "2026-02-09"


def test_get_records_by_mood_no_match(sample_records):
    """测试按心情筛选无匹配结果"""
    result = get_records_by_mood(sample_records, "不存在的心情")

    assert result == []


def test_get_latest_record(sample_records):
    """测试获取最新记录"""
    latest = get_latest_record(sample_records)

    assert latest["date"] == "2026-02-09"
    assert latest["content"] == "学了 pytest 基础"


def test_get_latest_record_empty(empty_records):
    """测试空列表返回 None"""
    result = get_latest_record(empty_records)

    assert result is None


# ========== 参数化测试边界情况 ==========

@pytest.mark.parametrize("content,should_accept", [
    ("今天学了 Python", True),           # 正常内容
    ("  有空格的内容  ", True),          # 带空格
    ("", False),                          # 空内容，应该拒绝
    ("a" * 5000, False),                  # 超长内容
    ("🐍 Python 学习", True),            # 带 emoji
])
def test_validate_record_content(content, should_accept):
    """测试内容校验"""
    record = {"date": "2026-02-09", "content": content}

    if should_accept:
        result = validate_record(record)
        assert result == True
    else:
        with pytest.raises(ValueError):
            validate_record(record)


@pytest.mark.parametrize("record,expected_error", [
    ({"date": "2026-02-09"}, "content"),           # 缺少 content
    ({"content": "学了 Python"}, "date"),          # 缺少 date
    ({}, "date"),                                   # 空字典
    ("不是字典", "必须是字典"),                     # 不是字典
])
def test_validate_record_invalid_format(record, expected_error):
    """测试格式错误的记录"""
    with pytest.raises(ValueError) as exc_info:
        validate_record(record)

    assert expected_error in str(exc_info.value)


# ========== 测试同一天多条记录的特殊情况 ==========

def test_duplicate_dates_count():
    """测试同一天多条记录的统计"""
    records = [
        {"date": "2026-02-09", "content": "上午学 pytest", "mood": "开心"},
        {"date": "2026-02-09", "content": "下午学 fixture", "mood": "兴奋"},
        {"date": "2026-02-08", "content": "复习", "mood": "平静"}
    ]

    # count_study_days 应该返回不重复的日期数
    days = count_study_days(records)

    assert days == 2  # 2 个不同日期


# ========== 反例：测试设计问题 ==========

def test_bad_test_design():
    """
    反例：不好的测试设计

    不好的做法：
    1. 一个测试函数验证多个不相关的事情
    2. 没有清晰的断言说明
    3. 测试失败后难以定位问题

    # 不好的例子：
    def test_everything():
        records = []
        add_record(records, {...})
        add_record(records, {...})
        count = count_study_days(records)
        by_mood = get_records_by_mood(records, "开心")
        latest = get_latest_record(records)

        assert len(records) == 2 and count == 2 and by_mood and latest
        # 这个断言失败了，但不知道是哪个条件不满足

    好的做法：
    - 每个测试函数只测一个概念
    - 使用描述性的测试名
    - 多个独立的断言，失败时清楚知道哪里错了
    """
    pass  # 这是一个文档化的反例
