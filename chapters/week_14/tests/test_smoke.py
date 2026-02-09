"""Week 14 基线测试（Smoke Tests）

这些是基础的冒烟测试，用于验证基本的测试框架是否正常工作。
不要修改这个文件——这是脚手架自带的基线测试。
"""

import pytest


def test_python_version():
    """测试 Python 版本是否合理"""
    import sys
    # 要求 Python 3.8+
    assert sys.version_info >= (3, 8)


def test_pytest_works():
    """测试 pytest 框架本身是否正常工作"""
    assert True is True
    assert False is False
    assert 1 + 1 == 2


def test_basic_imports():
    """测试基本库导入"""
    import sys
    import os
    import re
    from pathlib import Path
    from typing import List, Dict, Tuple

    # 这些导入应该成功
    assert sys is not None
    assert os is not None
    assert re is not None
    assert Path is not None


class TestBasicAssertions:
    """测试基本的断言功能"""

    def test_assertion_equal(self):
        """测试相等断言"""
        assert 1 == 1
        assert "hello" == "hello"

    def test_assertion_not_equal(self):
        """测试不等断言"""
        assert 1 != 2
        assert "hello" != "world"

    def test_assertion_in(self):
        """测试包含断言"""
        assert "hello" in "hello world"
        assert 1 in [1, 2, 3]

    def test_assertion_is_instance(self):
        """测试类型断言"""
        assert isinstance(1, int)
        assert isinstance("hello", str)
        assert isinstance([1, 2], list)

    def test_assertion_raises(self):
        """测试异常断言"""
        with pytest.raises(ValueError):
            raise ValueError("测试异常")

        with pytest.raises(ZeroDivisionError):
            result = 1 / 0


class TestFixturesWork:
    """测试 fixtures 功能"""

    def test_simple_fixture(self):
        """测试简单的 fixture"""
        # 这是一个简单的 fixture 测试
        data = {"key": "value"}
        assert data["key"] == "value"


def test_string_operations():
    """测试字符串操作"""
    s = "PyHelper v1.0.0"
    assert "PyHelper" in s
    assert "v1.0.0" in s
    assert s.startswith("PyHelper")
    assert s.endswith("1.0.0")


def test_list_operations():
    """测试列表操作"""
    versions = ["1.0.0", "1.1.0", "2.0.0"]
    assert len(versions) == 3
    assert "1.0.0" in versions
    assert versions[0] == "1.0.0"


def test_dict_operations():
    """测试字典操作"""
    project = {
        "name": "PyHelper",
        "version": "1.0.0",
        "description": "学习助手"
    }
    assert project["name"] == "PyHelper"
    assert project["version"] == "1.0.0"
    assert "description" in project
