"""
Week 03 作业参考实现

本文件是作业的参考实现，当你在作业中遇到困难时可以查看。
注意：这是基础要求的参考实现，进阶/挑战部分需要你自己完成。

运行方式：python3 chapters/week_03/starter_code/solution.py
预期输出：一个有菜单的单位换算器
"""


# =====================
# 核心换算函数
# =====================

def km_to_miles(km):
    """公里转英里"""
    return km * 0.621371


def miles_to_km(miles):
    """英里转公里"""
    return miles / 0.621371


def kg_to_pounds(kg):
    """公斤转磅"""
    return kg * 2.20462


def pounds_to_kg(pounds):
    """磅转公斤"""
    return pounds / 2.20462


def celsius_to_fahrenheit(c):
    """摄氏度转华氏度"""
    return c * 9/5 + 32


def rectangle_area(width, height):
    """计算矩形面积"""
    return width * height


def rectangle_perimeter(width, height):
    """计算矩形周长"""
    return (width + height) * 2


def fahrenheit_to_celsius(f):
    """华氏度转摄氏度"""
    return (f - 32) * 5/9


# =====================
# 菜单和输入函数
# =====================

def show_menu():
    """显示菜单"""
    print("\n=== 单位换算器 ===")
    print("1. 公里 → 英里")
    print("2. 英里 → 公里")
    print("3. 公斤 → 磅")
    print("4. 磅 → 公斤")
    print("5. 摄氏度 → 华氏度")
    print("6. 华氏度 → 摄氏度")
    print("7. 退出")


def get_choice():
    """获取用户选择，带输入验证"""
    while True:
        choice = input("请选择（1-7）：")
        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            return choice
        print("无效输入，请输入 1-7")


def get_number(prompt):
    """获取数字输入，带错误处理"""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("请输入一个有效的数字！")


# =====================
# 执行换算的函数
# =====================

def do_conversion(choice):
    """根据用户选择执行换算"""
    if choice == "1":
        km = get_number("输入公里数：")
        result = km_to_miles(km)
        print(f"{km} 公里 = {result:.2f} 英里")
    elif choice == "2":
        miles = get_number("输入英里数：")
        result = miles_to_km(miles)
        print(f"{miles} 英里 = {result:.2f} 公里")
    elif choice == "3":
        kg = get_number("输入公斤数：")
        result = kg_to_pounds(kg)
        print(f"{kg} 公斤 = {result:.2f} 磅")
    elif choice == "4":
        pounds = get_number("输入磅数：")
        result = pounds_to_kg(pounds)
        print(f"{pounds} 磅 = {result:.2f} 公斤")
    elif choice == "5":
        c = get_number("输入摄氏度：")
        result = celsius_to_fahrenheit(c)
        print(f"{c}°C = {result:.2f}°F")
    elif choice == "6":
        f = get_number("输入华氏度：")
        result = fahrenheit_to_celsius(f)
        print(f"{f}°F = {result:.2f}°C")


# =====================
# 主函数
# =====================

def main():
    """主函数"""
    print("欢迎使用单位换算器！")

    while True:
        show_menu()
        choice = get_choice()

        if choice == "7":
            print("再见！")
            break

        do_conversion(choice)


# =====================
# 启动程序
# =====================

if __name__ == "__main__":
    main()


# =====================
# 设计说明
# =====================

"""
这个参考实现包含了 Week 03 作业的基础要求：

1. 函数定义：
   - 所有换算逻辑都封装在函数中
   - 每个函数只做一件事
   - 函数名清晰表达功能

2. 参数和返回值：
   - 所有换算函数都接受参数
   - 所有换算函数都返回计算结果
   - 调用者决定如何处理结果（这里是打印）
   - rectangle_area() 和 rectangle_perimeter() 对应基础作业中的矩形练习

3. 函数分解：
   - show_menu(): 显示菜单
   - get_choice(): 获取并验证用户选择
   - get_number(): 获取并验证数字输入
   - do_conversion(): 根据选择执行相应换算
   - main(): 主循环

4. 错误处理：
   - get_choice() 验证菜单选择是否有效
   - get_number() 处理非数字输入（用 try/except）

5. 代码复用：
   - 每个换算函数都是独立的
   - 可以在任何地方调用这些函数
   - 换算函数不涉及输入输出，只做计算

进阶挑战建议：
- 加上"历史记录"功能，记录用户的换算历史
- 支持"批量换算"，一次输入多个值
- 加上"常用换算"快捷选项
- 用字典存储换算率，进一步减少重复代码
"""
