"""
示例：split 和 join 操作 - 处理结构化文本

本例演示如何用 split() 拆分 CSV 格式日志，
以及用 join() 重组数据。

运行方式：
    python3 chapters/week_09/examples/02_split_join.py

预期输出：
    === split() 基础 ===
    拆分结果: ['2026-02-09 14:32:01', '192.168.1.1', 'GET', '/api/users', '200']
    IP: 192.168.1.1, 状态: 200
    === split() 默认行为 ===
    'hello   world'.split(): ['hello', 'world']
    'hello\tworld\npython'.split(): ['hello', 'world', 'python']
    === 处理用户输入 ===
    带空格输入 split(','): ['  192.168.1.1  ']
    带空格输入 split(): ['192.168.1.1']
    === partition() 只拆一次 ===
    'key=value'.partition('='): ('key', '=', 'value')
    'key=value=extra'.partition('='): ('key', '=', 'value=extra')
    === join() 重组 ===
    空格连接: 'hello world python'
    逗号连接: 'hello,world,python'
    横线连接: 'hello-world-python'
    === 实战：过滤 404 日志 ===
    2026-02-09 14:32:10 - 192.168.1.1 访问 /api/products 失败
    2026-02-09 14:32:15 - 192.168.1.3 访问 /api/admin 失败
    === 格式化成报告 ===
    时间,IP,路径
    2026-02-09 14:32:10,192.168.1.1,/api/products
    2026-02-09 14:32:15,192.168.1.3,/api/admin
    === 坏例子：不检查字段数 ===
    坏例子处理不完整的行会抛出 IndexError！
"""


# =====================
# split() 基础
# =====================

print("=== split() 基础 ===")

line = "2026-02-09 14:32:01,192.168.1.1,GET,/api/users,200"
parts = line.split(",")
print(f"拆分结果: {parts}")

# 提取特定字段
ip = parts[1]
status = parts[4]
print(f"IP: {ip}, 状态: {status}")


# =====================
# split() 默认行为
# =====================

print("\n=== split() 默认行为 ===")

# 默认按空白字符拆分，且会合并连续的空白
result1 = "hello   world".split()
result2 = "hello\tworld\npython".split()
print(f"'hello   world'.split(): {result1}")
print(f"'hello\\tworld\\npython'.split(): {result2}")


# =====================
# 处理用户输入
# =====================

print("\n=== 处理用户输入 ===")

user_input = "  192.168.1.1  "
print(f"带空格输入 split(','): {user_input.split(',')}")
print(f"带空格输入 split(): {user_input.split()}")


# =====================
# partition() 只拆一次
# =====================

print("\n=== partition() 只拆一次 ===")

# partition 返回三元组 (before, separator, after)
result1 = "key=value".partition("=")
result2 = "key=value=extra".partition("=")  # 只拆第一次
print(f"'key=value'.partition('='): {result1}")
print(f"'key=value=extra'.partition('='): {result2}")


# =====================
# join() 重组
# =====================

print("\n=== join() 重组 ===")

words = ["hello", "world", "python"]
print(f"空格连接: '{ ' '.join(words) }'")
print(f"逗号连接: '{ ','.join(words) }'")
print(f"横线连接: '{ '-'.join(words) }'")


# =====================
# 实战：过滤 404 日志
# =====================

print("\n=== 实战：过滤 404 日志 ===")


def filter_404_logs(csv_lines: list[str]) -> list[dict]:
    """从 CSV 日志中提取所有 404 错误

    Args:
        csv_lines: CSV 格式的日志行列表

    Returns:
        404 错误记录列表
    """
    errors = []
    for line in csv_lines:
        line = line.strip()
        if not line or line.startswith("timestamp"):
            continue  # 跳过空行和表头

        parts = line.split(",")
        if len(parts) >= 5 and parts[4] == "404":
            errors.append({
                "time": parts[0],
                "ip": parts[1],
                "path": parts[3]
            })
    return errors


# 测试数据
logs = [
    "timestamp,ip,method,path,status",
    "2026-02-09 14:32:01,192.168.1.1,GET,/api/users,200",
    "2026-02-09 14:32:10,192.168.1.1,GET,/api/products,404",
    "2026-02-09 14:32:15,192.168.1.3,GET,/api/admin,404"
]

errors = filter_404_logs(logs)
for e in errors:
    print(f"{e['time']} - {e['ip']} 访问 {e['path']} 失败")


# =====================
# 格式化成报告
# =====================

print("\n=== 格式化成报告 ===")


def format_errors_for_report(errors: list[dict]) -> str:
    """把错误记录格式化成报告格式

    Args:
        errors: 错误记录列表

    Returns:
        CSV 格式的报告字符串
    """
    lines = ["时间,IP,路径"]
    for e in errors:
        line = ",".join([e["time"], e["ip"], e["path"]])
        lines.append(line)
    return "\n".join(lines)


report = format_errors_for_report(errors)
print(report)


# =====================
# 坏例子：不检查字段数
# =====================

print("\n=== 坏例子：不检查字段数 ===")


def filter_404_logs_bad(csv_lines: list[str]) -> list[dict]:
    """坏例子：不检查字段数，可能抛出 IndexError

    不要这样写！
    """
    errors = []
    for line in csv_lines:
        parts = line.split(",")
        # 没有检查 len(parts)，直接访问 parts[4]
        if parts[4] == "404":  # 如果行不完整，这里会崩溃
            errors.append({
                "time": parts[0],
                "ip": parts[1],
                "path": parts[3]
            })
    return errors


# 测试坏例子
bad_logs = [
    "timestamp,ip,method,path,status",
    "2026-02-09,incomplete,line",  # 字段不足
    "2026-02-09 14:32:10,192.168.1.1,GET,/api/products,404"
]

try:
    filter_404_logs_bad(bad_logs)
except IndexError as e:
    print(f"坏例子处理不完整的行会抛出 IndexError: {e}")
