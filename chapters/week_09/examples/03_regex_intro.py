r"""
示例：正则表达式入门 - 模式匹配基础

本例演示正则表达式的基本语法和 re 模块的使用，
包括元字符、原始字符串、search 和 match 的区别。

运行方式：
    python3 chapters/week_09/examples/03_regex_intro.py

预期输出：
    === 原始字符串 r"..." ===
    普通字符串 "\\d": '\\d'
    原始字符串 r"\d": '\\d'
    === 基本匹配 ===
    在 "192.168.1.1" 中找到 IP: 192.168.1.1
    在 "abc123" 中找到数字: 123
    === search vs match ===
    match("123abc"): <re.Match object; span=(0, 3), match='123'>
    match("abc123"): None
    search("abc123"): <re.Match object; span=(3, 6), match='123'>
    === 常用元字符 ===
    匹配任意字符 (.): cat, cbt, c1t
    匹配数字 (\d): 123, 42
    匹配单词字符 (\w): hello, user_123
    匹配空白 (\s): 找到空白
    匹配开头 (^): Hello world
    匹配结尾 ($): Hello world
    匹配 0次或多次 (*): , a, aaa
    匹配 1次或多次 (+): a, aaa
    匹配 0次或1次 (?): color, colour
    匹配 n到m次 ({n,m}): 12, 123, 1234
    字符集 ([]): cat
    或 (|): cat
    === 分组提取 ===
    完整匹配: 2026-02-09 14:32:01
    日期: 2026-02-09
    时间: 14:32:01
    === 邮箱匹配 ===
    简化版匹配: user@company.org
    改进版匹配: user.name@company.org
    === 坏例子：忘记原始字符串 ===
    坏例子 ("\\d+"): 需要写四个反斜杠才能匹配数字！
"""

import re


# =====================
# 原始字符串 r"..."
# =====================

print("=== 原始字符串 r\"...\" ===")

# 普通字符串：\d 会被解释成转义序列
normal = "\\d"
print(f'普通字符串 "\\d": {repr(normal)}')

# 原始字符串：\d 就是反斜杠加 d
raw = r"\d"
print(f'原始字符串 r"\\d": {repr(raw)}')

# 如果不加 r，要写 \\d 才能让正则收到 \d
# r"\d" == "\\d"  # True


# =====================
# 基本匹配
# =====================

print("\n=== 基本匹配 ===")

log_line = "[2026-02-09 14:32:01] 192.168.1.1 - GET /api/users 200"

# 搜索 IP 地址
ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
match = re.search(ip_pattern, log_line)

if match:
    print(f'在 "192.168.1.1" 中找到 IP: {match.group()}')

# 搜索数字
number_match = re.search(r"\d+", "abc123def")
if number_match:
    print(f'在 "abc123" 中找到数字: {number_match.group()}')


# =====================
# search vs match
# =====================

print("\n=== search vs match ===")

# match 只从开头匹配
match_result1 = re.match(r"\d+", "123abc")
match_result2 = re.match(r"\d+", "abc123")
print(f'match("123abc"): {match_result1}')
print(f'match("abc123"): {match_result2}')

# search 扫描整个字符串
search_result = re.search(r"\d+", "abc123")
print(f'search("abc123"): {search_result}')


# =====================
# 常用元字符
# =====================

print("\n=== 常用元字符 ===")

# . 匹配任意字符（除换行）
dot_matches = [
    re.search(r"c.t", "cat"),
    re.search(r"c.t", "cbt"),
    re.search(r"c.t", "c1t")
]
print(f"匹配任意字符 (.): {', '.join([m.group() for m in dot_matches if m])}")

# \d 匹配数字
digit_matches = [
    re.search(r"\d+", "123"),
    re.search(r"\d+", "abc42def")
]
print(f"匹配数字 (\\d): {', '.join([m.group() for m in digit_matches if m])}")

# \w 匹配字母/数字/下划线
word_match = re.search(r"\w+", "hello world")
print(f"匹配单词字符 (\\w): {word_match.group() if word_match else 'None'}")
word_match2 = re.search(r"\w+", "user_123")
print(f"匹配单词字符 (\\w): {word_match2.group() if word_match2 else 'None'}")

