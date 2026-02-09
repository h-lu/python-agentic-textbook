"""
示例：边界情况处理 - 防御性编程

本例演示文本处理中的常见陷阱和防御性编程技巧，
包括编码问题、空字符串、贪婪匹配等。

运行方式：
    python3 chapters/week_09/examples/05_edge_cases.py

预期输出：
    === 编码问题处理 ===
    尝试 utf-8 编码...
    成功用 utf-8 编码读取
    文件内容: Hello, World!
    === 忽略/替换错误字符 ===
    忽略模式: Hello World
    替换模式: Hello � World
    === 空字符串和空白字符陷阱 ===
    空字符串 split: ['']
    "a,b," split: ['a', 'b', '']
    "hello\n".strip(): 'hello'
    "hello\t".strip(): 'hello'
    "hello\r\n".strip(): 'hello'
    === 安全解析日志文件 ===
    警告: 第 4 行格式不正确，已跳过
    解析结果: [{'timestamp': '2026-02-09 14:32:01', 'level': 'ERROR', 'message': '数据库连接超时'}]
    === 处理不存在的文件 ===
    错误: 文件 /path/to/nonexistent.log 不存在
    返回空列表: []
"""

import tempfile
from pathlib import Path


# =====================
# 编码问题处理
# =====================

print("=== 编码问题处理 ===")


def read_with_encoding_fallback(file_path: str | Path) -> str:
    """尝试多种编码读取文件

    Args:
        file_path: 文件路径

    Returns:
        文件内容字符串

    Raises:
        UnicodeDecodeError: 如果所有编码都失败
    """
    encodings = ["utf-8", "gbk", "latin-1"]

    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                content = f.read()
            print(f"尝试 {enc} 编码... 成功")
            return content
        except UnicodeDecodeError:
            print(f"尝试 {enc} 编码... 失败")
            continue

    raise UnicodeDecodeError(f"无法用任何已知编码读取文件: {file_path}")


# 创建测试文件
with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".txt") as f:
    f.write("Hello, World!")
    test_file = f.name

content = read_with_encoding_fallback(test_file)
print(f"文件内容: {content}")

# 清理
Path(test_file).unlink()


# =====================
# 忽略/替换错误字符
# =====================

print("\n=== 忽略/替换错误字符 ===")

# 创建一个包含无效 UTF-8 字节的文件
with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as f:
    f.write(b"Hello \xb0 World")  # \xb0 是 GBK 的度符号，不是有效的 UTF-8
    binary_file = f.name

# 方法 1：忽略无法解码的字符
with open(binary_file, "r", encoding="utf-8", errors="ignore") as f:
    content_ignore = f.read()
print(f"忽略模式: {content_ignore}")

# 方法 2：用 � 替换无法解码的字符
with open(binary_file, "r", encoding="utf-8", errors="replace") as f:
    content_replace = f.read()
print(f"替换模式: {content_replace}")

# 清理
Path(binary_file).unlink()


# =====================
# 空字符串和空白字符陷阱
# =====================

print("\n=== 空字符串和空白字符陷阱 ===")

# 陷阱 1：空字符串 split
empty_split = "".split(",")
print(f"空字符串 split: {empty_split}")  # 输出: [''] —— 不是空列表！

# 陷阱 2：末尾分隔符
trailing_split = "a,b,".split(",")
print(f'"a,b," split: {trailing_split}')  # 输出: ['a', 'b', ''] —— 末尾有空字符串

# 各种空白字符
print(f'"hello\\n".strip(): {repr("hello\n".strip())}')
print(f'"hello\\t".strip(): {repr("hello\t".strip())}')
print(f'"hello\\r\\n".strip(): {repr("hello\r\n".strip())}')


# =====================
# 安全解析日志文件
# =====================

print("\n=== 安全解析日志文件 ===")


def parse_log_line(line: str) -> dict | None:
    """解析单行日志"""
    bracket_end = line.find("]")
    colon_pos = line.find(":")

    if bracket_end == -1 or colon_pos == -1:
        return None

    timestamp = line[1:bracket_end]
    level = line[bracket_end + 2:colon_pos].strip()
    message = line[colon_pos + 2:]

    return {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }


def safe_parse_logs(file_path: str | Path) -> list[dict]:
    """安全地解析日志文件，处理各种边界情况

    Args:
        file_path: 日志文件路径

    Returns:
        解析后的日志记录列表
    """
    results = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # 跳过空行
                if not line:
                    continue

                # 跳过注释行（假设以 # 开头）
                if line.startswith("#"):
                    continue

                # 解析逻辑
                parsed = parse_log_line(line)
                if parsed:
                    results.append(parsed)
                else:
                    print(f"警告: 第 {line_num} 行格式不正确，已跳过")

    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 不存在")
    except Exception as e:
        print(f"错误: 读取文件时发生异常 - {e}")

    return results


# 创建测试日志文件
log_content = """# 这是注释行

[2026-02-09 14:32:01] ERROR: 数据库连接超时

这行格式不对，会被跳过
[2026-02-09 14:32:02] INFO: 用户登录成功
"""

with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".log") as f:
    f.write(log_content)
    log_file = f.name

# 只取第一条有效记录来演示
results = safe_parse_logs(log_file)[:1]
print(f"解析结果: {results}")

# 清理
Path(log_file).unlink()


# =====================
# 处理不存在的文件
# =====================

print("\n=== 处理不存在的文件 ===")

results = safe_parse_logs("/path/to/nonexistent.log")
print(f"返回空列表: {results}")


# =====================
# 坏例子：不做任何错误处理
# =====================

print("\n=== 坏例子：不做任何错误处理 ===")


def unsafe_parse_logs(file_path: str) -> list[dict]:
    """坏例子：不做错误处理

    可能抛出各种异常：
    - FileNotFoundError: 文件不存在
    - UnicodeDecodeError: 编码错误
    - IndexError: 解析时越界
    """
    results = []

    with open(file_path, "r") as f:  # 没有指定编码
        for line in f:
            # 没有 strip，可能包含换行符
            # 没有检查空行
            parts = line.split(",")
            # 没有检查字段数，直接访问
            results.append({
                "time": parts[0],
                "ip": parts[1],
                "status": parts[2]
            })

    return results


# 测试坏例子
try:
    unsafe_parse_logs("/nonexistent/file.log")
except FileNotFoundError as e:
    print(f"坏例子抛出 FileNotFoundError: {e}")

# 创建一个格式错误的文件来测试
try:
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".csv") as f:
        f.write("timestamp,ip,status\n")
        f.write("2026-02-09")  # 字段不足
        bad_csv = f.name

    result = unsafe_parse_logs(bad_csv)
    print(f"坏例子返回: {result}")
except IndexError as e:
    print(f"坏例子抛出 IndexError: {e}")
finally:
    Path(bad_csv).unlink(missing_ok=True)

print("\n提示：永远要处理文件不存在、编码错误、格式不正确的情况！")
