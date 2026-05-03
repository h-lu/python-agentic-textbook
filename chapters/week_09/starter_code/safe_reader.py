"""Week 09 挑战 2：安全读取文本和日志。"""

import re

try:
    from log_parser import clean_log_line, extract_level, extract_timestamp
except ImportError:  # pragma: no cover - package import fallback
    from .log_parser import clean_log_line, extract_level, extract_timestamp


def safe_read_file(file_path, encoding="utf-8"):
    """尝试多种编码读取文件，最后用替换模式兜底。"""
    encodings = [encoding, "gbk", "latin-1"]
    tried = []

    for item in encodings:
        if item in tried:
            continue
        tried.append(item)
        try:
            with open(file_path, "r", encoding=item) as file:
                return file.read()
        except UnicodeDecodeError:
            continue

    with open(file_path, "r", encoding=encoding, errors="replace") as file:
        return file.read()


def read_logs_with_fallback(file_path):
    """读取日志文件，返回 (records, errors)。"""
    records = []
    errors = []
    content = safe_read_file(file_path)

    for line_number, line in enumerate(content.splitlines(), 1):
        cleaned = clean_log_line(line)
        if cleaned is None:
            continue

        timestamp = extract_timestamp(cleaned)
        level = extract_level(cleaned)
        if not timestamp or not level:
            errors.append({"line": line_number, "content": line})
            continue

        records.append({"timestamp": timestamp, "level": level, "raw": cleaned})

    return records, errors


def normalize_whitespace(text):
    """把所有连续空白规范化为单个空格。"""
    if text is None:
        return ""
    return re.sub(r"\s+", " ", text).strip()
