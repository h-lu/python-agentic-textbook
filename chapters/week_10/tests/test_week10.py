"""Week 10 测试：JSON 与序列化

测试范围：
1. JSON 基础操作（loads/dumps）
2. 文件读写（load/dump）
3. 序列化边界情况（嵌套结构、日期对象）
4. 异常处理（JSONDecodeError、验证失败）
5. PyHelper 功能（导入导出、数据迁移）
"""

import json
import datetime
import tempfile
import os
from pathlib import Path

import pytest


# ==================== Fixtures ====================

@pytest.fixture
def sample_note():
    """单条笔记数据"""
    return {
        "date": "2026-02-09",
        "content": "学习了 JSON 格式",
        "rating": 5,
        "tags": ["Python", "JSON"]
    }


@pytest.fixture
def sample_notes():
    """多条笔记数据"""
    return [
        {"date": "2026-02-01", "content": "学习 Python 基础", "rating": 5, "tags": ["Python"]},
        {"date": "2026-02-02", "content": "学习 JSON 格式", "rating": 4, "tags": ["Python", "JSON"]},
        {"date": "2026-02-03", "content": "练习序列化", "rating": 5, "tags": ["Python"]},
    ]


@pytest.fixture
def nested_data():
    """嵌套数据结构"""
    return {
        "user": {
            "name": "小北",
            "profile": {
                "age": 25,
                "interests": ["编程", "阅读", "音乐"]
            }
        },
        "notes": [
            {"id": 1, "content": "笔记1"},
            {"id": 2, "content": "笔记2"}
        ],
        "metadata": {
            "version": 1.0,
            "created": "2026-02-09"
        }
    }


