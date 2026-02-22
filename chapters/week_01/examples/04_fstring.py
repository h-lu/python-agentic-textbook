"""
示例：f-string 格式化字符串基础。

展示 f-string 的基本用法和格式说明符。

运行方式：python3 chapters/week_01/examples/04_fstring.py
预期输出：
    姓名：李小明，职业：Python 学习者
    圆周率约等于 3.14
    价格：¥  19.90
    右对齐：     42
"""

name = "李小明"
job = "Python 学习者"

# 基本用法：在字符串前加 f，用 {} 插入变量
print(f"姓名：{name}，职业：{job}")

# 格式说明符：控制小数位数
pi = 3.1415926
print(f"圆周率约等于 {pi:.2f}")  # :.2f 表示保留两位小数

# 格式说明符：控制宽度和对齐
price = 19.9
print(f"价格：¥ {price:>7.2f}")  # :>7.2f = 右对齐 + 总宽度7位 + 2位小数（浮点数）

# 整数对齐
num = 42
print(f"右对齐：{num:>10}")  # :>10 表示右对齐，占10位
