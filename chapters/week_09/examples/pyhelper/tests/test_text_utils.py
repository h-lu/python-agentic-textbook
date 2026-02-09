"""
test_text_utils.py - text_utils 模块的测试

测试内容：
- search_notes: 关键词搜索
- filter_by_date: 日期范围过滤
- extract_tags: 标签提取
- format_note_summary: 摘要格式化
"""

import pytest
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from text_utils import search_notes, filter_by_date, extract_tags, format_note_summary


class TestSearchNotes:
    """测试 search_notes 函数"""

    def test_basic_search(self, sample_notes):
        """测试基本搜索功能"""
        results = search_notes(sample_notes, "Python")
        assert len(results) == 3  # 3条笔记包含 Python（"了解了异常处理"这条没有）

    def test_case_insensitive(self, sample_notes):
        """测试大小写不敏感"""
        results_lower = search_notes(sample_notes, "python")
        results_upper = search_notes(sample_notes, "PYTHON")
        assert len(results_lower) == len(results_upper)

    def test_empty_keyword(self, sample_notes):
        """测试空关键词返回空列表"""
        assert search_notes(sample_notes, "") == []
        assert search_notes(sample_notes, "   ") == []
        assert search_notes(sample_notes, None) == []

    def test_no_match(self, sample_notes):
        """测试没有匹配的情况"""
        results = search_notes(sample_notes, "Java")
        assert results == []

    def test_partial_match(self, sample_notes):
        """测试部分匹配"""
        results = search_notes(sample_notes, "正则")
        assert len(results) == 1
        assert results[0]["date"] == "2026-02-09"

    def test_empty_notes(self):
        """测试空笔记列表"""
        assert search_notes([], "Python") == []


class TestFilterByDate:
    """测试 filter_by_date 函数"""

    def test_date_range(self, sample_notes):
        """测试日期范围过滤"""
        results = filter_by_date(sample_notes, "2026-02-07", "2026-02-08")
        assert len(results) == 2
        dates = [r["date"] for r in results]
        assert "2026-02-07" in dates
        assert "2026-02-08" in dates

    def test_start_date_only(self, sample_notes):
        """测试只指定开始日期"""
        results = filter_by_date(sample_notes, start_date="2026-02-08")
        assert len(results) == 2
        assert all(r["date"] >= "2026-02-08" for r in results)

    def test_end_date_only(self, sample_notes):
        """测试只指定结束日期"""
        results = filter_by_date(sample_notes, end_date="2026-02-05")
        assert len(results) == 1
        assert results[0]["date"] == "2026-02-01"

    def test_no_dates(self, sample_notes):
        """测试不指定日期返回所有笔记"""
        results = filter_by_date(sample_notes)
        assert len(results) == 4

    def test_invalid_date_format(self, sample_notes):
        """测试无效日期格式"""
        results = filter_by_date(sample_notes, "invalid", "2026-02-10")
        assert results == []  # 无效日期格式时跳过所有

    def test_invalid_note_date(self):
        """测试笔记日期格式错误"""
        bad_notes = [
            {"date": "invalid", "content": "test"},
            {"date": "2026-02-09", "content": "valid"},
        ]
        results = filter_by_date(bad_notes)
        assert len(results) == 1
        assert results[0]["date"] == "2026-02-09"


class TestExtractTags:
    """测试 extract_tags 函数"""

    def test_basic_tags(self):
        """测试基本标签提取"""
        content = "学了 #Python 和 #正则表达式"
        tags = extract_tags(content)
        assert "Python" in tags
        assert "正则表达式" in tags

    def test_english_tags(self):
        """测试英文标签"""
        content = "Working on #Python project with #pytest"
        tags = extract_tags(content)
        assert "Python" in tags
        assert "pytest" in tags

    def test_mixed_tags(self):
        """测试中英文混合标签"""
        content = "#Python #学习 #week_09"
        tags = extract_tags(content)
        assert "Python" in tags
        assert "学习" in tags
        assert "week_09" in tags

    def test_empty_content(self):
        """测试空内容"""
        assert extract_tags("") == []
        assert extract_tags(None) == []

    def test_no_tags(self):
        """测试没有标签的内容"""
        content = "今天学习了 Python"
        assert extract_tags(content) == []

    def test_tag_with_special_chars(self):
        """测试带特殊字符的标签"""
        # #tag! 应该只提取 tag，不包括 !
        content = "Hello #world!"
        tags = extract_tags(content)
        assert "world" in tags
        assert "world!" not in tags


class TestFormatNoteSummary:
    """测试 format_note_summary 函数"""

    def test_long_content(self):
        """测试长内容截断"""
        # 内容超过50个字符会被截断
        note = {
            "date": "2026-02-09",
            "content": "今天学习了很多内容，包括正则表达式、字符串方法、边界情况处理等等，还有测试和调试技巧和更多内容 #Python"
        }
        summary = format_note_summary(note)
        assert "..." in summary
        assert len(summary) > 50  # 摘要应该包含日期和标签

    def test_short_content(self):
        """测试短内容不截断"""
        note = {
            "date": "2026-02-09",
            "content": "复习"
        }
        summary = format_note_summary(note)
        assert "..." not in summary
        assert "复习" in summary

    def test_with_tags(self):
        """测试带标签的格式化"""
        note = {
            "date": "2026-02-09",
            "content": "学了正则 #Python #学习"
        }
        summary = format_note_summary(note)
        assert "#Python" in summary
        assert "#学习" in summary

    def test_missing_fields(self):
        """测试缺失字段"""
        note = {"content": "test"}
        summary = format_note_summary(note)
        assert "未知日期" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