# \s 匹配空白
space_match = re.search(r"\s+", "hello   world")
print(f"匹配空白 (\\s): {'找到空白' if space_match else 'None'}")

# ^ 匹配开头
start_match = re.search(r"^Hello", "Hello world")
print(f"匹配开头 (^): {start_match.group() if start_match else 'None'}")

# $ 匹配结尾
end_match = re.search(r"world$", "Hello world")
print(f"匹配结尾 ($): {end_match.group() if end_match else 'None'}")

# * 匹配 0次或多次
star_matches = [
    (re.search(r"a*", ""), ""),
    (re.search(r"a*", "b"), "b"),
    (re.search(r"a*", "a"), "a"),
    (re.search(r"a*", "aaa"), "aaa")
]
print(f"匹配 0次或多次 (*): {', '.join([m.group() if m else '' for m, _ in star_matches])}")

# + 匹配 1次或多次
plus_matches = [
    re.search(r"a+", "a"),
    re.search(r"a+", "aaa")
]
print(f"匹配 1次或多次 (+): {', '.join([m.group() for m in plus_matches if m])}")

# ? 匹配 0次或1次
optional_matches = [
    (re.search(r"colou?r", "color"), "color"),
    (re.search(r"colou?r", "colour"), "colour")
]
print(f"匹配 0次或1次 (?): {', '.join([m.group() for m, _ in optional_matches if m])}")

# {n,m} 匹配 n到m次
range_matches = [
    re.search(r"\d{2,4}", "12"),
    re.search(r"\d{2,4}", "123"),
    re.search(r"\d{2,4}", "12345")  # 只匹配前4位
]
print(f"匹配 n到m次 ({{n,m}}): {', '.join([m.group() for m in range_matches if m])}")

# [] 字符集
char_class_match = re.search(r"[cb]at", "cat")
print(f"字符集 ([]): {char_class_match.group() if char_class_match else 'None'}")

# | 或
or_match = re.search(r"cat|dog", "cat")
print(f"或 (|): {or_match.group() if or_match else 'None'}")


# =====================
# 分组提取
# =====================

print("\n=== 分组提取 ===")

log_line = "[2026-02-09 14:32:01] 用户登录成功"

# 用分组提取日期和时间
pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})"
match = re.search(pattern, log_line)

if match:
    print(f"完整匹配: {match.group(0)}")
    print(f"日期: {match.group(1)}")
    print(f"时间: {match.group(2)}")


# =====================
# 邮箱匹配
# =====================

print("\n=== 邮箱匹配 ===")

log_line = "[2026-02-09 14:32:15] 收到来自 user.name@company.org 的反馈"

# 简化版邮箱正则
simple_email = r"\w+@\w+\.\w+"
match1 = re.search(simple_email, log_line)
print(f"简化版匹配: {match1.group() if match1 else 'None'}")

# 更完善的邮箱正则（支持 . 和 -）
better_email = r"[\w.-]+@[\w.-]+\.\w+"
match2 = re.search(better_email, log_line)
print(f"改进版匹配: {match2.group() if match2 else 'None'}")


# =====================
# 坏例子：忘记原始字符串
# =====================

print("\n=== 坏例子：忘记原始字符串 ===")

# 坏例子：忘记 r，要写四个反斜杠！
def match_digit_bad(text: str) -> re.Match | None:
    r"""坏例子：忘记使用原始字符串

    需要写 \\\\d+ 才能让正则引擎看到 \\d+
    非常容易出错！
    """
    return re.search("\\d+", text)  # 实际上可能无法按预期工作


# 正确做法
def match_digit_good(text: str) -> re.Match | None:
    """正确做法：使用原始字符串"""
    return re.search(r"\d+", text)


# 测试
test_text = "abc123"
bad_result = match_digit_bad(test_text)
good_result = match_digit_good(test_text)

bad_msg = "匹配成功" if bad_result else "匹配失败"
good_msg = "匹配成功" if good_result else "匹配失败"
print(f'坏例子 ("\\d+"): {bad_msg}')
print(f'好例子 (r"\\d+"): {good_msg}')
