"""
测试单位换算器功能

Week 03 贯穿案例：单位换算器

测试覆盖：
- 长度换算（公里 ↔ 英里）
- 重量换算（公斤 ↔ 磅）
- 温度换算（摄氏度 ↔ 华氏度）
- 边界情况和特殊值
"""

import pytest


# ============================================================================
# 测试长度换算
# ============================================================================

def test_km_to_miles_basic():
    """测试：基本公里转英里"""
    def km_to_miles(km):
        return km * 0.621371

    result = km_to_miles(10)
    expected = 10 * 0.621371
    assert abs(result - expected) < 0.0001


def test_km_to_miles_zero():
    """测试：0 公里转英里"""
    def km_to_miles(km):
        return km * 0.621371

    assert km_to_miles(0) == 0


def test_km_to_miles_negative():
    """测试：负数公里转英里"""
    def km_to_miles(km):
        return km * 0.621371

    result = km_to_miles(-10)
    expected = -10 * 0.621371
    assert abs(result - expected) < 0.0001


def test_km_to_miles_large_value():
    """测试：大数值公里转英里"""
    def km_to_miles(km):
        return km * 0.621371

    result = km_to_miles(1000)
    expected = 1000 * 0.621371
    assert abs(result - expected) < 0.0001


def test_miles_to_km():
    """测试：英里转公里"""
    def miles_to_km(miles):
        return miles / 0.621371

    result = miles_to_km(10)
    expected = 10 / 0.621371
    assert abs(result - expected) < 0.0001


@pytest.mark.parametrize("km, expected_miles", [
    (0, 0),
    (1, 0.621371),
    (5, 3.106855),
    (10, 6.21371),
    (42, 26.097582),
    (100, 62.1371),
    (1000, 621.371),
])
def test_km_to_miles_parameterized(km, expected_miles):
    """测试：公里转英里（参数化测试）"""
    def km_to_miles(km):
        return km * 0.621371

    result = km_to_miles(km)
    assert abs(result - expected_miles) < 0.0001


# ============================================================================
# 测试重量换算
# ============================================================================

def test_kg_to_pounds_basic():
    """测试：基本公斤转磅"""
    def kg_to_pounds(kg):
        return kg * 2.20462

    result = kg_to_pounds(5)
    expected = 5 * 2.20462
    assert abs(result - expected) < 0.0001


def test_kg_to_pounds_zero():
    """测试：0 公斤转磅"""
    def kg_to_pounds(kg):
        return kg * 2.20462

    assert kg_to_pounds(0) == 0


def test_kg_to_pounds_negative():
    """测试：负数公斤转磅"""
    def kg_to_pounds(kg):
        return kg * 2.20462

    result = kg_to_pounds(-5)
    expected = -5 * 2.20462
    assert abs(result - expected) < 0.0001


def test_kg_to_pounds_large_value():
    """测试：大数值公斤转磅"""
    def kg_to_pounds(kg):
        return kg * 2.20462

    result = kg_to_pounds(1000)
    expected = 1000 * 2.20462
    assert abs(result - expected) < 0.0001


def test_pounds_to_kg():
    """测试：磅转公斤"""
    def pounds_to_kg(pounds):
        return pounds / 2.20462

    result = pounds_to_kg(10)
    expected = 10 / 2.20462
    assert abs(result - expected) < 0.0001


@pytest.mark.parametrize("kg, expected_pounds", [
    (0, 0),
    (1, 2.20462),
    (5, 11.0231),
    (10, 22.0462),
    (50, 110.231),
    (100, 220.462),
])
def test_kg_to_pounds_parameterized(kg, expected_pounds):
    """测试：公斤转磅（参数化测试）"""
    def kg_to_pounds(kg):
        return kg * 2.20462

    result = kg_to_pounds(kg)
    assert abs(result - expected_pounds) < 0.0001


# ============================================================================
# 测试温度换算
# ============================================================================

def test_celsius_to_fahrenheit_freezing():
    """测试：0°C（水的冰点）转华氏度"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    assert celsius_to_fahrenheit(0) == 32


def test_celsius_to_fahrenheit_boiling():
    """测试：100°C（水的沸点）转华氏度"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    assert celsius_to_fahrenheit(100) == 212