@pytest.fixture
def temp_json_file():
    """临时 JSON 文件"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        filepath = f.name
    yield filepath
    # 清理
    if os.path.exists(filepath):
        os.unlink(filepath)


# ==================== 1. JSON 基础操作测试 ====================

class TestJsonBasicOperations:
    """测试 JSON 基础操作：loads 和 dumps"""

    def test_loads_valid_json_object(self):
        """test_loads_有效JSON对象_解析成功"""
        json_str = '{"name": "小北", "age": 25}'
        result = json.loads(json_str)
        assert result == {"name": "小北", "age": 25}
        assert isinstance(result, dict)

    def test_loads_valid_json_array(self):
        """test_loads_有效JSON数组_解析成功"""
        json_str = '[1, 2, 3, "hello"]'
        result = json.loads(json_str)
        assert result == [1, 2, 3, "hello"]
        assert isinstance(result, list)

    def test_loads_valid_json_nested(self):
        """test_loads_嵌套JSON_解析成功"""
        json_str = '{"user": {"name": "小北"}, "tags": ["a", "b"]}'
        result = json.loads(json_str)
        assert result["user"]["name"] == "小北"
        assert result["tags"] == ["a", "b"]

    def test_loads_invalid_json_single_quotes(self):
        """test_loads_单引号JSON_抛出JSONDecodeError"""
        json_str = "{'key': 'value'}"
        with pytest.raises(json.JSONDecodeError):
            json.loads(json_str)

    def test_loads_invalid_json_missing_brace(self):
        """test_loads_缺少右大括号_抛出JSONDecodeError"""
        json_str = '{"key": "value"'
        with pytest.raises(json.JSONDecodeError):
            json.loads(json_str)

    def test_loads_invalid_json_trailing_comma(self):
        """test_loads_尾随逗号_抛出JSONDecodeError"""
        json_str = '{"a": 1, "b": 2,}'
        with pytest.raises(json.JSONDecodeError):
            json.loads(json_str)

    def test_loads_empty_string(self):
        """test_loads_空字符串_抛出JSONDecodeError"""
        with pytest.raises(json.JSONDecodeError):
            json.loads("")

    def test_dumps_basic_dict(self):
        """test_dumps_基础字典_序列化成功"""
        data = {"name": "小北", "age": 25}
        result = json.dumps(data)
        assert isinstance(result, str)
        # 默认 ensure_ascii=True，中文被转义
        assert '"name":' in result
        assert '"age": 25' in result

    def test_dumps_basic_list(self):
        """test_dumps_基础列表_序列化成功"""
        data = [1, 2, 3, "hello"]
        result = json.dumps(data)
        assert result == '[1, 2, 3, "hello"]'

    def test_dumps_with_indent(self):
        """test_dumps_带缩进_格式化输出"""
        data = {"name": "小北"}
        result = json.dumps(data, indent=2)
        assert '\n' in result
        assert '  "name":' in result

    def test_dumps_ensure_ascii_true(self):
        """test_dumps_ensure_ascii为True_中文转义"""
        data = {"name": "小北"}
        result = json.dumps(data, ensure_ascii=True)
        assert '\\u' in result  # 中文字符被转义

    def test_dumps_ensure_ascii_false(self):
        """test_dumps_ensure_ascii为False_中文原样输出"""
        data = {"name": "小北"}
        result = json.dumps(data, ensure_ascii=False)
        assert '小北' in result  # 中文字符原样输出
        assert '\\u' not in result

    def test_dumps_sort_keys(self):
        """test_dumps_排序键_按键名排序输出"""
        data = {"z": 1, "a": 2, "m": 3}
        result = json.dumps(data, sort_keys=True)
        assert result == '{"a": 2, "m": 3, "z": 1}'

    def test_dumps_separators(self):
        """test_dumps_自定义分隔符_紧凑输出"""
        data = {"a": 1, "b": 2}
        result = json.dumps(data, separators=(',', ':'))
        assert result == '{"a":1,"b":2}'

    def test_roundtrip_loads_dumps(self):
        """test_roundtrip_loads_dumps_往返数据一致"""
        original = {"name": "小北", "tags": ["Python", "JSON"]}
        json_str = json.dumps(original)
        result = json.loads(json_str)
        assert result == original


# ==================== 2. 文件读写测试 ====================

class TestJsonFileOperations:
    """测试 JSON 文件读写：load 和 dump"""

    def test_dump_to_file_and_load(self, temp_json_file, sample_note):
        """test_dump_and_load_写入再读取_数据一致"""
        # 写入
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_note, f)

        # 读取
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)

        assert result == sample_note

    def test_dump_with_indent_to_file(self, temp_json_file):
        """test_dump_with_indent_格式化写入_文件可读"""
        data = {"name": "小北"}
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        with open(temp_json_file, 'r', encoding='utf-8') as f:
            content = f.read()

        assert '\n' in content
        assert '  "name":' in content

    def test_dump_chinese_preserve(self, temp_json_file):
        """test_dump_chinese_保留中文_ensure_ascii_false"""
        data = {"name": "小北", "content": "中文内容"}
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        with open(temp_json_file, 'r', encoding='utf-8') as f:
            content = f.read()

        assert '小北' in content
        assert '中文内容' in content

    def test_load_file_not_found(self):
        """test_load_文件不存在_抛出FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            with open('/nonexistent/path/file.json', 'r') as f:
                json.load(f)

    def test_load_invalid_json_file(self, temp_json_file):
        """test_load_无效JSON文件_抛出JSONDecodeError"""
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            f.write('{"invalid json')

        with pytest.raises(json.JSONDecodeError):
            with open(temp_json_file, 'r', encoding='utf-8') as f:
                json.load(f)

    def test_dump_list_to_file(self, temp_json_file, sample_notes):
        """test_dump_list_列表写入文件_读取正确"""
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_notes, f)

        with open(temp_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)

        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0]["date"] == "2026-02-01"


# ==================== 3. 序列化边界情况测试 ====================

