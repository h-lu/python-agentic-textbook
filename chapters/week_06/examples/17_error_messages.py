"""
示例：好的 vs 坏的错误消息

本例演示：设计友好的错误消息
运行方式：python3 chapters/week_06/examples/17_error_messages.py
预期输出：
  - 对比三种错误消息：坏的、稍好的、最好的
"""

print("=== 错误消息对比 ===\n")

# ❌ 坏：太模糊
print("1. 坏的错误消息：")
print("   raise ValueError('error')")
print("   问题：用户不知道出了什么错、为什么、怎么修复\n")

# ⚠️ 稍好：有说明，但不完整
print("2. 稍好的错误消息：")
print("   raise ValueError('年龄不能为负数')")
print("   问题：用户知道错了，但不知道怎么修复\n")

# ✅ 最好：清晰、完整、可操作
print("3. 最好的错误消息：")
print("   raise ValueError('年龄不能为负数，请输入一个正整数')")
print("   优点：告诉用户 出了什么错、为什么、怎么修复\n")

print("=== 更多对比 ===\n")

print("❌ 坏：")
print("   raise ValueError('invalid input')")
print()

print("✅ 好：")
print("   raise ValueError('日期格式不对，请输入类似 02-09 的格式')")
print()

print("❌ 坏：")
print("   raise ValueError('error')")
print()

print("✅ 好：")
print("   raise ValueError(f'年龄 {age} 超出合理范围（0-120），请重新输入')")
print()

# 好的错误信息应该告诉用户三件事：
# 1. 出了什么错（What）
# 2. 为什么出错（Why）
# 3. 怎么修复（How）

# 示例代码
def validate_age(age):
    """验证年龄的合法性"""
    if age < 0:
        raise ValueError("年龄不能为负数，请输入一个正整数")

    if age > 120:
        raise ValueError(f"年龄 {age} 超出合理范围（0-120），请重新输入")

    return age


# 测试
try:
    age = validate_age(-5)
except ValueError as e:
    print(f"验证失败：{e}")
