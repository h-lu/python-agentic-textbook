"""Week 09 测试：文本处理与正则表达式

测试范围：
1. 字符串方法（strip, find）
2. split 和 join
3. 正则表达式（re 模块）
4. 日志分析器（贯穿案例）
5. PyHelper 文本工具
"""

import pytest
import re
from datetime import datetime


# ==================== 1. 字符串方法测试 ====================

class TestStringMethods:
    """测试字符串方法"""

    def test_strip_whitespace(self):
        """测试 strip 去除空白字符（正例）"""
        text = "  hello world  \n\t"
        result = text.strip()
        assert result == "hello world"
        # 原字符串不变
        assert text == "  hello world  \n\t"

    def test_strip_custom_chars(self):
        """测试 strip 去除自定义字符（正例）"""
        assert "[ERROR]".strip("[]") == "ERROR"
        assert "---hello---".strip("-") == "hello"
        assert "###Python###".strip("#") == "Python"

    def test_strip_edge_cases(self):
        """测试 strip 边界情况"""
        # 空字符串
        assert "".strip() == ""
        # 全是空白
        assert "   ".strip() == ""
        # 无空白
        assert "hello".strip() == "hello"
        # 仅头部或尾部
        assert "  hello".strip() == "hello"
        assert "hello  ".strip() == "hello"

    def test_find_substring(self):
        """测试 find 查找子串（正例）"""
        text = "[2026-02-09 14:32:01] ERROR: 数据库连接超时"
        assert text.find("]") == 20
        # 第一个冒号在时间戳里（索引 14），日志级别后的冒号在索引 28
        assert text.find(":") == 14  # 第一个冒号在 "2026-02-09 14:32:01" 中
        assert text.find("ERROR") == 22
        # 从指定位置开始查找冒号
        assert text.find(":", 21) == 27  # 从右方括号后开始找，找到日志级别后的冒号

    def test_find_not_found(self):
        """测试 find 找不到时返回 -1（反例）"""
        text = "hello world"
        assert text.find("xyz") == -1
        assert text.find("") == 0  # 空字符串返回 0

    def test_find_with_start_index(self):
        """测试 find 指定起始位置"""
        text = "hello hello world"
        assert text.find("hello") == 0
        assert text.find("hello", 1) == 6  # 从索引 1 开始查找
        assert text.find("hello", 7) == -1


# ==================== 2. split 和 join 测试 ====================

class TestSplitAndJoin:
    """测试 split 和 join 方法"""

    def test_split_by_separator(self):
        """测试按分隔符拆分（正例）"""
        line = "2026-02-09,192.168.1.1,GET,/api/users,200"
        parts = line.split(",")
        assert parts == ["2026-02-09", "192.168.1.1", "GET", "/api/users", "200"]

    def test_split_whitespace(self):
        """测试按空白字符拆分"""
        text = "hello   world\tpython\n"
        parts = text.split()
        assert parts == ["hello", "world", "python"]

    def test_split_maxsplit(self):
        """测试 maxsplit 参数（边界）"""
        text = "a,b,c,d,e"
        # 不限制拆分次数
        assert text.split(",") == ["a", "b", "c", "d", "e"]
        # 最多拆分 1 次
        assert text.split(",", 1) == ["a", "b,c,d,e"]
        # 最多拆分 2 次
        assert text.split(",", 2) == ["a", "b", "c,d,e"]

    def test_split_edge_cases(self):
        """测试 split 边界情况"""
        # 空字符串
        assert "".split(",") == [""]
        # 分隔符在末尾
        assert "a,b,".split(",") == ["a", "b", ""]
        # 分隔符在开头
        assert ",a,b".split(",") == ["", "a", "b"]
        # 没有分隔符
        assert "hello".split(",") == ["hello"]

    def test_partition(self):
        """测试 partition 方法（正例）"""
        text = "key=value"
        result = text.partition("=")
        assert result == ("key", "=", "value")

    def test_partition_multiple_separators(self):
        """测试 partition 只拆一次（边界）"""
        text = "key=value=extra"
        # partition 只拆一次
        result = text.partition("=")
        assert result == ("key", "=", "value=extra")
        # split 会拆所有
        assert text.split("=") == ["key", "value", "extra"]

    def test_partition_not_found(self):
        """测试 partition 找不到分隔符"""
        text = "keyvalue"
        result = text.partition("=")
        assert result == ("keyvalue", "", "")

    def test_join_strings(self):
        """测试 join 方法（正例）"""
        words = ["hello", "world", "python"]
        assert " ".join(words) == "hello world python"
        assert ",".join(words) == "hello,world,python"
        assert "-".join(words) == "hello-world-python"

    def test_join_empty_list(self):
        """测试 join 空列表（边界）"""
        assert "".join([]) == ""
        assert ",".join([]) == ""

    def test_join_single_element(self):
        """测试 join 单元素列表（边界）"""
        assert ",".join(["hello"]) == "hello"


