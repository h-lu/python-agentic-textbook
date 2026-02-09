"""
conftest.py - pytest 共享 fixture

定义测试用的共享数据和 fixture
"""

import pytest


@pytest.fixture
def sample_notes():
    """提供测试用的笔记数据"""
    return [
        {"date": "2026-02-09", "content": "学了正则表达式 #Python #学习"},
        {"date": "2026-02-08", "content": "复习了字符串方法 #Python"},
        {"date": "2026-02-07", "content": "了解了异常处理 #基础"},
        {"date": "2026-02-01", "content": "开始学习 Python #入门"},
    ]


@pytest.fixture
def empty_notes():
    """提供空的笔记列表"""
    return []
