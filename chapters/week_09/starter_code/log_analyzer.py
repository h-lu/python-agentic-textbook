"""Week 09 练习 4：日志分析器扩展。"""

import re

try:
    from log_parser import extract_level, extract_timestamp
except ImportError:  # pragma: no cover - package import fallback
    from .log_parser import extract_level, extract_timestamp


def extract_urls(text):
    """从文本中提取 http/https URL。"""
    if not text:
        return []
    return re.findall(r"https?://[^\s,，。]+", text)


def analyze_error_types(log_lines):
    """统计各日志级别出现次数。"""
    counts = {}
    for line in log_lines:
        level = extract_level(line)
        if level:
            counts[level] = counts.get(level, 0) + 1
    return counts


def find_slow_queries(log_lines, threshold_ms):
    """找出耗时超过阈值的慢查询日志。"""
    results = []
    pattern = r"查询耗时\s*(\d+)ms\s*-\s*(.+)$"

    for line in log_lines:
        match = re.search(pattern, line)
        if not match:
            continue

        duration = int(match.group(1))
        if duration > threshold_ms:
            results.append(
                {
                    "time": extract_timestamp(line),
                    "duration": duration,
                    "query": match.group(2).strip(),
                }
            )

    return results
