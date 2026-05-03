"""Week 09 assignment contract tests."""

import sys
from pathlib import Path

STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))

from csv_handler import filter_by_status, format_as_table, parse_csv_line
from log_analyzer import analyze_error_types, extract_urls, find_slow_queries
from log_parser import clean_log_line, extract_level, extract_timestamp
from pattern_matcher import find_emails, find_ip_addresses, is_valid_phone
from safe_reader import normalize_whitespace, read_logs_with_fallback, safe_read_file
from url_parser import parse_path_params, parse_query_params, reconstruct_url


def test_log_parser_contract():
    line = "  [2026-02-09 14:32:01]  warning : 磁盘不足  \n"
    cleaned = clean_log_line(line)
    assert cleaned == "[2026-02-09 14:32:01]  warning : 磁盘不足"
    assert clean_log_line("   ") is None
    assert clean_log_line("# 注释") is None
    assert extract_timestamp(cleaned) == "2026-02-09 14:32:01"
    assert extract_level(cleaned) == "WARNING"
    assert extract_timestamp("没有方括号") is None


def test_csv_handler_contract():
    line = "2026-02-09 14:32:01,192.168.1.1,GET,/api/users,200"
    assert parse_csv_line(line) == {
        "time": "2026-02-09 14:32:01",
        "ip": "192.168.1.1",
        "method": "GET",
        "path": "/api/users",
        "status": "200",
    }
    assert parse_csv_line("字段不够") is None

    records = filter_by_status(
        [
            "timestamp,ip,method,path,status",
            line,
            "2026-02-09 14:32:10,192.168.1.2,GET,/missing,404",
        ],
        "404",
    )
    assert len(records) == 1
    assert records[0]["path"] == "/missing"
    table = format_as_table(records)
    assert "时间" in table and "/missing" in table


def test_pattern_matcher_contract():
    text = "服务器 192.168.1.1 和 10.0.0.1，联系 admin@example.com 或 support@company.org.cn"
    assert find_ip_addresses(text) == ["192.168.1.1", "10.0.0.1"]
    assert find_emails(text) == ["admin@example.com", "support@company.org.cn"]
    assert is_valid_phone("13812345678") is True
    assert is_valid_phone("11812345678") is False
    assert is_valid_phone("1381234567") is False


def test_log_analyzer_contract():
    logs = [
        "[2026-02-09 14:32:01] ERROR: 连接失败 https://example.com",
        "[2026-02-09 14:32:02] WARNING: 内存不足",
        "[2026-02-09 14:32:03] ERROR: 超时",
    ]
    assert extract_urls(logs[0]) == ["https://example.com"]
    assert analyze_error_types(logs) == {"ERROR": 2, "WARNING": 1}

    slow = find_slow_queries(
        [
            "[2026-02-09 14:32:01] SLOW: 查询耗时 150ms - SELECT * FROM users",
            "[2026-02-09 14:32:02] SLOW: 查询耗时 50ms - SELECT * FROM posts",
        ],
        100,
    )
    assert slow == [
        {
            "time": "2026-02-09 14:32:01",
            "duration": 150,
            "query": "SELECT * FROM users",
        }
    ]


def test_url_parser_contract():
    assert parse_query_params("https://example.com/search?q=python&page=1") == {
        "q": "python",
        "page": "1",
    }
    assert parse_query_params("https://example.com/") == {}
    assert parse_path_params("/api/users/123/posts/456") == [
        "api",
        "users",
        "123",
        "posts",
        "456",
    ]
    assert reconstruct_url("https://api.example.com/search", {"q": "python"}) == (
        "https://api.example.com/search?q=python"
    )


def test_safe_reader_contract(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text(
        "\n# comment\n[2026-02-09 14:32:01] INFO: ok\nbad line\n",
        encoding="utf-8",
    )

    assert safe_read_file(log_file) == log_file.read_text(encoding="utf-8")
    records, errors = read_logs_with_fallback(log_file)
    assert records[0]["level"] == "INFO"
    assert errors == [{"line": 4, "content": "bad line"}]
    assert normalize_whitespace("  hello   world\t\n  python  ") == "hello world python"
