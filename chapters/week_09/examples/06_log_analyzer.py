"""
示例：完整的日志分析器（贯穿案例最终版）

本例演示一个功能完整的日志分析器，综合运用字符串方法、
正则表达式和边界情况处理。

运行方式：
    python3 chapters/week_09/examples/06_log_analyzer.py

预期输出：
    === 日志分析器 ===
    已加载 5 条日志记录
    === 统计概览 ===
    总请求数: 5
    独立 IP 数: 3
    错误数 (4xx/5xx): 3
    === IP 访问统计 ===
    192.168.1.1: 总请求 3, 错误 2
    192.168.1.2: 总请求 1, 错误 0
    192.168.1.3: 总请求 1, 错误 1
    === 查找 404 错误 ===
    2026-02-09 14:32:10 - 192.168.1.1 GET /api/products 404
    2026-02-09 14:32:15 - 192.168.1.3 GET /api/admin 404
    === 提取所有 IP 地址 ===
    找到的 IP: ['192.168.1.1', '192.168.1.2', '192.168.1.1', '192.168.1.1', '192.168.1.3']
    独立 IP: ['192.168.1.1', '192.168.1.2', '192.168.1.3']
    === 生成脱敏报告 ===
    时间,IP,方法,路径,状态
    2026-02-09 14:32:01,***.***.1.1,GET,/api/users,200
    2026-02-09 14:32:05,***.***.1.2,POST,/api/login,200
    ...
"""

import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class LogAnalyzer:
    """日志分析器 - 解析和分析 Web 访问日志"""

    # 正则模式：匹配 IP、方法、路径、状态码
    LOG_PATTERN = re.compile(
        r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+-\s+"
        r"(?P<method>\w+)\s+"
        r"(?P<path>/\S+)\s+"
        r"(?P<status>\d{3})"
    )

    def __init__(self):
        self.records: list[dict] = []

    def parse_line(self, line: str) -> dict | None:
        """解析单行日志

        Args:
            line: 日志行字符串

        Returns:
            解析后的字典，格式错误返回 None
        """
        line = line.strip()
        if not line:
            return None

        match = self.LOG_PATTERN.search(line)
        if not match:
            return None

        return {
            "ip": match.group("ip"),
            "method": match.group("method"),
            "path": match.group("path"),
            "status": match.group("status"),
            "status_int": int(match.group("status"))
        }

    def load_from_text(self, text: str) -> int:
        """从文本加载日志

        Args:
            text: 日志文本（多行）

        Returns:
            成功解析的记录数
        """
        count = 0
        for line in text.strip().split("\n"):
            record = self.parse_line(line)
            if record:
                self.records.append(record)
                count += 1
        return count

    def load_from_file(self, file_path: str | Path, encoding: str = "utf-8") -> int:
        """从文件加载日志

        Args:
            file_path: 日志文件路径
            encoding: 文件编码，默认 utf-8

        Returns:
            成功解析的记录数
        """
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"警告: 文件 {file_path} 不存在")
            return 0

        try:
            with open(file_path, "r", encoding=encoding, errors="replace") as f:
                content = f.read()
            return self.load_from_text(content)
        except Exception as e:
            print(f"错误: 读取文件时发生异常 - {e}")
            return 0

    def get_stats(self) -> dict[str, int]:
        """获取统计信息

        Returns:
            包含总请求数、独立 IP 数、错误数的字典
        """
        total = len(self.records)
        unique_ips = len(set(r["ip"] for r in self.records))
        errors = sum(1 for r in self.records if r["status_int"] >= 400)

        return {
            "total_requests": total,
            "unique_ips": unique_ips,
            "errors": errors
        }

    def get_ip_stats(self) -> dict[str, dict[str, int]]:
        """获取每个 IP 的访问统计

        Returns:
            字典，key 是 IP，value 是统计信息
        """
        stats = defaultdict(lambda: {"total": 0, "errors": 0})

        for record in self.records:
            ip = record["ip"]
            stats[ip]["total"] += 1
            if record["status_int"] >= 400:
                stats[ip]["errors"] += 1

        return dict(stats)

    def filter_by_status(self, status_prefix: str) -> list[dict]:
        """按状态码前缀过滤记录

        Args:
            status_prefix: 状态码前缀，如 "4" 表示所有 4xx 错误

        Returns:
            符合条件的记录列表
        """
        return [
            r for r in self.records
            if r["status"].startswith(status_prefix)
        ]

    def filter_by_ip(self, ip: str) -> list[dict]:
        """按 IP 地址过滤记录

        Args:
            ip: IP 地址

        Returns:
            该 IP 的所有记录
        """
        return [r for r in self.records if r["ip"] == ip]

    def extract_ips(self) -> list[str]:
        """提取所有 IP 地址

        Returns:
            IP 地址列表（可能包含重复）
        """
        return [r["ip"] for r in self.records]

    def extract_unique_ips(self) -> list[str]:
        """提取所有唯一的 IP 地址

        Returns:
            去重后的 IP 地址列表
        """
        return sorted(set(r["ip"] for r in self.records))

    def generate_report(self, mask_ips: bool = False) -> str:
        """生成 CSV 格式的报告

        Args:
            mask_ips: 是否脱敏 IP 地址

        Returns:
            CSV 格式的报告字符串
        """
        lines = ["IP,方法,路径,状态"]

        for r in self.records:
            ip = r["ip"]
            if mask_ips:
                parts = ip.split(".")
                ip = f"***.***.{parts[2]}.{parts[3]}"

            line = f"{ip},{r['method']},{r['path']},{r['status']}"
            lines.append(line)

        return "\n".join(lines)

    def print_summary(self):
        """打印统计摘要"""
        stats = self.get_stats()

        print("=== 统计概览 ===")
        print(f"总请求数: {stats['total_requests']}")
        print(f"独立 IP 数: {stats['unique_ips']}")
        print(f"错误数 (4xx/5xx): {stats['errors']}")

        print("\n=== IP 访问统计 ===")
        ip_stats = self.get_ip_stats()
        for ip, data in ip_stats.items():
            print(f"{ip}: 总请求 {data['total']}, 错误 {data['errors']}")