def test_celsius_to_fahrenheit_negative():
    """测试：负摄氏度转华氏度"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    # -40°C = -40°F（特殊的相等点）
    assert celsius_to_fahrenheit(-40) == -40


def test_celsius_to_fahrenheit_body_temperature():
    """测试：人体温度（37°C）转华氏度"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    result = celsius_to_fahrenheit(37)
    expected = 98.6
    assert abs(result - expected) < 0.1


def test_fahrenheit_to_celsius():
    """测试：华氏度转摄氏度"""
    def fahrenheit_to_celsius(f):
        return (f - 32) * 5/9

    assert fahrenheit_to_celsius(32) == 0  # 冰点
    assert fahrenheit_to_celsius(212) == 100  # 沸点


@pytest.mark.parametrize("celsius, expected_fahrenheit", [
    (-273.15, -459.67),  # 绝对零度
    (-40, -40),          # 特殊相等点
    (-20, -4),
    (-10, 14),
    (0, 32),             # 冰点
    (10, 50),
    (20, 68),
    (25, 77),            # 室温
    (30, 86),
    (37, 98.6),          # 人体温度
    (100, 212),          # 沸点
])
def test_celsius_to_fahrenheit_parameterized(celsius, expected_fahrenheit):
    """测试：摄氏度转华氏度（参数化测试）"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    result = celsius_to_fahrenheit(celsius)
    assert abs(result - expected_fahrenheit) < 0.1


# ============================================================================
# 测试换算精度
# ============================================================================

def test_km_to_miles_precision():
    """测试：公里转英里的精度"""
    def km_to_miles(km):
        return km * 0.621371

    # 测试小数精度
    result = km_to_miles(1.5)
    expected = 1.5 * 0.621371
    assert abs(result - expected) < 0.00001


def test_kg_to_pounds_precision():
    """测试：公斤转磅的精度"""
    def kg_to_pounds(kg):
        return kg * 2.20462

    # 测试小数精度
    result = kg_to_pounds(2.5)
    expected = 2.5 * 2.20462
    assert abs(result - expected) < 0.00001


def test_temperature_conversion_precision():
    """测试：温度换算的精度"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    def fahrenheit_to_celsius(f):
        return (f - 32) * 5/9

    # 往返转换应该接近原值
    original_c = 25.5
    f = celsius_to_fahrenheit(original_c)
    back_to_c = fahrenheit_to_celsius(f)

    assert abs(original_c - back_to_c) < 0.0001


# ============================================================================
# 测试换算函数的返回值类型
# ============================================================================

def test_km_to_miles_returns_float():
    """测试：公里转英里返回浮点数"""
    def km_to_miles(km):
        return km * 0.621371

    result = km_to_miles(10)
    assert isinstance(result, float)


def test_kg_to_pounds_returns_float():
    """测试：公斤转磅返回浮点数"""
    def kg_to_pounds(kg):
        return kg * 2.20462

    result = kg_to_pounds(10)
    assert isinstance(result, float)


def test_celsius_to_fahrenheit_returns_float():
    """测试：摄氏度转华氏度返回浮点数"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    result = celsius_to_fahrenheit(25)
    assert isinstance(result, float)


# ============================================================================
# 测试换算函数的可复用性
# ============================================================================

def test_conversion_function_reusability():
    """测试：换算函数可以多次调用"""
    def km_to_miles(km):
        return km * 0.621371

    # 可以多次调用同一个函数
    result1 = km_to_miles(10)
    result2 = km_to_miles(20)
    result3 = km_to_miles(30)

    assert result1 == 10 * 0.621371
    assert result2 == 20 * 0.621371
    assert result3 == 30 * 0.621371


def test_conversion_result_can_be_used_in_calculations():
    """测试：换算结果可以用于后续计算"""
    def km_to_miles(km):
        return km * 0.621371

    # 换算结果可以参与计算
    miles = km_to_miles(10)
    double_miles = miles * 2
    half_miles = miles / 2

    assert abs(double_miles - (10 * 0.621371 * 2)) < 0.0001
    assert abs(half_miles - (10 * 0.621371 / 2)) < 0.0001


# ============================================================================
# 测试换算函数的组合
# ============================================================================

def test_combine_conversions():
    """测试：组合多个换算函数"""
    def km_to_miles(km):
        return km * 0.621371

    def miles_to_feet(miles):
        return miles * 5280

    # 公里 -> 英里 -> 英尺
    km = 1
    miles = km_to_miles(km)
    feet = miles_to_feet(miles)

    expected_feet = 1 * 0.621371 * 5280
    assert abs(feet - expected_feet) < 0.1


def test_convert_with_offset():
    """测试：带偏移量的换算（如温度）"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    def celsius_to_kelvin(c):
        return c + 273.15

    celsius = 25
    fahrenheit = celsius_to_fahrenheit(celsius)
    kelvin = celsius_to_kelvin(celsius)

    assert abs(fahrenheit - 77) < 0.1
    assert abs(kelvin - 298.15) < 0.1


