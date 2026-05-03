"""Week 09 作业参考实现聚合模块。

作业正文把功能拆在多个文件中；本文件重新导出这些函数，方便学生
从一个入口浏览参考实现。
"""

try:
    from csv_handler import filter_by_status, format_as_table, parse_csv_line
    from log_analyzer import analyze_error_types, extract_urls, find_slow_queries
    from log_parser import clean_log_line, extract_level, extract_timestamp
    from pattern_matcher import find_emails, find_ip_addresses, is_valid_phone
    from safe_reader import normalize_whitespace, read_logs_with_fallback, safe_read_file
    from url_parser import parse_path_params, parse_query_params, reconstruct_url
except ImportError:  # pragma: no cover - package import fallback
    from .csv_handler import filter_by_status, format_as_table, parse_csv_line
    from .log_analyzer import analyze_error_types, extract_urls, find_slow_queries
    from .log_parser import clean_log_line, extract_level, extract_timestamp
    from .pattern_matcher import find_emails, find_ip_addresses, is_valid_phone
    from .safe_reader import normalize_whitespace, read_logs_with_fallback, safe_read_file
    from .url_parser import parse_path_params, parse_query_params, reconstruct_url


__all__ = [
    "clean_log_line",
    "extract_timestamp",
    "extract_level",
    "parse_csv_line",
    "filter_by_status",
    "format_as_table",
    "find_ip_addresses",
    "find_emails",
    "is_valid_phone",
    "extract_urls",
    "analyze_error_types",
    "find_slow_queries",
    "parse_query_params",
    "parse_path_params",
    "reconstruct_url",
    "safe_read_file",
    "read_logs_with_fallback",
    "normalize_whitespace",
]
