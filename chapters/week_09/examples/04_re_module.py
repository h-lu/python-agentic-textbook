"""
示例：re 模块实战 - search、findall、groups、sub

本例演示 re 模块的高级用法，包括 findall、分组提取、
命名分组和替换操作。

运行方式：
    python3 chapters/week_09/examples/04_re_module.py

预期输出：
    === findall 找到所有匹配 ===
    找到的所有 IP: ['192.168.1.1', '192.168.1.1', '192.168.1.2']
    带分组的结果: [('2026-02-09', '14:32:01'), ('2026-02-09', '14:32:05'), ('2026-02-09', '14:32:10'), ('2026-02-09', '14:32:15')]
    === 分组提取详细信息 ===
    方法: GET, 路径: /api/users?page=1, 状态: 200
    === 命名分组 ===
    方法: GET
    路径: /api/users?page=1
    字典形式: {'method': 'GET', 'path': '/api/users?page=1', 'status': '200'}
    === 实战：日志分析器 ===
    192.168.1.1: 总请求 3, 错误 2
    192.168.1.2: 总请求 1, 错误 0
    192.168.1.3: 总请求 1, 错误 1
    === re.sub() 替换 ===
    脱敏后: 用户 ***.***.***.*** 访问了 /api/users
    部分脱敏: 用户 ***.***.1.1 访问了 /api/users
    === 坏例子：贪婪匹配陷阱 ===
    贪婪匹配结果: <div>内容1</div><div>内容2</div>
    非贪婪匹配结果: <div>内容1</div>
"""

import re
from collections import defaultdict


# =====================
# findall 找到所有匹配
# =====================

print("=== findall 找到所有匹配 ===")

log_text = """
[2026-02-09 14:32:01] 192.168.1.1 - GET /api/users 200
[2026-02-09 14:32:05] 用户 admin@example.com 登录成功
[2026-02-09 14:32:10] 192.168.1.1 - GET /api/products 404
[2026-02-09 14:32:15] 192.168.1.2 - POST /api/login 200
"""

# findall 返回所有非重叠匹配的列表
ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
ips = re.findall(ip_pattern, log_text)
print(f"找到的所有 IP: {ips}")

# 如果正则里有分组，返回分组内容的元组列表
datetime_pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})"
datetimes = re.findall(datetime_pattern, log_text)
print(f"带分组的结果: {datetimes}")


# =====================
# 分组提取详细信息
# =====================

print("\n=== 分组提取详细信息 ===")

log_line = "192.168.1.1 - GET /api/users?page=1 200"

# 用分组提取方法、路径、状态码
pattern = r"(\w+) (/\S+) (\d{3})"
match = re.search(pattern, log_line)

if match:
    method = match.group(1)     # 第一个分组
    path = match.group(2)       # 第二个分组
    status = match.group(3)     # 第三个分组
    print(f"方法: {method}, 路径: {path}, 状态: {status}")


# =====================
# 命名分组
# =====================

print("\n=== 命名分组 ===")

# 命名分组 (?P<name>...)
pattern = r"(?P<method>\w+) (?P<path>/\S+) (?P<status>\d{3})"
match = re.search(pattern, log_line)

if match:
    print(f"方法: {match.group('method')}")
    print(f"路径: {match.group('path')}")
    print(f"字典形式: {match.groupdict()}")


# =====================
# 实战：日志分析器
# =====================

print("\n=== 实战：日志分析器 ===")


def analyze_logs(log_lines: list[str]) -> dict[str, dict[str, int]]:
    """分析日志，统计每个 IP 的访问次数和错误数

    Args:
        log_lines: 日志行列表

    Returns:
        字典，key 是 IP，value 是 {'total': 总请求数, 'errors': 错误数}
    """
    ip_counter = defaultdict(lambda: {"total": 0, "errors": 0})

    # 匹配 IP、方法、路径、状态码
    pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\w+) (/\S+) (\d{3})"

    for line in log_lines:
        match = re.search(pattern, line)
        if match:
            ip, method, path, status = match.groups()
            ip_counter[ip]["total"] += 1
            if status.startswith("4") or status.startswith("5"):
                ip_counter[ip]["errors"] += 1

    return dict(ip_counter)


# 测试数据
logs = [
    "192.168.1.1 - GET /api/users 200",
    "192.168.1.2 - POST /api/login 200",
    "192.168.1.1 - GET /api/products 404",
    "192.168.1.1 - DELETE /api/users/123 403",
    "192.168.1.3 - GET /api/admin 500"
]

stats = analyze_logs(logs)
for ip, data in stats.items():
    print(f"{ip}: 总请求 {data['total']}, 错误 {data['errors']}")


# =====================
# re.sub() 替换
# =====================

print("\n=== re.sub() 替换 ===")

# 把日志里的 IP 地址脱敏（隐藏）
log_line = "用户 192.168.1.1 访问了 /api/users"
masked = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "***.***.***.***", log_line)
print(f"脱敏后: {masked}")

# sub() 也支持用函数动态决定替换内容


def mask_ip(match: re.Match) -> str:
    """只保留 IP 的后两段"""
    ip = match.group()
    parts = ip.split(".")
    return f"***.***.{parts[2]}.{parts[3]}"


masked = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", mask_ip, log_line)
print(f"部分脱敏: {masked}")


# =====================
# 坏例子：贪婪匹配陷阱
# =====================

print("\n=== 坏例子：贪婪匹配陷阱 ===")

html = "<div>内容1</div><div>内容2</div>"

# 贪婪匹配：.* 会尽可能多匹配
greedy_pattern = r"<div>.*</div>"
greedy_match = re.search(greedy_pattern, html)
print(f"贪婪匹配结果: {greedy_match.group() if greedy_match else 'None'}")

# 非贪婪匹配：.*? 尽可能少匹配
non_greedy_pattern = r"<div>.*?</div>"
non_greedy_match = re.search(non_greedy_pattern, html)
print(f"非贪婪匹配结果: {non_greedy_match.group() if non_greedy_match else 'None'}")

print("\n提示：处理 HTML/XML 时，非贪婪匹配 .*? 通常更符合预期")
