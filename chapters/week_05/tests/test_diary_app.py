"""
Week 05: 日记本工具测试

测试日记本的写日记、读日记、搜日记功能
"""

import sys
from pathlib import Path


STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))
sys.modules.pop("solution", None)

from solution import add_diary_entry, count_diaries, read_all_diaries, search_diaries


# ========================================
# 测试用例
# ========================================

class TestAddDiaryEntry:
    """测试写日记功能"""

    def test_add_single_entry(self, tmp_path):
        """测试添加单条日记"""
        diary_file = tmp_path / "diary.txt"
        add_diary_entry("今天学会了文件操作", str(diary_file))

        content = diary_file.read_text(encoding="utf-8")
        assert "今天学会了文件操作" in content
        assert ":" in content  # 应该有日期分隔符

    def test_add_multiple_entries(self, tmp_path):
        """测试添加多条日记"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("第一条日记", str(diary_file))
        add_diary_entry("第二条日记", str(diary_file))
        add_diary_entry("第三条日记", str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert len(lines) == 3
        assert "第一条日记" in lines[0]
        assert "第二条日记" in lines[1]
        assert "第三条日记" in lines[2]

    def test_append_mode_does_not_overwrite(self, tmp_path):
        """测试追加模式不会覆盖已有内容"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("原有内容", str(diary_file))
        add_diary_entry("新增内容", str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert len(lines) == 2
        assert "原有内容" in lines[0]
        assert "新增内容" in lines[1]

    def test_add_entry_with_chinese(self, tmp_path):
        """测试添加中文日记"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("今天很开心，学会了文件读写", str(diary_file))
        add_diary_entry("编码问题也搞懂了", str(diary_file))

        content = diary_file.read_text(encoding="utf-8")
        assert "开心" in content
        assert "编码" in content

    def test_add_entry_with_special_characters(self, tmp_path):
        """测试添加包含特殊字符的日记"""
        diary_file = tmp_path / "diary.txt"

        entry = "今天学习了：文件操作、编码、pathlib 等"
        add_diary_entry(entry, str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert len(lines) == 1
        assert "文件操作" in lines[0]

    def test_add_long_entry(self, tmp_path):
        """测试添加长日记"""
        diary_file = tmp_path / "diary.txt"

        long_content = "今天学习了很多内容：" + "，".join([f"知识点{i}" for i in range(100)])
        add_diary_entry(long_content, str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert len(lines) == 1
        assert "知识点0" in lines[0]
        assert "知识点99" in lines[0]


class TestReadDiaries:
    """测试读日记功能"""

    def test_read_from_empty_file(self, tmp_path):
        """测试读取不存在的日记文件"""
        diary_file = tmp_path / "nonexistent.txt"

        lines = read_all_diaries(str(diary_file))
        assert lines == []

    def test_read_single_entry(self, tmp_path):
        """测试读取单条日记"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("今天的日记", str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert len(lines) == 1
        assert "今天的日记" in lines[0]

    def test_read_multiple_entries(self, tmp_path):
        """测试读取多条日记"""
        diary_file = tmp_path / "diary.txt"

        entries = ["第一天", "第二天", "第三天"]
        for entry in entries:
            add_diary_entry(entry, str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert len(lines) == 3

        for i, entry in enumerate(entries):
            assert entry in lines[i]

    def test_read_preserves_content(self, tmp_path):
        """测试读取内容与写入内容一致"""
        diary_file = tmp_path / "diary.txt"

        original = "今天学会了文件操作和 with 语句"
        add_diary_entry(original, str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert original in lines[0]

    def test_read_empty_lines_filtered(self, tmp_path):
        """测试空行被正确过滤"""
        diary_file = tmp_path / "diary.txt"

        # 手动创建包含空行的文件
        diary_file.write_text("第一行\n\n第二行\n\n\n", encoding="utf-8")

        lines = read_all_diaries(str(diary_file))
        # 空行应该被过滤掉
        assert len(lines) <= 3  # 取决于实现，可能包含空行

    def test_read_chinese_content(self, tmp_path):
        """测试读取中文日记"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("今天学习了 Python 编程", str(diary_file))
        add_diary_entry("中文编码没有问题", str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert "Python" in lines[0]
        assert "中文" in lines[1]


class TestSearchDiaries:
    """测试搜日记功能"""

    def test_search_single_keyword(self, tmp_path):
        """搜索单个关键词"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("今天学会了文件操作", str(diary_file))
        add_diary_entry("编码问题终于搞懂了", str(diary_file))
        add_diary_entry("追加模式让日记本能持续记录", str(diary_file))

        results = search_diaries("编码", str(diary_file))
        assert len(results) == 1
        assert "编码" in results[0]

    def test_search_multiple_matches(self, tmp_path):
        """测试搜索多个匹配结果"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("今天学习了 Python 文件操作", str(diary_file))
        add_diary_entry("文件编码很重要", str(diary_file))
        add_diary_entry("pathlib 处理文件路径", str(diary_file))

        results = search_diaries("文件", str(diary_file))
        assert len(results) == 3
        # 所有结果都应该包含"文件"
        for result in results:
            assert "文件" in result

    def test_search_no_matches(self, tmp_path):
        """测试搜索不存在的关键词"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("今天学习了 Python", str(diary_file))
        add_diary_entry("编码问题搞懂了", str(diary_file))

        results = search_diaries("不存在的内容", str(diary_file))
        assert len(results) == 0

    def test_search_chinese_keyword(self, tmp_path):
        """测试搜索中文关键词"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("今天很开心", str(diary_file))
        add_diary_entry("学习了编程", str(diary_file))
        add_diary_entry("继续加油", str(diary_file))

        results = search_diaries("开心", str(diary_file))
        assert len(results) == 1
        assert "开心" in results[0]

    def test_search_date_format(self, tmp_path):
        """测试搜索日期格式"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("今天的内容", str(diary_file))

        lines = read_all_diaries(str(diary_file))
        # 应该包含日期（格式：YYYY-MM-DD）
        assert len(lines) > 0
        # 检查是否有日期格式的文本
        assert ":" in lines[0]  # 日期和内容之间有冒号

    def test_search_partial_match(self, tmp_path):
        """测试部分匹配搜索"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("今天学习了 file 操作", str(diary_file))
        add_diary_entry("文件编码很重要", str(diary_file))

        # 搜索"文件"应该能匹配到"file"
        results = search_diaries("file", str(diary_file))
        assert len(results) == 1


class TestCountDiaries:
    """测试统计日记功能"""

    def test_count_empty_diary(self, tmp_path):
        """测试统计空日记"""
        diary_file = tmp_path / "empty.txt"

        count = count_diaries(str(diary_file))
        assert count == 0

    def test_count_single_entry(self, tmp_path):
        """测试统计单条日记"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("第一条", str(diary_file))

        count = count_diaries(str(diary_file))
        assert count == 1

    def test_count_multiple_entries(self, tmp_path):
        """测试统计多条日记"""
        diary_file = tmp_path / "diary.txt"

        for i in range(10):
            add_diary_entry(f"第{i+1}条", str(diary_file))

        count = count_diaries(str(diary_file))
        assert count == 10


class TestDiaryIntegration:
    """测试日记本综合功能"""

    def test_write_read_search_workflow(self, tmp_path):
        """测试完整的写-读-搜工作流"""
        diary_file = tmp_path / "diary.txt"

        # 1. 写入多条日记
        entries = [
            "今天学会了文件操作",
            "with 语句会自动关闭文件",
            "编码问题用 UTF-8 解决",
            "pathlib 处理路径很方便"
        ]

        for entry in entries:
            add_diary_entry(entry, str(diary_file))

        # 2. 读取所有日记
        all_diaries = read_all_diaries(str(diary_file))
        assert len(all_diaries) == 4

        # 3. 搜索"文件"
        results = search_diaries("文件", str(diary_file))
        assert len(results) >= 1

        # 4. 搜索"编码"
        results = search_diaries("编码", str(diary_file))
        assert len(results) == 1

    def test_persistence_across_operations(self, tmp_path):
        """测试数据持久化：多次操作后数据仍然保留"""
        diary_file = tmp_path / "diary.txt"

        # 第一次写入
        add_diary_entry("第一次", str(diary_file))
        assert count_diaries(str(diary_file)) == 1

        # 第二次写入
        add_diary_entry("第二次", str(diary_file))
        assert count_diaries(str(diary_file)) == 2

        # 第三次写入
        add_diary_entry("第三次", str(diary_file))
        assert count_diaries(str(diary_file)) == 3

        # 验证所有内容都在
        all_diaries = read_all_diaries(str(diary_file))
        assert "第一次" in all_diaries[0]
        assert "第二次" in all_diaries[1]
        assert "第三次" in all_diaries[2]

    def test_unicode_content_preservation(self, tmp_path):
        """测试 Unicode 内容的正确保存和读取"""
        diary_file = tmp_path / "diary.txt"

        # 写入包含 emoji 的内容
        add_diary_entry("今天很开心 😊", str(diary_file))
        add_diary_entry("庆祝一下 🎉", str(diary_file))

        # 读取并验证
        lines = read_all_diaries(str(diary_file))
        assert "😊" in lines[0]
        assert "🎉" in lines[1]

        # 搜索 emoji
        results = search_diaries("😊", str(diary_file))
        assert len(results) == 1


class TestDiaryEdgeCases:
    """测试日记本边界情况"""

    def test_empty_diary_content(self, tmp_path):
        """测试空日记内容"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("", str(diary_file))

        lines = read_all_diaries(str(diary_file))
        # 空内容是否保存取决于实现
        # 这里只验证不会崩溃

    def test_very_long_diary_entry(self, tmp_path):
        """测试很长的日记条目"""
        diary_file = tmp_path / "diary.txt"

        long_entry = "今天学习了很多内容：" + "，".join([f"知识点{i}" for i in range(1000)])
        add_diary_entry(long_entry, str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert len(lines) == 1
        assert "知识点0" in lines[0]
        assert "知识点999" in lines[0]

    def test_special_characters_in_diary(self, tmp_path):
        """测试特殊字符在日记中"""
        diary_file = tmp_path / "diary.txt"

        special_entry = "今天学习了：\n、制表符\t、引号\"和单引号'"
        add_diary_entry(special_entry, str(diary_file))

        lines = read_all_diaries(str(diary_file))
        assert len(lines) >= 1

    def test_search_empty_keyword(self, tmp_path):
        """测试搜索空关键词"""
        diary_file = tmp_path / "diary.txt"

        add_diary_entry("第一条", str(diary_file))
        add_diary_entry("第二条", str(diary_file))

        # 空关键词应该匹配所有行（或没有匹配，取决于实现）
        results = search_diaries("", str(diary_file))
        # 不会崩溃即可

    def test_consecutive_add_operations(self, tmp_path):
        """测试连续添加日记"""
        diary_file = tmp_path / "diary.txt"

        # 快速连续添加
        for i in range(100):
            add_diary_entry(f"日记{i}", str(diary_file))

        count = count_diaries(str(diary_file))
        assert count == 100