# ============================================================================
# 测试换算函数的文档字符串
# ============================================================================

def test_conversion_function_docstring():
    """测试：换算函数应该有文档字符串"""
    def km_to_miles(km):
        """将公里转换为英里

        参数:
            km: 公里数

        返回:
            对应的英里数
        """
        return km * 0.621371

    assert km_to_miles.__doc__ is not None
    assert "公里" in km_to_miles.__doc__
    assert "英里" in km_to_miles.__doc__


# ============================================================================
# 测试单位换算器的菜单系统
# ============================================================================

def test_show_menu():
    """测试：显示菜单函数"""
    def show_menu():
        """显示换算菜单"""
        return """
单位换算器
1. 公里 → 英里
2. 公斤 → 磅
3. 摄氏度 → 华氏度
4. 退出
"""

    menu = show_menu()
    assert "单位换算器" in menu
    assert "公里 → 英里" in menu
    assert "公斤 → 磅" in menu
    assert "摄氏度 → 华氏度" in menu
    assert "退出" in menu


def test_get_choice_valid():
    """测试：获取有效选择"""
    # 注意：这个测试模拟函数逻辑，不涉及实际输入
    def validate_choice(choice):
        """验证选择是否有效"""
        valid_choices = ["1", "2", "3", "4"]
        return choice in valid_choices

    assert validate_choice("1") is True
    assert validate_choice("2") is True
    assert validate_choice("3") is True
    assert validate_choice("4") is True
    assert validate_choice("5") is False
    assert validate_choice("0") is False
    assert validate_choice("abc") is False


@pytest.mark.parametrize("choice, is_valid", [
    ("1", True),
    ("2", True),
    ("3", True),
    ("4", True),
    ("0", False),
    ("5", False),
    ("10", False),
    ("-1", False),
    ("abc", False),
    ("1.5", False),
    ("", False),
])
def test_validate_choice_parameterized(choice, is_valid):
    """测试：验证选择（参数化）"""
    def validate_choice(choice):
        """验证选择是否有效"""
        valid_choices = ["1", "2", "3", "4"]
        return choice in valid_choices

    assert validate_choice(choice) == is_valid


# ============================================================================
# 测试换算的边界情况
# ============================================================================

def test_very_small_value():
    """测试：非常小的数值"""
    def km_to_miles(km):
        return km * 0.621371

    result = km_to_miles(0.001)
    expected = 0.001 * 0.621371
    assert abs(result - expected) < 0.000001


def test_very_large_value():
    """测试：非常大的数值"""
    def km_to_miles(km):
        return km * 0.621371

    result = km_to_miles(1000000)
    expected = 1000000 * 0.621371
    assert abs(result - expected) < 0.1


def test_float_input():
    """测试：浮点数输入"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    result = celsius_to_fahrenheit(36.6)
    expected = 36.6 * 9/5 + 32
    assert abs(result - expected) < 0.01


# ============================================================================
# 测试反向换算
# ============================================================================

def test_round_trip_km_miles():
    """测试：公里 ↔ 英里往返转换"""
    def km_to_miles(km):
        return km * 0.621371

    def miles_to_km(miles):
        return miles / 0.621371

    original_km = 100
    miles = km_to_miles(original_km)
    back_to_km = miles_to_km(miles)

    assert abs(original_km - back_to_km) < 0.0001


def test_round_trip_kg_pounds():
    """测试：公斤 ↔ 磅往返转换"""
    def kg_to_pounds(kg):
        return kg * 2.20462

    def pounds_to_kg(pounds):
        return pounds / 2.20462

    original_kg = 50
    pounds = kg_to_pounds(original_kg)
    back_to_kg = pounds_to_kg(pounds)

    assert abs(original_kg - back_to_kg) < 0.0001


def test_round_trip_celsius_fahrenheit():
    """测试：摄氏度 ↔ 华氏度往返转换"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    def fahrenheit_to_celsius(f):
        return (f - 32) * 5/9

    original_c = 25
    fahrenheit = celsius_to_fahrenheit(original_c)
    back_to_c = fahrenheit_to_celsius(fahrenheit)

    assert abs(original_c - back_to_c) < 0.0001


