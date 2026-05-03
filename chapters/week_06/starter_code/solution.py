"""
Week 06 作业参考实现

本文件是作业的参考实现，包含异常处理和防御性编程的核心功能。

运行方式：python3 chapters/week_06/starter_code/solution.py
预期输出：一个健壮的除法器和用户输入处理器
"""


# =====================
# 核心异常处理函数
# =====================

def safe_divide(numerator, denominator):
    """
    安全的除法器，处理除零错误

    Args:
        numerator: 分子
        denominator: 分母

    Returns:
        float: 除法结果
        None: 如果除零或输入非数字

    Raises:
        ValueError: 如果输入不是数字
        ZeroDivisionError: 如果分母为零
    """
    try:
        result = numerator / denominator
        return result
    except ZeroDivisionError:
        return None
    except TypeError:
        raise ValueError("输入必须是数字")


def get_dictionary_value(dictionary, key, default=None):
    """
    获取字典的值（EAFP 风格）

    Args:
        dictionary: 字典对象
        key: 要查找的键
        default: 键不存在时的默认值

    Returns:
        键对应的值，如果不存在则返回默认值
    """
    try:
        return dictionary[key]
    except KeyError:
        return default


def get_list_item(lst, index, default=None):
    """
    获取列表元素（EAFP 风格）

    Args:
        lst: 列表对象
        index: 索引位置
        default: 索引越界时的默认值

    Returns:
        列表元素，如果越界则返回默认值
    """
    try:
        return lst[index]
    except IndexError:
        return default


# =====================
# 输入校验函数（LBYL 风格）
# =====================

def is_positive_integer(value_str):
    """
    检查字符串是否代表正整数（LBYL 风格）

    Args:
        value_str: 要检查的字符串

    Returns:
        bool: 如果是正整数字符串则返回 True
    """
    if not isinstance(value_str, str):
        return False

    if not value_str.isdigit():
        return False

    value = int(value_str)
    return value > 0


def is_valid_age(age_str, min_age=0, max_age=120):
    """
    检查年龄是否有效（LBYL 风格）

    Args:
        age_str: 年龄字符串
        min_age: 最小年龄
        max_age: 最大年龄

    Returns:
        bool: 如果年龄在有效范围内则返回 True
    """
    if not isinstance(age_str, str):
        return False

    if not age_str.isdigit():
        return False

    age = int(age_str)
    return min_age <= age <= max_age


def is_valid_date_format(date_str):
    """
    检查日期格式是否为 MM-DD（LBYL 风格）

    Args:
        date_str: 日期字符串

    Returns:
        bool: 如果格式正确则返回 True
    """
    if not isinstance(date_str, str):
        return False

    if "-" not in date_str:
        return False

    parts = date_str.split("-")
    if len(parts) != 2:
        return False

    if len(parts[0]) != 2 or len(parts[1]) != 2:
        return False

    if not (parts[0].isdigit() and parts[1].isdigit()):
        return False

    return True


# =====================
# 带重试机制的输入获取函数
# =====================

def get_positive_integer_with_retry(prompt, max_attempts=3):
    """
    获取正整数，带重试限制

    Args:
        prompt: 提示信息
        max_attempts: 最大尝试次数

    Returns:
        int: 用户输入的正整数

    Raises:
        ValueError: 如果超过最大尝试次数
    """
    for attempt in range(max_attempts):
        value_str = input(prompt)

        if is_positive_integer(value_str):
            return int(value_str)

        remaining = max_attempts - attempt - 1
        if value_str.isdigit() or (value_str.startswith("-") and value_str[1:].isdigit()):
            print(f"错误：请输入大于 0 的整数（剩余尝试次数：{remaining}）")
        else:
            print(f"错误：请输入一个正整数（剩余尝试次数：{remaining}）")

    raise ValueError(f"输入错误次数过多，超过 {max_attempts} 次")


def get_positive_integer(prompt):
    """
    获取一个正整数（会重试直到输入正确）

    这是作业题 5 的接口；无最大重试次数。
    """
    while True:
        value_str = input(prompt)

        if value_str.startswith("-") and value_str[1:].isdigit():
            print("错误：请输入大于 0 的整数")
            continue

        if not value_str.isdigit():
            print("错误：请输入一个正整数")
            continue

        value = int(value_str)
        if value <= 0:
            print("错误：请输入大于 0 的整数")
            continue

        return value


def get_age(min_age=18, max_age=120):
    """
    获取年龄，并在年龄超出范围时抛出 ValueError

    这是作业题 6 的接口。
    """
    age = get_positive_integer(f"请输入你的年龄（{min_age}-{max_age}）：")

    if age < min_age:
        raise ValueError(f"年龄必须大于等于 {min_age}")
    if age > max_age:
        raise ValueError(f"年龄超出合理范围（最大 {max_age}）")

    return age


def get_menu_choice(min_choice, max_choice):
    """
    获取菜单选择（会重试直到输入正确）

    这是作业题 8 的接口。
    """
    while True:
        try:
            choice = int(input(f"请输入选择（{min_choice}-{max_choice}）："))
        except ValueError:
            print("错误：请输入数字，不要输入文字")
            continue

        if min_choice <= choice <= max_choice:
            return choice

        print(f"错误：请输入 {min_choice} 到 {max_choice} 之间的数字")


