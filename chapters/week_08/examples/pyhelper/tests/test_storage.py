"""
storage.py 的 pytest 测试

本测试文件演示：
1. 使用 tmp_path fixture 进行文件操作测试
2. 测试正常路径和异常情况
3. 验证数据完整性

运行方式：
  cd chapters/week_08/examples/pyhelper
  pytest tests/test_storage.py -v

预期输出：
  所有测试通过（绿色小点）
"""

import pytest
from pathlib import Path

# 导入被测模块
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from storage import save_learning_log, load_learning_log


def test_save_and_load_learning_log(tmp_path):
    """
    测试保存和加载学习记录

    使用 pytest 内置的 tmp_path fixture，
    它提供一个临时目录，测试结束后自动清理。
    """
    file_path = tmp_path / "test_log.json"

    records = [
        {"date": "2026-02-09", "content": "学了 pytest 基础", "mood": "开心"},
        {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"}
    ]

    # 保存
    result = save_learning_log(records, file_path)
    assert result == True

    # 加载
    loaded = load_learning_log(file_path)

    # 验证数据完整性
    assert loaded == records
    assert len(loaded) == 2
    assert loaded[0]["date"] == "2026-02-09"
    assert loaded[1]["mood"] == "困惑"


def test_load_nonexistent_file(tmp_path):
    """测试加载不存在的文件返回空列表"""
    file_path = tmp_path / "not_exist.json"

    result = load_learning_log(file_path)

    assert result == []


def test_load_empty_file(tmp_path):
    """测试加载空文件返回空列表"""
    file_path = tmp_path / "empty.json"
    file_path.write_text("", encoding="utf-8")

    result = load_learning_log(file_path)

    assert result == []


def test_save_invalid_type(tmp_path):
    """测试保存非列表类型应该抛出 TypeError"""
    file_path = tmp_path / "invalid.json"

    with pytest.raises(TypeError):
        save_learning_log("不是列表", file_path)


def test_save_invalid_record_format(tmp_path):
    """测试保存格式错误的记录应该抛出 ValueError"""
    file_path = tmp_path / "invalid.json"

    # 缺少 content 字段
    invalid_records = [{"date": "2026-02-09"}]

    with pytest.raises(ValueError):
        save_learning_log(invalid_records, file_path)


@pytest.mark.parametrize("record_count", [0, 1, 5, 10])
def test_save_various_record_counts(tmp_path, record_count):
    """测试保存不同数量的记录"""
    file_path = tmp_path / "test.json"

    records = [
        {"date": f"2026-02-{i+1:02d}", "content": f"学习内容{i}", "mood": "开心"}
        for i in range(record_count)
    ]

    save_learning_log(records, file_path)
    loaded = load_learning_log(file_path)

    assert len(loaded) == record_count
    if record_count > 0:
        assert loaded[0]["date"] == "2026-02-01"


# 反例：不使用 tmp_path 的问题
def test_without_tmp_path_problem():
    """
    反例：不使用 tmp_path 的问题

    如果直接写入真实文件系统：
    1. 测试后留下垃圾文件
    2. 并行测试可能互相干扰
    3. 清理逻辑复杂且容易遗漏

    # 不好的做法：
    # file_path = Path("/tmp/test_file.json")  # 硬编码路径
    # save_learning_log(records, file_path)
    # 测试结束后还要手动删除文件

    # 好的做法：使用 tmp_path fixture
    # 临时文件自动管理，测试隔离性好
    """
    pass  # 这是一个文档化的反例
