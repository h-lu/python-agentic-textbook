"""
共享 fixture 定义

本文件定义了多个测试文件共享的 fixture。
pytest 会自动发现 conftest.py 中的 fixture。

运行方式：
  pytest tests/ -v
"""

import pytest


@pytest.fixture
def sample_records():
    """
    提供示例学习记录

    返回包含 3 条记录的列表，用于多个测试共享
    """
    return [
        {"date": "2026-02-09", "content": "学了 pytest 基础", "mood": "开心"},
        {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"},
        {"date": "2026-02-07", "content": "学了异常处理", "mood": "兴奋"}
    ]


@pytest.fixture
def empty_records():
    """提供空记录列表"""
    return []


@pytest.fixture
def single_record():
    """提供单条记录"""
    return [
        {"date": "2026-02-09", "content": "今天学了 Python", "mood": "开心"}
    ]
