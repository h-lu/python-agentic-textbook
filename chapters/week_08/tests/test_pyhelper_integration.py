"""
test_pyhelper_integration.py - PyHelper 集成测试

对 PyHelper 的集成测试：
- 测试 storage 模块的读写功能
- 测试 records 模块的增删改查
- 使用 tmp_path fixture 隔离测试数据
"""

import pytest
import sys
from pathlib import Path

# 添加 examples/pyhelper 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "examples" / "pyhelper"))

from storage import save_learning_log, load_learning_log
from records import (
    add_record,
    count_study_days,
    get_records_by_mood,
    get_latest_record,
    validate_record,
)


# =====================
# 1. Storage 模块测试
# =====================

class TestStorage:
    """测试 storage 模块的文件读写功能"""

    # 测试类型: 正例
    # 覆盖场景: 正常保存和加载学习记录
    # 预期结果: 加载的数据与保存的数据一致
    def test_save_and_load_roundtrip(self, tmp_path):
        """测试保存和加载的往返"""
        file_path = tmp_path / "test_log.json"

        records = [
            {"date": "2026-02-09", "content": "学了 pytest 基础", "mood": "开心"},
            {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"},
        ]

        save_learning_log(records, file_path)
        loaded = load_learning_log(file_path)

        assert loaded == records

    # 测试类型: 正例
    # 覆盖场景: 保存空列表
    # 预期结果: 可以正常保存和加载
    def test_save_empty_list(self, tmp_path):
        """测试保存空列表"""
        file_path = tmp_path / "empty.json"

        save_learning_log([], file_path)
        loaded = load_learning_log(file_path)

        assert loaded == []

    # 测试类型: 正例
    # 覆盖场景: 保存单条记录
    # 预期结果: 数据完整保留
    def test_save_single_record(self, tmp_path):
        """测试保存单条记录"""
        file_path = tmp_path / "single.json"

        records = [{"date": "2026-02-09", "content": "今天学了 Python"}]

        save_learning_log(records, file_path)
        loaded = load_learning_log(file_path)

        assert len(loaded) == 1
        assert loaded[0]["date"] == "2026-02-09"
        assert loaded[0]["content"] == "今天学了 Python"

    # 测试类型: 边界
    # 覆盖场景: 加载不存在的文件
    # 预期结果: 返回空列表而不是报错
    def test_load_nonexistent_file(self, tmp_path):
        """测试加载不存在的文件返回空列表"""
        file_path = tmp_path / "not_exist.json"

        result = load_learning_log(file_path)

        assert result == []

    # 测试类型: 边界
    # 覆盖场景: 加载空文件
    # 预期结果: 返回空列表
    def test_load_empty_file(self, tmp_path):
        """测试加载空文件返回空列表"""
        file_path = tmp_path / "empty_file.json"
        file_path.write_text("", encoding="utf-8")

        result = load_learning_log(file_path)

        assert result == []

    # 测试类型: 边界
    # 覆盖场景: 加载只有空白字符的文件
    # 预期结果: 返回空列表
    def test_load_whitespace_only_file(self, tmp_path):
        """测试加载只有空白字符的文件"""
        file_path = tmp_path / "whitespace.json"
        file_path.write_text("   \n\n   ", encoding="utf-8")

        result = load_learning_log(file_path)

        assert result == []

    # 测试类型: 反例
    # 覆盖场景: 加载无效的 JSON 文件
    # 预期结果: 抛出 ValueError
    def test_load_invalid_json(self, tmp_path):
        """测试加载无效的 JSON 抛出异常"""
        file_path = tmp_path / "invalid.json"
        file_path.write_text("不是有效的 JSON", encoding="utf-8")

        with pytest.raises(ValueError, match="无效的 JSON"):
            load_learning_log(file_path)

    # 测试类型: 反例
    # 覆盖场景: 保存非列表数据
    # 预期结果: 抛出 TypeError
    def test_save_non_list_raises(self, tmp_path):
        """测试保存非列表数据抛出异常"""
        file_path = tmp_path / "test.json"

        with pytest.raises(TypeError, match="必须是列表"):
            save_learning_log("不是列表", file_path)

    # 测试类型: 反例
    # 覆盖场景: 保存包含非字典记录的列表
    # 预期结果: 抛出 ValueError
    def test_save_invalid_record_format(self, tmp_path):
        """测试保存无效格式的记录抛出异常"""
        file_path = tmp_path / "test.json"

        with pytest.raises(ValueError, match="必须是字典"):
            save_learning_log(["不是字典"], file_path)

    # 测试类型: 反例
    # 覆盖场景: 保存缺少必要字段的记录
    # 预期结果: 抛出 ValueError
    def test_save_missing_required_fields(self, tmp_path):
        """测试保存缺少必要字段的记录抛出异常"""
        file_path = tmp_path / "test.json"

        # 缺少 content 字段
        with pytest.raises(ValueError, match="content"):
            save_learning_log([{"date": "2026-02-09"}], file_path)

        # 缺少 date 字段
        with pytest.raises(ValueError, match="date"):
            save_learning_log([{"content": "学了 Python"}], file_path)

    # 测试类型: 正例
    # 覆盖场景: 多次保存到同一文件（覆盖写入）
    # 预期结果: 只有最后一次的数据保留
    def test_overwrite_existing_file(self, tmp_path):
        """测试覆盖已有文件"""
        file_path = tmp_path / "overwrite.json"

        save_learning_log([{"date": "2026-02-09", "content": "第一次"}], file_path)
        save_learning_log([{"date": "2026-02-10", "content": "第二次"}], file_path)

        loaded = load_learning_log(file_path)

        assert len(loaded) == 1
        assert loaded[0]["date"] == "2026-02-10"

    # 测试类型: 正例
    # 覆盖场景: 记录包含 Unicode 字符（中文、emoji）
    # 预期结果: 数据正确保存和加载
    def test_unicode_content(self, tmp_path):
        """测试 Unicode 内容"""
        file_path = tmp_path / "unicode.json"

        records = [
            {"date": "2026-02-09", "content": "学了 Python 🐍", "mood": "开心 😊"},
            {"date": "2026-02-08", "content": "中文内容测试", "mood": "兴奋"},
        ]

        save_learning_log(records, file_path)
        loaded = load_learning_log(file_path)

        assert loaded == records


# =====================
# 2. Records 模块测试
# =====================

class TestRecordsValidation:
    """测试记录验证功能"""

    # 测试类型: 正例
    # 覆盖场景: 验证有效的记录
    # 预期结果: 返回 True
    def test_validate_valid_record(self):
        """测试验证有效记录"""
        record = {"date": "2026-02-09", "content": "学了 Python"}

        result = validate_record(record)

        assert result is True

    # 测试类型: 反例
    # 覆盖场景: 验证非字典类型
    # 预期结果: 抛出 ValueError
    def test_validate_non_dict_raises(self):
        """测试验证非字典类型抛出异常"""
        with pytest.raises(ValueError, match="必须是字典"):
            validate_record("不是字典")

        with pytest.raises(ValueError, match="必须是字典"):
            validate_record(["列表"])

    # 测试类型: 反例
    # 覆盖场景: 缺少 date 字段
    # 预期结果: 抛出 ValueError
    def test_validate_missing_date_raises(self):
        """测试缺少 date 字段抛出异常"""
        with pytest.raises(ValueError, match="date"):
            validate_record({"content": "学了 Python"})

    # 测试类型: 反例
    # 覆盖场景: 缺少 content 字段
    # 预期结果: 抛出 ValueError
    def test_validate_missing_content_raises(self):
        """测试缺少 content 字段抛出异常"""
        with pytest.raises(ValueError, match="content"):
            validate_record({"date": "2026-02-09"})

    # 测试类型: 反例
    # 覆盖场景: content 为空字符串
    # 预期结果: 抛出 ValueError
    def test_validate_empty_content_raises(self):
        """测试空 content 抛出异常"""
        with pytest.raises(ValueError, match="不能为空"):
            validate_record({"date": "2026-02-09", "content": ""})

    # 测试类型: 反例
    # 覆盖场景: content 只有空格
    # 预期结果: 抛出 ValueError
    def test_validate_whitespace_content_raises(self):
        """测试只有空格的 content 抛出异常"""
        with pytest.raises(ValueError, match="不能为空"):
            validate_record({"date": "2026-02-09", "content": "   "})

    # 测试类型: 反例
    # 覆盖场景: content 超过 1000 字符
    # 预期结果: 抛出 ValueError
    def test_validate_too_long_content_raises(self):
        """测试超长 content 抛出异常"""
        with pytest.raises(ValueError, match="不能超过 1000"):
            validate_record({"date": "2026-02-09", "content": "x" * 1001})

    # 测试类型: 边界
    # 覆盖场景: content 恰好 1000 字符
    # 预期结果: 返回 True
    def test_validate_max_length_content(self):
        """测试恰好 1000 字符的 content"""
        record = {"date": "2026-02-09", "content": "x" * 1000}

        result = validate_record(record)

        assert result is True


class TestAddRecord:
    """测试添加记录功能"""

    # 测试类型: 正例
    # 覆盖场景: 向空列表添加记录
    # 预期结果: 记录被添加
    def test_add_to_empty_list(self):
        """测试向空列表添加记录"""
        records = []
        new_record = {"date": "2026-02-09", "content": "学了 pytest"}

        result = add_record(records, new_record)

        assert len(result) == 1
        assert result[0] == new_record

    # 测试类型: 正例
    # 覆盖场景: 向已有记录的列表添加
    # 预期结果: 新记录被追加到末尾
    def test_add_to_existing_list(self):
        """测试向已有列表添加记录"""
        records = [{"date": "2026-02-08", "content": "昨天学的"}]
        new_record = {"date": "2026-02-09", "content": "今天学的"}

        result = add_record(records, new_record)

        assert len(result) == 2
        assert result[-1] == new_record

    # 测试类型: 正例
    # 覆盖场景: 添加相同日期的记录（覆盖）
    # 预期结果: 原有记录被覆盖
    def test_add_duplicate_date_overwrites(self):
        """测试相同日期覆盖原有记录"""
        records = [{"date": "2026-02-09", "content": "旧内容"}]
        new_record = {"date": "2026-02-09", "content": "新内容"}

        result = add_record(records, new_record)

        assert len(result) == 1
        assert result[0]["content"] == "新内容"

    # 测试类型: 反例
    # 覆盖场景: 添加无效格式的记录
    # 预期结果: 抛出 ValueError，原列表不变
    def test_add_invalid_record_raises(self):
        """测试添加无效记录抛出异常"""
        records = []
        invalid_record = {"date": "2026-02-09"}  # 缺少 content

        with pytest.raises(ValueError):
            add_record(records, invalid_record)

        # 确保原列表未被修改
        assert len(records) == 0


class TestCountStudyDays:
    """测试统计学习天数功能"""

    # 测试类型: 正例
    # 覆盖场景: 统计不同日期的记录
    # 预期结果: 返回不重复的日期数
    def test_count_unique_dates(self):
        """测试统计不同日期"""
        records = [
            {"date": "2026-02-09", "content": "学了 pytest"},
            {"date": "2026-02-08", "content": "学了 fixture"},
            {"date": "2026-02-07", "content": "学了异常"},
        ]

        result = count_study_days(records)

        assert result == 3

    # 测试类型: 正例
    # 覆盖场景: 有重复日期的记录
    # 预期结果: 重复日期只算一天
    def test_count_with_duplicate_dates(self):
        """测试有重复日期的统计"""
        records = [
            {"date": "2026-02-09", "content": "上午学的"},
            {"date": "2026-02-09", "content": "下午学的"},
            {"date": "2026-02-08", "content": "昨天学的"},
        ]

        result = count_study_days(records)

        assert result == 2  # 2 个不同日期

    # 测试类型: 边界
    # 覆盖场景: 空列表
    # 预期结果: 返回 0
    def test_count_empty_list(self):
        """测试空列表返回 0"""
        result = count_study_days([])

        assert result == 0

    # 测试类型: 边界
    # 覆盖场景: 记录缺少 date 字段
    # 预期结果: 缺少 date 的记录被忽略
    def test_count_missing_date_ignored(self):
        """测试缺少 date 的记录被忽略"""
        records = [
            {"date": "2026-02-09", "content": "有日期的"},
            {"content": "没有日期的"},  # 缺少 date
        ]

        result = count_study_days(records)

        assert result == 1


class TestGetRecordsByMood:
    """测试按心情筛选功能"""

    # 测试类型: 正例
    # 覆盖场景: 筛选特定心情的记录
    # 预期结果: 返回符合条件的记录
    def test_filter_by_mood(self):
        """测试按心情筛选"""
        records = [
            {"date": "2026-02-09", "content": "学了 pytest", "mood": "开心"},
            {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"},
            {"date": "2026-02-07", "content": "学了异常", "mood": "开心"},
        ]

        result = get_records_by_mood(records, "开心")

        assert len(result) == 2
        assert all(r["mood"] == "开心" for r in result)

    # 测试类型: 边界
    # 覆盖场景: 没有匹配的记录
    # 预期结果: 返回空列表
    def test_filter_no_matches(self):
        """测试没有匹配的记录"""
        records = [
            {"date": "2026-02-09", "content": "学了 pytest", "mood": "开心"},
        ]

        result = get_records_by_mood(records, "不存在的心情")

        assert result == []

    # 测试类型: 边界
    # 覆盖场景: 空列表
    # 预期结果: 返回空列表
    def test_filter_empty_list(self):
        """测试空列表筛选"""
        result = get_records_by_mood([], "开心")

        assert result == []

    # 测试类型: 边界
    # 覆盖场景: 记录没有 mood 字段
    # 预期结果: 这些记录被忽略
    def test_filter_missing_mood_ignored(self):
        """测试没有 mood 字段的记录被忽略"""
        records = [
            {"date": "2026-02-09", "content": "有心情的", "mood": "开心"},
            {"date": "2026-02-08", "content": "没心情的"},  # 没有 mood
        ]

        result = get_records_by_mood(records, "开心")

        assert len(result) == 1


class TestGetLatestRecord:
    """测试获取最新记录功能"""

    # 测试类型: 正例
    # 覆盖场景: 获取最新记录
    # 预期结果: 返回日期最新的记录
    def test_get_latest(self):
        """测试获取最新记录"""
        records = [
            {"date": "2026-02-07", "content": "最早"},
            {"date": "2026-02-09", "content": "最新"},
            {"date": "2026-02-08", "content": "中间"},
        ]

        result = get_latest_record(records)

        assert result["date"] == "2026-02-09"
        assert result["content"] == "最新"

    # 测试类型: 边界
    # 覆盖场景: 空列表
    # 预期结果: 返回 None
    def test_get_latest_empty_list(self):
        """测试空列表返回 None"""
        result = get_latest_record([])

        assert result is None

    # 测试类型: 边界
    # 覆盖场景: 单条记录
    # 预期结果: 返回该记录
    def test_get_latest_single_record(self):
        """测试单条记录"""
        records = [{"date": "2026-02-09", "content": "唯一记录"}]

        result = get_latest_record(records)

        assert result["date"] == "2026-02-09"


# =====================
# 3. 集成测试
# =====================

class TestPyHelperIntegration:
    """PyHelper 模块间的集成测试"""

    # 测试类型: 正例
    # 覆盖场景: 完整的工作流程
    # 预期结果: storage 和 records 模块协同工作
    def test_full_workflow_with_storage(self, tmp_path):
        """测试完整的存储工作流程"""
        file_path = tmp_path / "workflow.json"

        # 添加记录
        records = []
        add_record(records, {"date": "2026-02-09", "content": "学了 pytest", "mood": "开心"})
        add_record(records, {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"})
        assert len(records) == 2

        # 保存到文件
        save_learning_log(records, file_path)
        assert file_path.exists()

        # 从文件加载
        loaded = load_learning_log(file_path)
        assert len(loaded) == 2

        # 统计
        days = count_study_days(loaded)
        assert days == 2

        # 筛选
        happy_records = get_records_by_mood(loaded, "开心")
        assert len(happy_records) == 1

    # 测试类型: 正例
    # 覆盖场景: 持久化和恢复
    # 预期结果: 数据在保存和加载后保持一致
    def test_persistence_and_recovery(self, tmp_path):
        """测试数据持久化和恢复"""
        file_path = tmp_path / "persistence.json"

        # 第一次会话：添加并保存
        records = []
        add_record(records, {"date": "2026-02-09", "content": "第一天"})
        save_learning_log(records, file_path)

        # 第二次会话：加载并继续添加
        loaded = load_learning_log(file_path)
        add_record(loaded, {"date": "2026-02-10", "content": "第二天"})
        save_learning_log(loaded, file_path)

        # 第三次会话：验证所有数据都在
        final = load_learning_log(file_path)
        assert len(final) == 2
        assert count_study_days(final) == 2

    # 测试类型: 边界
    # 覆盖场景: 覆盖已有记录后保存
    # 预期结果: 文件中的数据也被更新
    def test_overwrite_and_save(self, tmp_path):
        """测试覆盖记录后保存"""
        file_path = tmp_path / "overwrite.json"

        # 添加初始记录
        records = []
        add_record(records, {"date": "2026-02-09", "content": "旧内容"})
        save_learning_log(records, file_path)

        # 加载并覆盖
        loaded = load_learning_log(file_path)
        add_record(loaded, {"date": "2026-02-09", "content": "新内容"})
        save_learning_log(loaded, file_path)

        # 验证
        final = load_learning_log(file_path)
        assert len(final) == 1
        assert final[0]["content"] == "新内容"


# =====================
# 4. Fixture
# =====================

@pytest.fixture
def sample_records():
    """
    提供示例学习记录

    测试类型: 正例
    覆盖场景: 多个测试共享的预设数据
    预期结果: 返回包含三条记录的列表
    """
    return [
        {"date": "2026-02-09", "content": "学了 pytest", "mood": "开心"},
        {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"},
        {"date": "2026-02-07", "content": "学了异常处理", "mood": "兴奋"},
    ]


class TestWithFixture:
    """使用 fixture 的测试"""

    # 测试类型: 正例
    # 覆盖场景: 使用 fixture 数据测试添加记录
    # 预期结果: 新记录被正确添加
    def test_add_record_with_fixture(self, sample_records):
        """使用 fixture 测试添加记录"""
        new_record = {"date": "2026-02-10", "content": "学了 TDD", "mood": "期待"}

        result = add_record(sample_records, new_record)

        assert len(result) == 4
        assert result[-1] == new_record

    # 测试类型: 正例
    # 覆盖场景: 使用 fixture 数据测试统计
    # 预期结果: 返回正确的天数
    def test_count_days_with_fixture(self, sample_records):
        """使用 fixture 测试统计"""
        result = count_study_days(sample_records)

        assert result == 3

    # 测试类型: 正例
    # 覆盖场景: 使用 fixture 数据测试筛选
    # 预期结果: 返回符合条件的记录
    def test_filter_with_fixture(self, sample_records):
        """使用 fixture 测试筛选"""
        result = get_records_by_mood(sample_records, "开心")

        assert len(result) == 1
        assert result[0]["date"] == "2026-02-09"
