"""Pytest 配置文件

提供测试夹具（fixtures）和通用配置
"""

import pytest
import sys
import os
from pathlib import Path
import tempfile


# 添加 starter_code 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'starter_code'))


# =====================
# Fixtures
# =====================

@pytest.fixture
def temp_dir():
    """创建临时目录用于测试"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_note_content():
    """示例笔记内容"""
    return """# Week 06: 异常处理

让程序不崩溃。

## 核心概念

- try/except 语句
- 常见异常类型
- 异常处理最佳实践
"""


@pytest.fixture
def sample_note_file(temp_dir, sample_note_content):
    """创建示例笔记文件"""
    note_file = temp_dir / "week06_exceptions.md"
    note_file.write_text(sample_note_content, encoding="utf-8")
    return note_file


@pytest.fixture
def empty_note_file(temp_dir):
    """创建空笔记文件"""
    note_file = temp_dir / "empty.md"
    note_file.write_text("", encoding="utf-8")
    return note_file


@pytest.fixture
def all_topics():
    """所有主题列表（用于检查前置知识）"""
    return ["变量", "函数", "文件", "异常处理", "测试", "JSON", "dataclass", "argparse"]


@pytest.fixture
def solution_modules():
    """尝试导入 solution.py 模块"""
    try:
        from solution import (
            NoteInfo,
            StudyPlan,
            ReviewResult,
            ReaderAgent,
            WriterAgent,
            ReviewerAgent,
            iterative_plan_generation,
            create_note_info,
            create_study_plan,
            create_review_result
        )
        return {
            'NoteInfo': NoteInfo,
            'StudyPlan': StudyPlan,
            'ReviewResult': ReviewResult,
            'ReaderAgent': ReaderAgent,
            'WriterAgent': WriterAgent,
            'ReviewerAgent': ReviewerAgent,
            'iterative_plan_generation': iterative_plan_generation,
            'create_note_info': create_note_info,
            'create_study_plan': create_study_plan,
            'create_review_result': create_review_result
        }
    except ImportError:
        return None