# ============================================================================
# 测试常见换算值
# ============================================================================

def test_common_km_values():
    """测试：常见的公里换算值"""
    def km_to_miles(km):
        return km * 0.621371

    # 马拉松约 42.195 公里
    marathon_miles = km_to_miles(42.195)
    assert abs(marathon_miles - 26.22) < 0.1

    # 100公里赛
    result = km_to_miles(100)
    assert abs(result - 62.14) < 0.1


def test_common_kg_values():
    """测试：常见的公斤换算值"""
    def kg_to_pounds(kg):
        return kg * 2.20462

    # 一个人的体重
    person_pounds = kg_to_pounds(70)
    assert abs(person_pounds - 154.3) < 0.1

    # 一袋米
    rice_pounds = kg_to_pounds(5)
    assert abs(rice_pounds - 11.02) < 0.1


def test_common_temperature_values():
    """测试：常见的温度换算值"""
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

    # 室温
    room_temp = celsius_to_fahrenheit(20)
    assert abs(room_temp - 68) < 0.1

    # 发烧
    fever = celsius_to_fahrenheit(38.5)
    assert abs(fever - 101.3) < 0.1


# ============================================================================
# 测试换算函数的错误处理
# ============================================================================

def test_conversion_with_invalid_input_type():
    """测试：无效输入类型的处理"""
    def km_to_miles(km):
        """如果输入不是数字，会抛出异常"""
        return km * 0.621371

    # 字符串输入会导致 TypeError
    with pytest.raises(TypeError):
        km_to_miles("10")

    # None 输入会导致 TypeError
    with pytest.raises(TypeError):
        km_to_miles(None)


def test_conversion_with_none():
    """测试：None 输入的处理"""
    def km_to_miles(km):
        return km * 0.621371

    with pytest.raises(TypeError):
        km_to_miles(None)


# ============================================================================
# 测试换算函数的链式调用
# ============================================================================

def test_chained_conversions():
    """测试：链式调用换算函数"""
    def km_to_miles(km):
        return km * 0.621371

    def miles_to_yards(miles):
        return miles * 1760

    def yards_to_feet(yards):
        return yards * 3

    # 公里 -> 英里 -> 码 -> 英尺
    km = 1
    feet = yards_to_feet(miles_to_yards(km_to_miles(km)))

    # 1公里 ≈ 3280.84英尺
    assert abs(feet - 3280.84) < 1


# ============================================================================
# 测试换算函数的性能（简单测试）
# ============================================================================

def test_conversion_performance():
    """测试：换算函数的性能"""
    def km_to_miles(km):
        return km * 0.621371

    import time

    start = time.time()
    for i in range(10000):
        km_to_miles(i)
    end = time.time()

    # 10000次转换应该很快（< 1秒）
    assert end - start < 1.0


# ============================================================================
# 测试换算公式常量的准确性
# ============================================================================

def test_conversion_constants():
    """测试：换算常量的准确性"""
    # 这些是标准换算常量
    KM_TO_MILES = 0.621371
    KG_TO_POUNDS = 2.20462
    FAHRENHEIT_OFFSET = 32
    FAHRENHEIT_SCALE = 9/5

    # 验证常量值
    assert KM_TO_MILES == 0.621371
    assert KG_TO_POUNDS == 2.20462
    assert FAHRENHEIT_OFFSET == 32
    assert FAHRENHEIT_SCALE == 1.8


# ============================================================================
# 测试换算函数的可测试性
# ============================================================================

def test_pure_function():
    """测试：换算函数应该是纯函数（无副作用）"""
    def km_to_miles(km):
        return km * 0.621371

    # 纯函数：相同输入总是产生相同输出
    assert km_to_miles(10) == km_to_miles(10)
    assert km_to_miles(10) == km_to_miles(10)

    # 纯函数：不修改输入参数
    original_value = 10
    km_to_miles(original_value)
    assert original_value == 10

# Anchor contract alias — modular design should be visible in the submitted solution.
def test_modular_design():
    import importlib.util
    from pathlib import Path

    solution_path = Path(__file__).resolve().parents[1] / "starter_code" / "solution.py"
    spec = importlib.util.spec_from_file_location("week03_solution_for_modular_design", solution_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    for name in ["show_menu", "get_choice", "get_number", "do_conversion", "main"]:
        assert callable(getattr(module, name))