class TestSerializationEdgeCases:
    """测试序列化边界情况"""

    def test_nested_structure_roundtrip(self, nested_data):
        """test_nested_structure_嵌套结构_往返一致"""
        json_str = json.dumps(nested_data)
        result = json.loads(json_str)
        assert result == nested_data

    def test_deeply_nested(self):
        """test_deeply_nested_深层嵌套_序列化成功"""
        data = {"level1": {"level2": {"level3": {"level4": {"value": "deep"}}}}}
        json_str = json.dumps(data)
        result = json.loads(json_str)
        assert result["level1"]["level2"]["level3"]["level4"]["value"] == "deep"

    def test_empty_containers(self):
        """test_empty_containers_空容器_序列化成功"""
        data = {"empty_dict": {}, "empty_list": [], "null": None}
        json_str = json.dumps(data)
        result = json.loads(json_str)
        assert result["empty_dict"] == {}
        assert result["empty_list"] == []
        assert result["null"] is None

    def test_date_object_not_serializable(self):
        """test_date_object_日期对象_默认不可序列化"""
        data = {"date": datetime.date(2026, 2, 9)}
        with pytest.raises(TypeError) as exc_info:
            json.dumps(data)
        assert "not JSON serializable" in str(exc_info.value)

    def test_datetime_object_not_serializable(self):
        """test_datetime_日期时间对象_默认不可序列化"""
        data = {"datetime": datetime.datetime(2026, 2, 9, 14, 30, 0)}
        with pytest.raises(TypeError):
            json.dumps(data)

    def test_custom_default_handler(self):
        """test_custom_default_自定义处理器_日期序列化成功"""
        data = {"date": datetime.date(2026, 2, 9)}

        def date_handler(obj):
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        json_str = json.dumps(data, default=date_handler)
        result = json.loads(json_str)
        assert result["date"] == "2026-02-09"

    def test_set_not_serializable(self):
        """test_set_集合对象_不可序列化"""
        data = {"tags": {"Python", "JSON"}}
        with pytest.raises(TypeError):
            json.dumps(data)

    def test_bytes_not_serializable(self):
        """test_bytes_字节对象_不可序列izable"""
        data = {"data": b"hello"}
        with pytest.raises(TypeError):
            json.dumps(data)

    def test_object_hook_deserialization(self):
        """test_object_hook_对象钩子_自定义反序列化"""
        json_str = '{"date": "2026-02-09", "name": "小北"}'

        def convert_date(dct):
            if "date" in dct:
                dct["date"] = datetime.date.fromisoformat(dct["date"])
            return dct

        result = json.loads(json_str, object_hook=convert_date)
        assert isinstance(result["date"], datetime.date)
        assert result["date"] == datetime.date(2026, 2, 9)

    def test_special_float_values(self):
        """test_special_float_特殊浮点值_序列化成功"""
        data = {"inf": float('inf'), "neg_inf": float('-inf')}
        # 默认 allow_nan=True，inf 会被序列化为 Infinity
        result = json.dumps(data)
        assert "Infinity" in result

        # allow_nan=False 时会报错
        with pytest.raises(ValueError):
            json.dumps(data, allow_nan=False)

    def test_large_number(self):
        """test_large_number_大数字_序列化成功"""
        data = {"big_int": 10**18, "big_float": 1.7976931348623157e+308}
        json_str = json.dumps(data)
        result = json.loads(json_str)
        assert result["big_int"] == 10**18


# ==================== 4. 异常处理测试 ====================

