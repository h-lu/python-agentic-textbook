"""
Week 01 作业参考实现：个人名片生成器

这是基础作业的参考实现，展示了如何使用 print、变量、input 和 f-string
创建一个交互式的个人名片生成器。
"""

# 打印欢迎信息
print("=" * 40)
print("       欢迎使用个人名片生成器")
print("=" * 40)
print()

# 获取用户输入
name = input("请输入您的姓名：")
age = input("请输入您的年龄：")
job = input("请输入您的职业：")
age_display = age if age.endswith("岁") else f"{age} 岁"

# 使用 f-string 格式化输出名片
print("\n" + "=" * 40)
print("            个人名片")
print("=" * 40)
print(f"  姓名：{name}")
print(f"  年龄：{age_display}")
print(f"  职业：{job}")
print("=" * 40)
print("\n名片生成成功！")