def get_choice_with_retry(prompt, valid_choices, max_attempts=3):
    """
    获取用户选择，带重试限制

    Args:
        prompt: 提示信息
        valid_choices: 有效选项列表
        max_attempts: 最大尝试次数

    Returns:
        str: 用户选择的值

    Raises:
        ValueError: 如果超过最大尝试次数
    """
    for attempt in range(max_attempts):
        choice = input(prompt)

        if choice in valid_choices:
            return choice

        remaining = max_attempts - attempt - 1
        if remaining > 0:
            valid_str = ", ".join(valid_choices)
            print(f"错误：请选择 {valid_str} 之一（剩余尝试次数：{remaining}）")

    raise ValueError(f"输入错误次数过多，超过 {max_attempts} 次")


# =====================
# 文件操作函数（带异常处理）
# =====================

def safe_read_file(filepath):
    """
    安全读取文件内容

    Args:
        filepath: 文件路径

    Returns:
        str: 文件内容
        None: 如果文件不存在或读取失败

    Raises:
        FileNotFoundError: 如果文件不存在（不捕获，让调用者处理）
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return None


def safe_write_file(filepath, content):
    """
    安全写入文件内容

    Args:
        filepath: 文件路径
        content: 要写入的内容

    Returns:
        bool: 成功返回 True，失败返回 False
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"写入文件时出错：{e}")
        return False


# =====================
# 自定义异常类
# =====================

class InvalidInputError(ValueError):
    """自定义异常：无效输入"""
    pass


class OutOfRangeError(ValueError):
    """自定义异常：超出范围"""
    pass


def validate_age(age, min_age=18, max_age=120):
    """
    验证年龄并抛出合适的异常

    Args:
        age: 年龄值
        min_age: 最小年龄
        max_age: 最大年龄

    Returns:
        int: 验证通过的年龄

    Raises:
        InvalidInputError: 如果年龄无效
        OutOfRangeError: 如果年龄超出范围
    """
    if not isinstance(age, (int, float)):
        raise InvalidInputError("年龄必须是数字")

    if age < min_age:
        raise OutOfRangeError(f"年龄必须大于等于 {min_age}")

    if age > max_age:
        raise OutOfRangeError(f"年龄必须小于等于 {max_age}")

    return int(age)


# =====================
# 主函数（演示用）
# =====================

def main():
    """主函数，演示异常处理功能"""
    print("=== Week 06 异常处理演示 ===\n")

    # 演示 1：安全除法
    print("【演示 1】安全除法器")
    test_cases = [
        (10, 2),
        (10, 0),
        ("abc", 2),
    ]

    for num, den in test_cases:
        try:
            result = safe_divide(num, den)
            if result is not None:
                print(f"  {num} / {den} = {result}")
            else:
                print(f"  {num} / {den} = 除零错误")
        except ValueError as e:
            print(f"  {num} / {den} = 输入错误: {e}")

    # 演示 2：字典访问（EAFP）
    print("\n【演示 2】字典访问（EAFP 风格）")
    scores = {"小北": 85, "阿码": 90}
    names = ["小北", "老潘", "阿码"]

    for name in names:
        score = get_dictionary_value(scores, name, default=0)
        print(f"  {name}: {score}")

    # 演示 3：列表访问（EAFP）
    print("\n【演示 3】列表访问（EAFP 风格）")
    numbers = [10, 20, 30, 40, 50]
    indices = [0, 2, 10, -1]

    for idx in indices:
        value = get_list_item(numbers, idx, default=None)
        print(f"  numbers[{idx}] = {value}")

    # 演示 4：输入校验（LBYL）
    print("\n【演示 4】输入校验（LBYL 风格）")
    test_inputs = ["10", "abc", "-5", "0", "100"]

    for inp in test_inputs:
        is_valid = is_positive_integer(inp)
        print(f"  '{inp}' 是正整数? {is_valid}")

    # 演示 5：年龄验证
    print("\n【演示 5】年龄验证")
    ages = [25, -5, 150, "abc"]

    for age in ages:
        try:
            validated = validate_age(age, min_age=18, max_age=120)
            print(f"  年龄 {age} 有效")
        except (InvalidInputError, OutOfRangeError) as e:
            print(f"  年龄 {age} 无效: {e}")

    print("\n=== 演示结束 ===")


# =====================
# 启动程序
# =====================

if __name__ == "__main__":
    main()


# =====================
# 设计说明
# =====================

"""
这个参考实现包含了 Week 06 作业的核心功能：

1. 异常处理（try/except）：
   - safe_divide(): 处理除零和类型错误
   - get_dictionary_value(): 处理键不存在
   - get_list_item(): 处理索引越界
   - safe_read_file(): 处理文件读取错误

2. 输入校验（LBYL 风格）：
   - is_positive_integer(): 检查是否为正整数
   - is_valid_age(): 检查年龄是否有效
   - is_valid_date_format(): 检查日期格式

3. 自定义异常：
   - InvalidInputError: 无效输入异常
   - OutOfRangeError: 超出范围异常
   - validate_age(): 演示如何抛出自定义异常

4. 带重试机制的函数：
   - get_positive_integer_with_retry(): 限制重试次数
   - get_choice_with_retry(): 限制重试次数

5. EAFP vs LBYL：
   - 字典/列表访问使用 EAFP（先尝试再道歉）
   - 输入校验使用 LBYL（先检查再执行）

进阶挑战建议：
- 为 get_choice_with_retry 添加不区分大小写的选项匹配
- 实现一个支持范围验证的输入函数（如 get_number_in_range）
- 添加更多的自定义异常类型
- 实现一个装饰器来自动处理常见异常
- 为文件操作添加日志记录功能
"""