# ==================== 3. 正则表达式测试 ====================

class TestRegularExpressions:
    """测试正则表达式功能"""

    def test_re_search(self):
        """测试 re.search 基本用法（正例）"""
        pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        text = "[2026-02-09 14:32:01] 192.168.1.1 - GET /api/users 200"
        match = re.search(pattern, text)
        assert match is not None
        assert match.group() == "192.168.1.1"

    def test_re_search_not_found(self):
        """测试 re.search 找不到匹配（反例）"""
        pattern = r"\d+"
        text = "hello world"
        match = re.search(pattern, text)
        assert match is None

    def test_re_match_vs_search(self):
        """测试 match 和 search 的区别"""
        pattern = r"\d+"
        # match 只从开头匹配
        assert re.match(pattern, "123abc") is not None
        assert re.match(pattern, "abc123") is None
        # search 扫描整个字符串
        assert re.search(pattern, "123abc") is not None
        assert re.search(pattern, "abc123") is not None

    def test_re_findall(self):
        """测试 findall 返回所有匹配（正例）"""
        pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        text = """
        [2026-02-09 14:32:01] 192.168.1.1 - GET /api/users 200
        [2026-02-09 14:32:10] 192.168.1.2 - POST /api/login 200
        """
        ips = re.findall(pattern, text)
        assert ips == ["192.168.1.1", "192.168.1.2"]

    def test_re_findall_empty(self):
        """测试 findall 无匹配时返回空列表"""
        pattern = r"\d+"
        text = "hello world"
        result = re.findall(pattern, text)
        assert result == []

    def test_re_groups(self):
        """测试分组提取（正例）"""
        log_line = "192.168.1.1 - GET /api/users 200"
        pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\w+) (/\S+) (\d{3})"
        match = re.search(pattern, log_line)
        assert match is not None
        assert match.group(0) == "192.168.1.1 - GET /api/users 200"
        assert match.group(1) == "192.168.1.1"
        assert match.group(2) == "GET"
        assert match.group(3) == "/api/users"
        assert match.group(4) == "200"

    def test_re_groups_named(self):
        """测试命名分组"""
        log_line = "GET /api/users 200"
        pattern = r"(?P<method>\w+) (?P<path>/\S+) (?P<status>\d{3})"
        match = re.search(pattern, log_line)
        assert match is not None
        assert match.group("method") == "GET"
        assert match.group("path") == "/api/users"
        assert match.group("status") == "200"
        assert match.groupdict() == {"method": "GET", "path": "/api/users", "status": "200"}

    def test_re_sub(self):
        """测试替换功能（正例）"""
        log_line = "用户 192.168.1.1 访问了 /api/users"
        masked = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "***.***.***.***", log_line)
        assert masked == "用户 ***.***.***.*** 访问了 /api/users"

    def test_re_sub_with_count(self):
        """测试替换次数限制"""
        text = "192.168.1.1 and 10.0.0.1"
        # 只替换第一个
        result = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "***", text, count=1)
        assert result == "*** and 10.0.0.1"

    def test_re_raw_string(self):
        """测试原始字符串的使用"""
        # 原始字符串中 \d 就是反斜杠加 d
        pattern1 = r"\d+"
        # 普通字符串需要写 \\d
        pattern2 = "\\d+"
        text = "123"
        assert re.search(pattern1, text) is not None
        assert re.search(pattern2, text) is not None


# ==================== 4. 日志分析器测试（贯穿案例） ====================