class TestJsonExceptionHandling:
    """测试 JSON 异常处理"""

    def test_jsondecodeerror_info(self):
        """test_JSONDecodeError_捕获错误_获取详细信息"""
        json_str = '{"key": "value"'
        try:
            json.loads(json_str)
            assert False, "应该抛出异常"
        except json.JSONDecodeError as e:
            assert "Expecting" in str(e) or "delimiter" in str(e)
            assert e.lineno == 1
            assert e.colno > 0

    def test_catch_specific_exception(self):
        """test_catch_specific_捕获特定异常_不捕获其他"""
        json_str = 'invalid'
        caught = False
        try:
            json.loads(json_str)
        except json.JSONDecodeError:
            caught = True
        except Exception:
            pass
        assert caught

    def test_safe_parse_with_default(self):
        """test_safe_parse_安全解析_出错返回默认值"""
        def safe_loads(json_str, default=None):
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return default

        assert safe_loads('{"valid": true}') == {"valid": True}
        assert safe_loads('invalid', {}) == {}
        assert safe_loads('invalid') is None

    def test_validate_json_type(self):
        """test_validate_type_验证JSON类型_确保结构正确"""
        json_str = '{"name": "小北"}'
        data = json.loads(json_str)
        assert isinstance(data, dict)
        assert "name" in data

        json_str = '[1, 2, 3]'
        data = json.loads(json_str)
        assert isinstance(data, list)

    def test_validate_required_fields(self):
        """test_validate_required_验证必需字段_缺失返回错误"""
        def validate(data):
            required = ["date", "content"]
            for field in required:
                if field not in data:
                    return False, f"Missing field: {field}"
            return True, None

        assert validate({"date": "2026-02-09", "content": "测试"})[0]
        assert not validate({"date": "2026-02-09"})[0]
        assert not validate({})[0]

    def test_corrupted_json_partial_recovery(self):
        """test_corrupted_json_损坏数据_尝试恢复"""
        # 模拟部分损坏的 JSON 数组
        corrupted = '[{"a": 1}, {"b": 2}'  # 缺少结尾 ]
        try:
            json.loads(corrupted)
        except json.JSONDecodeError as e:
            # 可以获取错误位置信息
            assert e.colno > 0


# ==================== 5. PyHelper 功能测试 ====================

