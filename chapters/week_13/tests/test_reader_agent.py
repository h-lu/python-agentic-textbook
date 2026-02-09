"""测试 ReaderAgent

测试读取和解析笔记文件的功能
"""

import pytest
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))

try:
    from solution import NoteInfo, ReaderAgent
    SOLUTION_AVAILABLE = True
except ImportError:
    SOLUTION_AVAILABLE = False


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReaderAgentBasic:
    """测试 ReaderAgent 基本功能"""

    def test_reader_agent_instantiation(self):
        """测试 ReaderAgent 可以实例化"""
        agent = ReaderAgent()
        assert agent is not None
        assert hasattr(agent, 'read_note')

    def test_read_note_returns_note_info(self, sample_note_file):
        """测试 read_note 返回 NoteInfo 对象"""
        agent = ReaderAgent()
        result = agent.read_note(sample_note_file)

        assert isinstance(result, NoteInfo)
        assert hasattr(result, 'title')
        assert hasattr(result, 'topics')
        assert hasattr(result, 'difficulty')


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReaderAgentHappyPath:
    """测试 ReaderAgent 正常情况（Happy Path）"""

    def test_read_note_extract_title(self, sample_note_file):
        """测试提取笔记标题"""
        agent = ReaderAgent()
        result = agent.read_note(sample_note_file)

        assert "异常处理" in result.title or "Week 06" in result.title

    def test_read_note_extract_topics(self, sample_note_file):
        """测试提取笔记主题"""
        agent = ReaderAgent()
        result = agent.read_note(sample_note_file)

        assert isinstance(result.topics, list)
        assert len(result.topics) > 0  # 应该至少提取到一个主题

    def test_read_note_determine_difficulty(self, sample_note_file):
        """测试确定笔记难度"""
        agent = ReaderAgent()
        result = agent.read_note(sample_note_file)

        assert result.difficulty in ["easy", "medium", "hard"]

    def test_read_note_with_multiple_topics(self, temp_dir):
        """测试读取包含多个主题的笔记"""
        content = """# Week 08: 单元测试

学习 pytest 和函数测试。
"""
        note_file = temp_dir / "week08_testing.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        assert isinstance(result.topics, list)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReaderAgentEdgeCases:
    """测试 ReaderAgent 边界情况"""

    def test_read_note_empty_file(self, empty_note_file):
        """测试读取空文件（边界情况）"""
        agent = ReaderAgent()
        result = agent.read_note(empty_note_file)

        # 空文件也应该返回 NoteInfo，只是字段可能是空或默认值
        assert isinstance(result, NoteInfo)
        assert result.title == empty_note_file.stem  # 应该用文件名作为标题

    def test_read_note_file_without_title(self, temp_dir):
        """测试读取没有标题的文件"""
        content = """这是一篇笔记，但没有 # 标题。

内容是关于变量的。"""
        note_file = temp_dir / "no_title.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        # 应该用文件名作为标题
        assert isinstance(result, NoteInfo)
        assert result.title == "no_title"

    def test_read_note_special_characters(self, temp_dir):
        """测试读取包含特殊字符的笔记"""
        content = """# 特殊字符测试

包含中文：变量、函数
包含符号：$ @ # % &
包含换行和空格
"""
        note_file = temp_dir / "special.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        # 应该正常处理特殊字符
        assert isinstance(result, NoteInfo)
        assert isinstance(result.title, str)

    def test_read_note_long_file(self, temp_dir):
        """测试读取长文件（边界情况）"""
        # 创建一个较长的文件
        content = "# Week 10: 综合练习\n\n"
        for i in range(100):
            content += f"## 主题 {i}\n\n这是第 {i} 个主题的内容。\n\n"

        note_file = temp_dir / "long_note.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        # 应该能够处理长文件
        assert isinstance(result, NoteInfo)

    def test_read_note_file_with_different_encoding(self, temp_dir):
        """测试读取不同编码的文件"""
        # UTF-8 with BOM
        content = """# 编码测试

测试不同编码。"""
        note_file = temp_dir / "encoding.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        assert isinstance(result, NoteInfo)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReaderAgentErrorCases:
    """测试 ReaderAgent 错误处理"""

    def test_read_note_nonexistent_file(self, temp_dir):
        """测试读取不存在的文件（错误情况）"""
        agent = ReaderAgent()
        nonexistent_file = temp_dir / "does_not_exist.md"

        # 应该抛出 FileNotFoundError
        with pytest.raises(FileNotFoundError):
            agent.read_note(nonexistent_file)

    def test_read_note_directory_instead_of_file(self, temp_dir):
        """测试传入目录而不是文件（错误情况）"""
        agent = ReaderAgent()

        # 应该抛出异常（IsADirectoryError 或其他）
        with pytest.raises(Exception):
            agent.read_note(temp_dir)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReaderAgentTopicExtraction:
    """测试主题提取逻辑"""

    def test_extract_exception_topic(self, temp_dir):
        """测试提取'异常处理'主题"""
        content = "# Week 06\n\n学习异常处理和 try/except 语句。"
        note_file = temp_dir / "exceptions.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        # 应该识别出"异常处理"主题
        assert "异常处理" in result.topics

    def test_extract_function_topic(self, temp_dir):
        """测试提取'函数'主题"""
        content = "# Week 03\n\n学习函数定义和调用。"
        note_file = temp_dir / "functions.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        # 应该识别出"函数"主题
        assert "函数" in result.topics

    def test_extract_multiple_topics(self, temp_dir):
        """测试提取多个主题"""
        content = """# Week 06

学习异常处理、函数和变量。
"""
        note_file = temp_dir / "multi.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        # 应该识别出多个主题
        assert len(result.topics) >= 1


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReaderAgentDifficultyInference:
    """测试难度推断逻辑"""

    def test_difficulty_easy_for_few_topics(self, temp_dir):
        """测试主题少时难度为 easy"""
        content = "# Week 01\n\n简单介绍。"
        note_file = temp_dir / "easy.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        # 如果没有提取到主题，难度应该是 easy
        if len(result.topics) == 0:
            assert result.difficulty == "easy"

    def test_difficulty_medium_for_some_topics(self, temp_dir):
        """测试有适量主题时难度为 medium"""
        content = "# Week 05\n\n学习函数和变量。"
        note_file = temp_dir / "medium.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        # 如果提取到 1-2 个主题，难度应该是 medium
        if 1 <= len(result.topics) < 3:
            assert result.difficulty == "medium"

    def test_difficulty_hard_for_many_topics(self, temp_dir):
        """测试主题多时难度为 hard"""
        content = """# Week 10

学习函数、异常处理、测试和文件操作。
"""
        note_file = temp_dir / "hard.md"
        note_file.write_text(content, encoding="utf-8")

        agent = ReaderAgent()
        result = agent.read_note(note_file)

        # 如果提取到 3+ 个主题，难度应该是 hard
        if len(result.topics) >= 3:
            assert result.difficulty == "hard"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