def parse_log_line(line):
    """解析单行日志，返回字典"""
    bracket_end = line.find("]")
    if bracket_end == -1:
        return None

    # 从右方括号之后开始查找冒号（避免匹配时间戳中的冒号）
    colon_pos = line.find(":", bracket_end + 1)
    if colon_pos == -1:
        return None

    timestamp = line[1:bracket_end]
    level = line[bracket_end + 2 : colon_pos].strip()
    message = line[colon_pos + 2 :]

    return {"timestamp": timestamp, "level": level, "message": message}


def extract_ip_address(line):
    """从日志行中提取 IP 地址"""
    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    match = re.search(pattern, line)
    if match:
        return match.group()
    return None


def filter_logs_by_level(log_lines, level):
    """按日志级别过滤"""
    results = []
    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed and parsed["level"] == level:
            results.append(parsed)
    return results


def analyze_log_file(log_lines):
    """分析日志文件，统计每个 IP 的访问次数和错误数"""
    from collections import defaultdict

    ip_counter = defaultdict(lambda: {"total": 0, "errors": 0})
    pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\w+) (/\S+) (\d{3})"

    for line in log_lines:
        match = re.search(pattern, line)
        if match:
            ip, method, path, status = match.groups()
            ip_counter[ip]["total"] += 1
            if status.startswith("4") or status.startswith("5"):
                ip_counter[ip]["errors"] += 1

    return dict(ip_counter)


class TestLogAnalyzer:
    """测试日志分析器功能"""

    def test_parse_log_line_success(self):
        """测试解析单行日志成功（正例）"""
        log = "[2026-02-09 14:32:01] ERROR: 数据库连接超时"
        result = parse_log_line(log)
        assert result == {
            "timestamp": "2026-02-09 14:32:01",
            "level": "ERROR",
            "message": "数据库连接超时",
        }

    def test_parse_log_line_different_levels(self):
        """测试解析不同日志级别"""
        # INFO 级别
        log_info = "[2026-02-09 14:32:02] INFO: 用户登录成功"
        result = parse_log_line(log_info)
        assert result["level"] == "INFO"

        # WARNING 级别（带空格）
        log_warn = "[2026-02-09 14:32:03]  WARNING : 磁盘空间不足"
        result = parse_log_line(log_warn)
        assert result["level"] == "WARNING"

    def test_parse_log_line_invalid_format(self):
        """测试解析格式错误的日志（反例）"""
        # 缺少方括号
        assert parse_log_line("2026-02-09 ERROR: 消息") is None
        # 缺少冒号
        assert parse_log_line("[2026-02-09] ERROR 消息") is None
        # 空字符串
        assert parse_log_line("") is None

    def test_extract_ip_address_success(self):
        """测试提取 IP 地址成功（正例）"""
        line = "[2026-02-09 14:32:01] 192.168.1.1 - GET /api/users 200"
        assert extract_ip_address(line) == "192.168.1.1"

    def test_extract_ip_address_various_formats(self):
        """测试提取不同格式的 IP"""
        assert extract_ip_address("10.0.0.1") == "10.0.0.1"
        assert extract_ip_address("255.255.255.255") == "255.255.255.255"
        assert extract_ip_address("127.0.0.1") == "127.0.0.1"

    def test_extract_ip_address_not_found(self):
        """测试提取 IP 地址失败（反例）"""
        assert extract_ip_address("hello world") is None
        assert extract_ip_address("192.168.1") is None  # 不完整
        assert extract_ip_address("") is None

    def test_filter_logs_by_level(self):
        """测试按日志级别过滤（正例）"""
        logs = [
            "[2026-02-09 14:32:01] ERROR: 数据库连接超时",
            "[2026-02-09 14:32:02] INFO: 用户登录成功",
            "[2026-02-09 14:32:03] ERROR: 磁盘空间不足",
            "[2026-02-09 14:32:04] DEBUG: 调试信息",
        ]
        errors = filter_logs_by_level(logs, "ERROR")
        assert len(errors) == 2
        assert errors[0]["message"] == "数据库连接超时"
        assert errors[1]["message"] == "磁盘空间不足"

    def test_filter_logs_by_level_empty(self):
        """测试过滤空列表（边界）"""
        assert filter_logs_by_level([], "ERROR") == []

    def test_filter_logs_by_level_no_match(self):
        """测试过滤无匹配结果（反例）"""
        logs = [
            "[2026-02-09 14:32:01] INFO: 用户登录成功",
            "[2026-02-09 14:32:02] DEBUG: 调试信息",
        ]
        assert filter_logs_by_level(logs, "ERROR") == []

    def test_analyze_log_file(self):
        """测试完整分析功能（正例）"""
        logs = [
            "192.168.1.1 - GET /api/users 200",
            "192.168.1.2 - POST /api/login 200",
            "192.168.1.1 - GET /api/products 404",
            "192.168.1.1 - DELETE /api/users/123 403",
            "192.168.1.3 - GET /api/admin 500",
        ]
        stats = analyze_log_file(logs)
        assert stats["192.168.1.1"] == {"total": 3, "errors": 2}
        assert stats["192.168.1.2"] == {"total": 1, "errors": 0}
        assert stats["192.168.1.3"] == {"total": 1, "errors": 1}

    def test_analyze_log_file_empty(self):
        """测试分析空日志（边界）"""
        assert analyze_log_file([]) == {}

    def test_analyze_log_file_no_match(self):
        """测试分析无匹配格式的日志（反例）"""
        logs = [
            "这是普通文本",
            "[2026-02-09] INFO: 消息",
        ]
        assert analyze_log_file(logs) == {}