class TestPyHelperFunctions:
    """测试 PyHelper JSON 功能"""

    def test_migrate_note_v1_to_v2_adds_tags(self):
        """test_migrate_note_v1到v2_添加tags字段"""
        # v1 格式笔记
        old_note = {"date": "2026-02-01", "content": "学习笔记"}

        # 迁移
        migrated = old_note.copy()
        if "tags" not in migrated:
            migrated["tags"] = []
        if "created_at" not in migrated:
            migrated["created_at"] = migrated.get("date", "")

        assert "tags" in migrated
        assert migrated["tags"] == []
        assert "created_at" in migrated
        assert migrated["created_at"] == "2026-02-01"

    def test_migrate_note_v2_unchanged(self):
        """test_migrate_note_v2格式_保持不变"""
        # v2 格式笔记
        note = {
            "date": "2026-02-01",
            "content": "学习笔记",
            "tags": ["Python"],
            "created_at": "2026-02-01T10:00:00"
        }

        # 迁移（已是最新格式）
        migrated = note.copy()
        if "tags" not in migrated:
            migrated["tags"] = []
        if "created_at" not in migrated:
            migrated["created_at"] = migrated.get("date", "")

        assert migrated == note

    def test_migrate_notes_batch(self, sample_notes):
        """test_migrate_notes_批量迁移_所有笔记更新"""
        # 模拟旧格式
        old_notes = [
            {"date": "2026-02-01", "content": "笔记1"},
            {"date": "2026-02-02", "content": "笔记2"},
        ]

        migrated = []
        for note in old_notes:
            m = note.copy()
            if "tags" not in m:
                m["tags"] = []
            if "created_at" not in m:
                m["created_at"] = m.get("date", "")
            migrated.append(m)

        assert all("tags" in n for n in migrated)
        assert all("created_at" in n for n in migrated)

    def test_export_notes_json_format(self, temp_json_file, sample_notes):
        """test_export_notes_json格式_导出成功"""
        # 导出为 JSON
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_notes, f, indent=2, ensure_ascii=False)

        # 验证文件内容
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)

        assert len(loaded) == 3
        assert loaded[0]["date"] == "2026-02-01"

    def test_export_notes_txt_format(self, temp_json_file, sample_notes):
        """test_export_notes_txt格式_导出成功"""
        # 导出为文本格式
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            for note in sample_notes:
                f.write(f"日期: {note.get('date', '未知')}\n")
                f.write(f"内容: {note.get('content', '')}\n")
                f.write("-" * 40 + "\n")

        # 验证文件内容
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            content = f.read()

        assert "日期: 2026-02-01" in content
        assert "内容: 学习 Python 基础" in content
        assert "-" * 40 in content

    def test_import_notes_success(self, temp_json_file, sample_notes):
        """test_import_notes_成功导入_返回笔记列表"""
        # 先导出
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_notes, f)

        # 再导入
        with open(temp_json_file, 'r', encoding='utf-8') as f:
            imported = json.load(f)

        assert len(imported) == 3
        assert imported[0]["content"] == "学习 Python 基础"

    def test_import_notes_deduplication(self, temp_json_file):
        """test_import_notes_去重_重复笔记跳过"""
        existing = [
            {"date": "2026-02-01", "content": "重复笔记", "tags": []},
            {"date": "2026-02-02", "content": "新笔记", "tags": []},
        ]

        # 要导入的数据包含重复
        to_import = [
            {"date": "2026-02-01", "content": "重复笔记", "tags": []},
            {"date": "2026-02-03", "content": "另一个新笔记", "tags": []},
        ]

        # 模拟导入去重逻辑
        existing_keys = {(n.get("date"), n.get("content")) for n in existing}
        added = 0
        for note in to_import:
            key = (note.get("date"), note.get("content"))
            if key not in existing_keys:
                existing.append(note)
                existing_keys.add(key)
                added += 1

        assert added == 1
        assert len(existing) == 3

    def test_import_notes_file_not_found(self):
        """test_import_notes_文件不存在_抛出FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            with open('/nonexistent/notes.json', 'r') as f:
                json.load(f)

    def test_import_notes_invalid_json(self, temp_json_file):
        """test_import_notes_无效JSON_抛出JSONDecodeError"""
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            f.write('not valid json')

        with pytest.raises(json.JSONDecodeError):
            with open(temp_json_file, 'r', encoding='utf-8') as f:
                json.load(f)

    def test_import_notes_wrong_structure(self, temp_json_file):
        """test_import_notes_错误结构_返回错误提示"""
        # 写入非数组数据
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump({"not": "a list"}, f)

        with open(temp_json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 验证结构
        assert not isinstance(data, list)
        assert isinstance(data, dict)

    def test_detect_version_v1(self):
        """test_detect_version_v1格式_返回版本1"""
        notes = [
            {"date": "2026-02-01", "content": "笔记1"},  # 无 tags
        ]
        # 检测逻辑：检查第一条笔记是否有 tags 字段
        version = 2 if notes and "tags" in notes[0] else 1
        assert version == 1

    def test_detect_version_v2(self, sample_notes):
        """test_detect_version_v2格式_返回版本2"""
        version = 2 if sample_notes and "tags" in sample_notes[0] else 1
        assert version == 2

    def test_detect_version_empty(self):
        """test_detect_version_空列表_返回版本2"""
        notes = []
        version = 2 if not notes or "tags" in notes[0] else 1
        # 空列表默认视为最新版本
        version = 2 if not notes else (2 if "tags" in notes[0] else 1)
        assert version == 2

    def test_validate_note_valid(self):
        """test_validate_note_有效笔记_验证通过"""
        note = {"date": "2026-02-01", "content": "有效笔记", "tags": []}
        is_valid = "date" in note and "content" in note
        assert is_valid

    def test_validate_note_missing_date(self):
        """test_validate_note_缺少日期_验证失败"""
        note = {"content": "缺少日期", "tags": []}
        is_valid = "date" in note and "content" in note
        assert not is_valid

    def test_validate_note_missing_content(self):
        """test_validate_note_缺少内容_验证失败"""
        note = {"date": "2026-02-01", "tags": []}
        is_valid = "date" in note and "content" in note
        assert not is_valid

    def test_filter_valid_notes(self, sample_notes):
        """test_filter_valid_notes_过滤无效笔记_保留有效"""
        mixed_notes = [
            {"date": "2026-02-01", "content": "有效笔记1", "tags": []},
            {"date": "2026-02-02"},  # 无效：缺少 content
            {"content": "无效笔记"},  # 无效：缺少 date
            {"date": "2026-02-03", "content": "有效笔记2", "tags": []},
        ]

        valid = [n for n in mixed_notes if "date" in n and "content" in n]
        assert len(valid) == 2
        assert valid[0]["content"] == "有效笔记1"
        assert valid[1]["content"] == "有效笔记2"


# ==================== 6. 编码处理测试 ====================

class TestEncodingHandling:
    """测试编码处理"""

    def test_utf8_encoding(self, temp_json_file):
        """test_utf8_编码处理_中文正常"""
        data = {"name": "小北", "content": "中文测试"}
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        with open(temp_json_file, 'r', encoding='utf-8') as f:
            result = json.load(f)

        assert result["name"] == "小北"
        assert result["content"] == "中文测试"

    def test_utf8_with_bom(self, temp_json_file):
        """test_utf8_bom_UTF8带BOM_正常读取"""
        # 写入带 BOM 的 UTF-8 文件
        data = {"key": "value"}
        with open(temp_json_file, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f)

        # 尝试用 utf-8 读取（应该失败或需要处理 BOM）
        with open(temp_json_file, 'rb') as f:
            raw = f.read()
        assert raw.startswith(b'\xef\xbb\xbf')  # BOM 标记

        # 用 utf-8-sig 正确读取
        with open(temp_json_file, 'r', encoding='utf-8-sig') as f:
            result = json.load(f)
        assert result["key"] == "value"

    def test_try_multiple_encodings(self, temp_json_file):
        """test_multiple_encodings_尝试多种编码_成功读取"""
        data = {"name": "测试"}
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

        # 尝试多种编码读取
        encodings = ["utf-8", "utf-8-sig", "gbk", "latin-1"]
        result = None
        for enc in encodings:
            try:
                with open(temp_json_file, 'r', encoding=enc) as f:
                    result = json.load(f)
                break
            except UnicodeDecodeError:
                continue

        assert result is not None
        assert result["name"] == "测试"


# ==================== 参数化测试 ====================

@pytest.mark.parametrize(
    "input_data,expected_str",
    [
        ({"a": 1}, '{"a": 1}'),
        ([1, 2, 3], "[1, 2, 3]"),
        ("hello", '"hello"'),
        (123, "123"),
        (True, "true"),
        (None, "null"),
    ],
)
def test_dumps_various_types(input_data, expected_str):
    """参数化测试：各种数据类型的序列化"""
    result = json.dumps(input_data)
    assert result == expected_str


@pytest.mark.parametrize(
    "json_str,expected",
    [
        ('{"a": 1}', {"a": 1}),
        ("[1, 2, 3]", [1, 2, 3]),
        ('"hello"', "hello"),
        ("123", 123),
        ("true", True),
        ("null", None),
    ],
)
def test_loads_various_types(json_str, expected):
    """参数化测试：各种 JSON 类型的反序列化"""
    result = json.loads(json_str)
    assert result == expected


@pytest.mark.parametrize(
    "invalid_json",
    [
        "{}",  # 空对象，不是数组
        "\"string\"",  # 字符串
        "123",  # 数字
        "null",  # null
    ],
)
def test_import_expects_array_but_gets_other(invalid_json):
    """参数化测试：期望数组但得到其他类型"""
    data = json.loads(invalid_json)
    assert not isinstance(data, list)
