"""
Week 09 作业参考实现：日志分析器

本文件提供 Week 09 作业的基础参考实现。
学生可以先尝试自己完成，遇到困难时再参考此文件。

作业要求：
1. 实现 parse_log_line() 函数，解析单行日志
2. 实现 extract_ips() 函数，提取所有 IP 地址
3. 实现 filter_by_level() 函数，按日志级别过滤
4. 实现 count_errors() 函数，统计错误数量
5. 处理边界情况（空行、格式错误等）
"""

import re
from collections import defaultdict


def parse_log_line(line: str) -> dict | None:
    """
    解析单行日志

    输入格式: "[YYYY-MM-DD HH:MM:SS] LEVEL: message"
    例如: "[2026-02-09 14:32:01] ERROR: 数据库连接超时"

    Args:
        line: 日志行字符串

    Returns:
        包含 timestamp, level, message 的字典，格式错误返回 None
    """
    line = line.strip()
    if not line:
        return None

    # 找到右方括号的位置
    bracket_end = line.find("]")
    if bracket_end == -1:
        return None

    # 从方括号后开始找冒号（避免找到时间戳中的冒号）
    colon_pos = line.find(":", bracket_end)
    if colon_pos == -1:
        return None

    # 提取各部分
    timestamp = line[1:bracket_end]
    level = line[bracket_end + 2:colon_pos].strip()
    message = line[colon_pos + 2:].strip()

    return {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }


def extract_ips(log_text: str) -> list[str]:
    """
    从日志文本中提取所有 IP 地址

    使用正则表达式匹配 IP 地址模式：xxx.xxx.xxx.xxx

    Args:
        log_text: 日志文本

    Returns:
        IP 地址列表（可能包含重复）
    """
    # IP 地址正则：四个 0-255 的数字，用点分隔
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    return re.findall(ip_pattern, log_text)


def filter_by_level(logs: list[dict], level: str) -> list[dict]:
    """
    按日志级别过滤

    Args:
        logs: 解析后的日志字典列表
        level: 日志级别（如 "ERROR", "INFO", "WARNING"）

    Returns:
        符合级别的日志列表
    """
    # 大小写不敏感比较
    level = level.upper()
    return [log for log in logs if log.get("level", "").upper() == level]


def count_errors(logs: list[dict]) -> int:
    """
    统计错误数量（ERROR 级别）

    Args:
        logs: 解析后的日志字典列表

    Returns:
        错误日志的数量
    """
    return len(filter_by_level(logs, "ERROR"))


def analyze_logs(log_lines: list[str]) -> dict:
    """
    分析日志文件，生成统计报告

    Args:
        log_lines: 日志行列表

    Returns:
        包含统计信息的字典
    """
    parsed_logs = []
    error_count = 0

    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed:
            parsed_logs.append(parsed)
            if parsed["level"].upper() == "ERROR":
                error_count += 1

    # 统计各级别数量
    level_counts = defaultdict(int)
    for log in parsed_logs:
        level_counts[log["level"]] += 1

    return {
        "total_lines": len(log_lines),
        "valid_lines": len(parsed_logs),
        "error_count": error_count,
        "level_counts": dict(level_counts)
    }


# =====================
# 测试代码
# =====================

if __name__ == "__main__":
    print("=== 日志分析器测试 ===\n")

    # 测试数据
    sample_logs = [
        "[2026-02-09 14:32:01] ERROR: 数据库连接超时",
        "[2026-02-09 14:32:05] INFO: 用户登录成功",
        "[2026-02-09 14:32:10] WARNING: 磁盘空间不足",
        "[2026-02-09 14:32:15] ERROR: 请求超时",
        "",  # 空行
        "这行格式不对",  # 无效格式
    ]

    # 测试 parse_log_line
    print("1. 测试 parse_log_line:")
    for line in sample_logs[:3]:
        result = parse_log_line(line)
        print(f"   输入: {line}")
        print(f"   输出: {result}")
    print(f"   空行返回: {parse_log_line('')}")
    print(f"   无效格式返回: {parse_log_line('invalid')}")

    # 测试 extract_ips
    print("\n2. 测试 extract_ips:")
    log_with_ips = """
    [2026-02-09 14:32:01] 192.168.1.1 - GET /api/users 200
    [2026-02-09 14:32:05] 192.168.1.2 - POST /api/login 200
    """
    ips = extract_ips(log_with_ips)
    print(f"   找到的 IP: {ips}")

    # 测试 filter_by_level
    print("\n3. 测试 filter_by_level:")
    parsed = [parse_log_line(line) for line in sample_logs if parse_log_line(line)]
    errors = filter_by_level(parsed, "ERROR")
    print(f"   ERROR 级别日志: {len(errors)} 条")
    for e in errors:
        print(f"   - {e['timestamp']}: {e['message']}")

    # 测试 count_errors
    print("\n4. 测试 count_errors:")
    count = count_errors(parsed)
    print(f"   错误数量: {count}")

    # 测试 analyze_logs
    print("\n5. 测试 analyze_logs:")
    report = analyze_logs(sample_logs)
    print(f"   总行数: {report['total_lines']}")
    print(f"   有效行数: {report['valid_lines']}")
    print(f"   错误数: {report['error_count']}")
    print(f"   各级别统计: {report['level_counts']}")

    print("\n✓ 所有测试完成！")
