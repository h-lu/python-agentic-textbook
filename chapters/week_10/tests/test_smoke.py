"""Week 10 冒烟测试 - 基础功能检查"""

import json
import tempfile
import os


def test_json_basic_roundtrip():
    """基础 JSON 序列化和反序列化"""
    data = {"name": "test", "value": 42}
    json_str = json.dumps(data)
    result = json.loads(json_str)
    assert result == data


def test_json_file_operations():
    """JSON 文件读写"""
    data = [1, 2, 3, "hello"]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        filepath = f.name
        json.dump(data, f)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            result = json.load(f)
        assert result == data
    finally:
        os.unlink(filepath)


def test_json_exception_handling():
    """JSON 异常处理"""
    try:
        json.loads('{"invalid')
        assert False, "应该抛出异常"
    except json.JSONDecodeError:
        pass  # 预期行为


def test_chinese_encoding():
    """中文编码处理"""
    data = {"name": "小北", "content": "中文测试"}
    json_str = json.dumps(data, ensure_ascii=False)
    assert "小北" in json_str
    assert "中文测试" in json_str


def test_nested_structure():
    """嵌套数据结构"""
    data = {
        "level1": {
            "level2": {
                "value": "deep"
            }
        }
    }
    json_str = json.dumps(data)
    result = json.loads(json_str)
    assert result["level1"]["level2"]["value"] == "deep"