# ==================== 5. PyHelper 测试 ====================

def search_notes(notes, keyword):
    """按关键词搜索笔记内容"""
    if not keyword or not keyword.strip():
        return []

    keyword = keyword.lower().strip()
    results = []

    for note in notes:
        content = note.get("content", "").lower()
        if keyword in content:
            results.append(note)

    return results


def filter_by_date(notes, start_date=None, end_date=None):
    """按日期范围过滤笔记"""
    results = []

    for note in notes:
        note_date = note.get("date", "")

        try:
            note_dt = datetime.strptime(note_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            continue

        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            if note_dt < start_dt:
                continue

        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            if note_dt > end_dt:
                continue

        results.append(note)

    return results


def extract_tags(content):
    """从笔记内容中提取 #标签"""
    if not content:
        return []

    pattern = r"#([\w\u4e00-\u9fff]+)"
    tags = re.findall(pattern, content)
    return tags


class TestPyHelperTextUtils:
    """测试 PyHelper 文本工具"""

    # ---------- search_notes 测试 ----------

    def test_search_notes_success(self):
        """测试笔记搜索成功（正例）"""
        notes = [
            {"content": "学习 Python 基础", "date": "2026-02-01"},
            {"content": "Python 正则表达式", "date": "2026-02-02"},
            {"content": "JavaScript 入门", "date": "2026-02-03"},
        ]
        results = search_notes(notes, "Python")
        assert len(results) == 2
        assert results[0]["content"] == "学习 Python 基础"
        assert results[1]["content"] == "Python 正则表达式"

    def test_search_notes_case_insensitive(self):
        """测试搜索大小写不敏感"""
        notes = [
            {"content": "学习 PYTHON 基础", "date": "2026-02-01"},
            {"content": "python 正则表达式", "date": "2026-02-02"},
        ]
        results = search_notes(notes, "python")
        assert len(results) == 2

    def test_search_notes_empty_keyword(self):
        """测试空关键词搜索（边界）"""
        notes = [
            {"content": "学习 Python 基础", "date": "2026-02-01"},
        ]
        assert search_notes(notes, "") == []
        assert search_notes(notes, "   ") == []
        assert search_notes(notes, None) == []

    def test_search_notes_not_found(self):
        """测试搜索无结果（反例）"""
        notes = [
            {"content": "学习 Python 基础", "date": "2026-02-01"},
        ]
        assert search_notes(notes, "Java") == []

    def test_search_notes_empty_list(self):
        """测试搜索空笔记列表（边界）"""
        assert search_notes([], "Python") == []

    def test_search_notes_whitespace_stripping(self):
        """测试关键词去除首尾空格"""
        notes = [
            {"content": "学习 Python 基础", "date": "2026-02-01"},
        ]
        results = search_notes(notes, "  Python  ")
        assert len(results) == 1

    # ---------- filter_by_date 测试 ----------

    def test_filter_by_date_range(self):
        """测试按日期范围过滤（正例）"""
        notes = [
            {"content": "笔记1", "date": "2026-02-01"},
            {"content": "笔记2", "date": "2026-02-05"},
            {"content": "笔记3", "date": "2026-02-10"},
            {"content": "笔记4", "date": "2026-02-15"},
        ]
        results = filter_by_date(notes, "2026-02-05", "2026-02-10")
        assert len(results) == 2
        assert results[0]["content"] == "笔记2"
        assert results[1]["content"] == "笔记3"

    def test_filter_by_date_start_only(self):
        """测试只指定开始日期"""
        notes = [
            {"content": "笔记1", "date": "2026-02-01"},
            {"content": "笔记2", "date": "2026-02-10"},
            {"content": "笔记3", "date": "2026-02-15"},
        ]
        results = filter_by_date(notes, start_date="2026-02-10")
        assert len(results) == 2
        assert results[0]["content"] == "笔记2"

    def test_filter_by_date_end_only(self):
        """测试只指定结束日期"""
        notes = [
            {"content": "笔记1", "date": "2026-02-01"},
            {"content": "笔记2", "date": "2026-02-10"},
            {"content": "笔记3", "date": "2026-02-15"},
        ]
        results = filter_by_date(notes, end_date="2026-02-10")
        assert len(results) == 2
        assert results[0]["content"] == "笔记1"

    def test_filter_by_date_no_dates(self):
        """测试不指定日期范围（边界）"""
        notes = [
            {"content": "笔记1", "date": "2026-02-01"},
            {"content": "笔记2", "date": "2026-02-10"},
        ]
        results = filter_by_date(notes)
        assert len(results) == 2

    def test_filter_by_date_invalid_date_format(self):
        """测试无效日期格式（反例）"""
        notes = [
            {"content": "笔记1", "date": "2026/02/01"},  # 错误格式
            {"content": "笔记2", "date": "2026-02-10"},
            {"content": "笔记3", "date": "invalid"},
        ]
        results = filter_by_date(notes)
        # 只有格式正确的笔记会被保留
        assert len(results) == 1
        assert results[0]["content"] == "笔记2"

    def test_filter_by_date_empty_list(self):
        """测试过滤空列表（边界）"""
        assert filter_by_date([]) == []

    # ---------- extract_tags 测试 ----------

    def test_extract_tags_success(self):
        """测试提取标签成功（正例）"""
        content = "今天学习了 #Python 和 #正则表达式，很有收获 #学习笔记"
        tags = extract_tags(content)
        assert "Python" in tags
        assert "正则表达式" in tags
        assert "学习笔记" in tags

    def test_extract_tags_english(self):
        """测试提取英文标签"""
        content = "学习 #Python #coding #week_09"
        tags = extract_tags(content)
        assert "Python" in tags
        assert "coding" in tags
        assert "week_09" in tags

    def test_extract_tags_empty(self):
        """测试提取空内容（边界）"""
        assert extract_tags("") == []
        assert extract_tags(None) == []

    def test_extract_tags_no_tags(self):
        """测试无标签内容（反例）"""
        content = "今天学习了 Python 和正则表达式"
        assert extract_tags(content) == []

    def test_extract_tags_special_chars(self):
        """测试标签中的特殊字符"""
        # 只有 \w 和中文字符会被匹配
        content = "#tag1 #tag-2 #tag.3 #中文"
        tags = extract_tags(content)
        assert "tag1" in tags
        # - 和 . 不被 \w 匹配，所以 tag-2 只会匹配 tag
        assert "tag" in tags
        assert "中文" in tags


# ==================== 参数化测试示例 ====================

@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("  hello  ", "hello"),
        ("\t\nworld\r\n", "world"),
        ("no_spaces", "no_spaces"),
        ("", ""),
    ],
)
def test_strip_parametrized(input_text, expected):
    """参数化测试 strip 方法"""
    assert input_text.strip() == expected


@pytest.mark.parametrize(
    "pattern,text,expected",
    [
        (r"\d+", "abc123", "123"),
        (r"[a-z]+", "ABCdefGHI", "def"),
        (r"\w+@\w+\.\w+", "联系 user@example.com 请", "user@example.com"),
    ],
)
def test_re_search_parametrized(pattern, text, expected):
    """参数化测试正则搜索"""
    match = re.search(pattern, text)
    assert match is not None
    assert match.group() == expected