# =====================
# 演示
# =====================

if __name__ == "__main__":
    # 示例日志数据
    sample_logs = """\
192.168.1.1 - GET /api/users 200
192.168.1.2 - POST /api/login 200
192.168.1.1 - GET /api/products 404
192.168.1.1 - DELETE /api/users/123 403
192.168.1.3 - GET /api/admin 404
"""

    print("=== 日志分析器 ===")

    # 创建分析器并加载日志
    analyzer = LogAnalyzer()
    count = analyzer.load_from_text(sample_logs)
    print(f"已加载 {count} 条日志记录")

    # 打印统计摘要
    analyzer.print_summary()

    # 查找 404 错误
    print("\n=== 查找 404 错误 ===")
    not_found = analyzer.filter_by_status("404")
    for r in not_found:
        print(f"{r['ip']} {r['method']} {r['path']} {r['status']}")

    # 提取所有 IP
    print("\n=== 提取所有 IP 地址 ===")
    all_ips = analyzer.extract_ips()
    unique_ips = analyzer.extract_unique_ips()
    print(f"找到的 IP: {all_ips}")
    print(f"独立 IP: {unique_ips}")

    # 生成脱敏报告
    print("\n=== 生成脱敏报告 ===")
    report = analyzer.generate_report(mask_ips=True)
    print(report)

    # 测试边界情况
    print("\n=== 测试边界情况 ===")

    # 空分析器
    empty_analyzer = LogAnalyzer()
    print(f"空分析器统计: {empty_analyzer.get_stats()}")

    # 格式错误的日志
    bad_logs = """\
192.168.1.1 - GET /api/users 200
这行格式不对
192.168.1.2 - POST /api/login 200


"""
    bad_analyzer = LogAnalyzer()
    valid_count = bad_analyzer.load_from_text(bad_logs)
    print(f"从混乱日志中解析出 {valid_count} 条有效记录")

    print("\n✓ 日志分析器演示完成！")
