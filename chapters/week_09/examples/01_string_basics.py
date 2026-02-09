"""
示例：字符串基础操作 - 索引、切片、find、strip

本例演示如何用字符串方法从日志行中提取信息，
以及为什么硬编码切片是脆弱的。

运行方式：
    python3 chapters/week_09/examples/01_string_basics.py

预期输出：
    === 硬编码切片的问题 ===
    时间: 2026-02-09 14:32:01
    级别: ERROR
    消息: 数据库连接超时
    ERROR 日志的级别: 'ERROR'
    INFO 日志的级别: 'INFO:'  <-- 多了一个冒号！
    === 使用 find() 定位 ===
    右方括号位置: 20
    第一个冒号位置: 14
    最后一个冒号位置: 27
    时间戳: 2026-02-09 14:32:01
    级别: ERROR
    === strip() 清洗 ===
    清洗前: '  WARNING '
    清洗后: 'WARNING'
    去除方括号: 'ERROR'
    去除横线: 'hello'
    === 字符串是不可变的 ===
    upper() 后原字符串: 'hello'
    重新赋值后: 'HELLO'
    === 健壮的解析函数 ===
    {'timestamp': '2026-02-09 14:32:01', 'level': 'ERROR', 'message': '数据库连接超时'}
    {'timestamp': '2026-02-09 14:32:02', 'level': 'INFO', 'message': '用户登录成功'}
    无效格式返回: None
"""


# =====================
# 硬编码切片的问题
# =====================

print("=== 硬编码切片的问题 ===")

log_line = "[2026-02-09 14:32:01] ERROR: 数据库连接超时"

# 硬编码切片 - 脆弱！
timestamp = log_line[1:20]      # 提取 "2026-02-09 14:32:01"
level = log_line[22:27]         # 提取 "ERROR"
message = log_line[29:]         # 提取 "数据库连接超时"

print(f"时间: {timestamp}")
print(f"级别: {level}")
print(f"消息: {message}")

# 问题：如果日志级别长度不同呢？
error_log = "[2026-02-09 14:32:01] ERROR: 数据库连接超时"
info_log = "[2026-02-09 14:32:02] INFO: 用户登录成功"

print(f"ERROR 日志的级别: '{error_log[22:27]}'")
print(f"INFO 日志的级别: '{info_log[22:27]}'  <-- 多了一个冒号！")


# =====================
# 使用 find() 定位
# =====================

print("\n=== 使用 find() 定位 ===")

log_line = "[2026-02-09 14:32:01] ERROR: 数据库连接超时"

# 找到右方括号的位置
bracket_end = log_line.find("]")
print(f"右方括号位置: {bracket_end}")  # 输出: 20

# 找到第一个冒号的位置（在时间戳里）
colon_pos_first = log_line.find(":")
print(f"第一个冒号位置: {colon_pos_first}")  # 输出: 14

# 找到最后一个冒号的位置（在日志级别后面）
colon_pos_last = log_line.find(":", bracket_end)
print(f"最后一个冒号位置: {colon_pos_last}")  # 输出: 27

# 提取方括号里的时间戳（不包括方括号）
timestamp = log_line[1:bracket_end]
print(f"时间戳: {timestamp}")

# 提取日志级别（方括号和冒号之间，去掉空格）
level = log_line[bracket_end+2:colon_pos_last].strip()
print(f"级别: {level}")


# =====================
# strip() 清洗
# =====================

print("\n=== strip() 清洗 ===")

# 如果日志级别前后有空格
log_line = "[2026-02-09 14:32:01]  WARNING : 磁盘空间不足"
bracket_end = log_line.find("]")
# 从方括号后开始找冒号
colon_pos = log_line.find(":", bracket_end)
level = log_line[bracket_end+2:colon_pos]

print(f"清洗前: '{level}'")
level = level.strip()
print(f"清洗后: '{level}'")

# strip() 还可以去除指定的字符
print(f"去除方括号: '{ '[ERROR]'.strip('[]') }'")
print(f"去除横线: '{ '---hello---'.strip('-') }'")


# =====================
# 字符串是不可变的
# =====================

print("\n=== 字符串是不可变的 ===")

my_str = "hello"
my_str.upper()  # 返回 "HELLO"，但 my_str 还是 "hello"
print(f"upper() 后原字符串: '{my_str}'")  # 还是 "hello"

# 必须重新赋值
my_str = my_str.upper()
print(f"重新赋值后: '{my_str}'")  # 变成 "HELLO"


# =====================
# 健壮的解析函数
# =====================

print("\n=== 健壮的解析函数 ===")


def parse_log_line(line: str) -> dict | None:
    """解析单行日志，返回字典

    Args:
        line: 日志行字符串

    Returns:
        包含 timestamp、level、message 的字典，格式错误返回 None
    """
    bracket_end = line.find("]")
    if bracket_end == -1:
        return None  # 格式不对，返回 None

    # 从方括号后开始找冒号（避免找到时间戳中的冒号）
    colon_pos = line.find(":", bracket_end)
    if colon_pos == -1:
        return None  # 格式不对，返回 None

    timestamp = line[1:bracket_end]
    level = line[bracket_end+2:colon_pos].strip()
    message = line[colon_pos+2:]

    return {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }


# 测试
log1 = "[2026-02-09 14:32:01] ERROR: 数据库连接超时"
log2 = "[2026-02-09 14:32:02] INFO: 用户登录成功"
log3 = "这行格式不对"  # 无效格式

print(parse_log_line(log1))
print(parse_log_line(log2))
print(f"无效格式返回: {parse_log_line(log3)}")


# =====================
# 坏例子：不做错误检查
# =====================


def parse_log_line_bad(line: str) -> dict:
    """坏例子：不做错误检查，可能崩溃

    如果输入格式不对，会抛出异常或返回错误结果。
    不要这样写！
    """
    # 假设格式一定正确 - 危险！
    bracket_end = line.find("]")
    # 错误：没有从 bracket_end 后开始找冒号，可能找到时间戳中的冒号
    colon_pos = line.find(":")

    # 没有检查 -1 的情况
    timestamp = line[1:bracket_end]
    level = line[bracket_end+2:colon_pos].strip()
    message = line[colon_pos+2:]

    return {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }


if __name__ == "__main__":
    # 测试坏例子
    print("\n=== 坏例子的问题 ===")
    try:
        result = parse_log_line_bad("无效格式")
        print(f"坏例子返回: {result}")  # 可能返回奇怪的结果
    except Exception as e:
        print(f"坏例子抛出异常: {e}")
