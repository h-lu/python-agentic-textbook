"""Week 09 练习 1：日志行清洗与基础提取。"""


def clean_log_line(line):
    """清洗一行日志；空行和注释行返回 None。"""
    if line is None:
        return None

    cleaned = line.strip()
    if not cleaned or cleaned.startswith("#"):
        return None
    return cleaned


def extract_timestamp(line):
    """提取 ``[时间] LEVEL: message`` 中方括号内的时间。"""
    if not line:
        return None

    start = line.find("[")
    end = line.find("]", start + 1)
    if start == -1 or end == -1 or end <= start + 1:
        return None
    return line[start + 1:end]


def extract_level(line):
    """提取日志级别，并统一为大写。"""
    if not line:
        return None

    bracket_end = line.find("]")
    if bracket_end == -1:
        return None

    colon_pos = line.find(":", bracket_end + 1)
    if colon_pos == -1:
        return None

    level = line[bracket_end + 1:colon_pos].strip()
    return level.upper() if level else None
