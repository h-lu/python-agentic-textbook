"""
测试布尔表达式和逻辑运算符

Week 02 核心知识点：
- 比较运算符（==, !=, <, >, <=, >=）
- 逻辑运算符（and, or, not）
- 布尔值的真值判断
- 复杂布尔表达式的组合
"""

import pytest


# ============================================================================
# 测试比较运算符
# ============================================================================

def test_comparison_equal():
    """测试：相等判断（==）"""
    assert (5 == 5) is True
    assert (5 == 6) is False
    assert ("hello" == "hello") is True
    assert ("hello" == "Hello") is False  # 大小写敏感


def test_comparison_not_equal():
    """测试：不等判断（!=）"""
    assert (5 != 6) is True
    assert (5 != 5) is False
    assert ("hello" != "world") is True


def test_comparison_less_than():
    """测试：小于判断（<）"""
    assert (3 < 5) is True
    assert (5 < 3) is False
    assert (5 < 5) is False  # 不包含等于


def test_comparison_less_equal():
    """测试：小于等于（<=）"""
    assert (3 <= 5) is True
    assert (5 <= 5) is True  # 包含等于
    assert (6 <= 5) is False


def test_comparison_greater_than():
    """测试：大于判断（>）"""
    assert (5 > 3) is True
    assert (3 > 5) is False
    assert (5 > 5) is False  # 不包含等于


def test_comparison_greater_equal():
    """测试：大于等于（>=）"""
    assert (5 >= 3) is True
    assert (5 >= 5) is True  # 包含等于
    assert (3 >= 5) is False


@pytest.mark.parametrize("a, b, result", [
    (5, 5, True),
    (5, 6, False),
    (-1, -1, True),
    (0, 0, True),
    (3.14, 3.14, True),
])
def test_comparison_equal_parametrized(a, b, result):
    """测试：相等判断的参数化测试"""
    assert (a == b) is result


@pytest.mark.parametrize("a, b, result", [
    (1, 2, True),
    (2, 1, False),
    (1, 1, False),
    (-1, 0, True),
    (0, 1, True),
])
def test_comparison_less_than_parametrized(a, b, result):
    """测试：小于判断的参数化测试"""
    assert (a < b) is result


# ============================================================================
# 测试逻辑运算符 - and
# ============================================================================

def test_logical_and_both_true():
    """测试：and 运算 - 两个都为 True"""
    assert (True and True) is True


def test_logical_and_one_false():
    """测试：and 运算 - 一个为 False"""
    assert (True and False) is False
    assert (False and True) is False


def test_logical_and_both_false():
    """测试：and 运算 - 两个都为 False"""
    assert (False and False) is False


def test_logical_and_with_comparisons():
    """测试：and 运算 - 结合比较运算符"""
    assert (5 > 3 and 10 > 5) is True   # 两个都对
    assert (5 > 3 and 10 < 5) is False  # 第二个错
    assert (5 < 3 and 10 > 5) is False  # 第一个错


def test_logical_and_short_circuit():
    """测试：and 运算 - 短路求值（第一个为 False 就不判断第二个）"""
    count = 0

    def increment():
        nonlocal count
        count += 1
        return True

    # 第一个条件为 False，increment() 不会被调用
    result = False and increment()

    assert result is False
    assert count == 0  # increment 没被调用


# ============================================================================
# 测试逻辑运算符 - or
# ============================================================================

def test_logical_or_both_true():
    """测试：or 运算 - 两个都为 True"""
    assert (True or True) is True


def test_logical_or_one_true():
    """测试：or 运算 - 一个为 True"""
    assert (True or False) is True
    assert (False or True) is True


def test_logical_or_both_false():
    """测试：or 运算 - 两个都为 False"""
    assert (False or False) is False


def test_logical_or_with_comparisons():
    """测试：or 运算 - 结合比较运算符"""
    assert (5 > 10 or 3 > 2) is True   # 第二个对
    assert (5 > 3 or 10 < 5) is True   # 第一个对
    assert (5 < 3 or 10 < 5) is False  # 两个都错


def test_logical_or_short_circuit():
    """测试：or 运算 - 短路求值（第一个为 True 就不判断第二个）"""
    count = 0

    def increment():
        nonlocal count
        count += 1
        return True

    # 第一个条件为 True，increment() 不会被调用
    result = True or increment()

    assert result is True
    assert count == 0  # increment 没被调用


# ============================================================================
# 测试逻辑运算符 - not
# ============================================================================

def test_logical_not_true():
    """测试：not 运算 - 取反 True"""
    assert (not True) is False


def test_logical_not_false():
    """测试：not 运算 - 取反 False"""
    assert (not False) is True


def test_logical_not_with_comparisons():
    """测试：not 运算 - 结合比较运算符"""
    assert (not (5 > 10)) is True      # 5 > 10 是 False，not 后是 True
    assert (not (5 > 3)) is False      # 5 > 3 是 True，not 后是 False


def test_logical_not_with_complex_expressions():
    """测试：not 运算 - 结合复杂表达式"""
    assert (not (5 > 3 and 10 > 5)) is False  # 原式为 True，not 后为 False
    assert (not (5 < 3 and 10 > 5)) is True   # 原式为 False，not 后为 True


# ============================================================================
# 测试复杂布尔表达式
# ============================================================================

def test_complex_and_or_combination():
    """测试：and 和 or 的组合"""
    # (5 > 3) and (10 > 5) or (1 > 2)
    # = True and True or False
    # = True or False
    # = True
    assert ((5 > 3 and 10 > 5) or (1 > 2)) is True


def test_difficulty_validation():
    """测试：难度选择的验证（isdigit() 和范围检查）"""
    difficulty = "2"

    # 检查是否为数字且在 1-3 之间
    is_valid = difficulty.isdigit() and (1 <= int(difficulty) <= 3)

    assert is_valid is True


def test_difficulty_validation_invalid():
    """测试：难度选择的验证 - 无效输入"""
    difficulty = "5"

    is_valid = difficulty.isdigit() and (1 <= int(difficulty) <= 3)

    assert is_valid is False


def test_age_discount_eligibility():
    """测试：优惠票价资格（未成年或老年）"""
    age = 66  # 改为 66 岁，因为条件是 > 65

    # 18 岁以下或 65 岁以上可享受优惠
    is_eligible = age < 18 or age > 65

    assert is_eligible is True


def test_age_discount_not_eligible():
    """测试：优惠票价资格 - 不符合条件"""
    age = 30

    is_eligible = age < 18 or age > 65

    assert is_eligible is False


def test_age_discount_boundary_exactly_65():
    """测试：优惠票价资格 - 正好 65 岁（不符合条件，因为条件是 > 65）"""
    age = 65

    is_eligible = age < 18 or age > 65

    assert is_eligible is False  # 65 岁不享受优惠（必须 > 65）


def test_username_validation():
    """测试：用户名验证（长度 3-20 且只包含字母数字）"""
    username = "user123"

    # 简化版：只检查长度和是否为字母数字
    is_valid = username.isalnum() and (3 <= len(username) <= 20)

    assert is_valid is True


def test_username_validation_too_short():
    """测试：用户名验证 - 太短"""
    username = "ab"

    is_valid = username.isalnum() and (3 <= len(username) <= 20)

    assert is_valid is False


def test_username_validation_special_chars():
    """测试：用户名验证 - 包含特殊字符"""
    username = "user@123"

    is_valid = username.isalnum() and (3 <= len(username) <= 20)

    assert is_valid is False


# ============================================================================
# 测试 in 和 not in 运算符
# ============================================================================

def test_in_operator_list():
    """测试：in 运算符 - 列表"""
    assert (3 in [1, 2, 3, 4, 5]) is True
    assert (6 in [1, 2, 3, 4, 5]) is False


def test_in_operator_string():
    """测试：in 运算符 - 字符串（子串）"""
    assert ("hello" in "hello world") is True
    assert ("xyz" in "hello world") is False


def test_not_in_operator_list():
    """测试：not in 运算符 - 列表"""
    assert (6 not in [1, 2, 3, 4, 5]) is True
    assert (3 not in [1, 2, 3, 4, 5]) is False


def test_difficulty_not_in_valid_values():
    """测试：难度不在有效值范围内（老潘推荐的写法）"""
    difficulty = 5

    is_invalid = difficulty not in [1, 2, 3]

    assert is_invalid is True


def test_difficulty_in_valid_values():
    """测试：难度在有效值范围内"""
    difficulty = 2

    is_valid = difficulty in [1, 2, 3]

    assert is_valid is True


# ============================================================================
# 测试布尔表达式简化（可读性优化）
# ============================================================================

def test_complex_condition_vs_variable():
    """测试：复杂布尔表达式 vs 命名变量"""
    difficulty = 2
    max_num = 100

    # 复杂表达式（不推荐）
    complex_condition = (difficulty == 1 and max_num == 50) or \
                        (difficulty == 2 and max_num == 100) or \
                        (difficulty == 3 and max_num == 200)

    # 简化版（推荐）
    is_valid_difficulty = difficulty in [1, 2, 3]
    is_valid_range = max_num in [50, 100, 200]
    simplified_condition = is_valid_difficulty and is_valid_range

    assert complex_condition is True
    assert simplified_condition is True


def test_de_morgan_law():
    """测试：德摩根定律（not (A or B) = not A and not B）"""
    difficulty = 5

    # 原始写法（复杂）
    original = not (difficulty == 1 or difficulty == 2 or difficulty == 3)

    # 简化写法（清晰）
    simplified = difficulty not in [1, 2, 3]

    assert original is True
    assert simplified is True
    assert original == simplified


# ============================================================================
# 测试真值判断（Truthy/Falsy）
# ============================================================================

def test_truthy_non_zero_numbers():
    """测试：非零数字为真"""
    assert bool(1) is True
    assert bool(-1) is True
    assert bool(3.14) is True


def test_falsy_zero():
    """测试：零为假"""
    assert bool(0) is False
    assert bool(0.0) is False


def test_truthy_non_empty_strings():
    """测试：非空字符串为真"""
    assert bool("hello") is True
    assert bool(" ") is True  # 空格也是真
    assert bool("0") is True  # 字符串 "0" 是真


def test_falsy_empty_string():
    """测试：空字符串为假"""
    assert bool("") is False


def test_truthy_non_empty_collections():
    """测试：非空容器为真"""
    assert bool([1, 2, 3]) is True
    assert bool({"a": 1}) is True
    assert bool((1, 2)) is True


def test_falsy_empty_collections():
    """测试：空容器为假"""
    assert bool([]) is False
    assert bool({}) is False
    assert bool(()) is False


def test_truthy_in_conditional():
    """测试：真值在条件判断中的应用"""
    # 非空列表
    items = [1, 2, 3]
    if items:
        has_items = True
    else:
        has_items = False
    assert has_items is True

    # 空列表
    empty = []
    if empty:
        has_empty = True
    else:
        has_empty = False
    assert has_empty is False


# ============================================================================
# 实际应用场景测试
# ============================================================================

def test_guess_number_validation():
    """测试：猜数字输入验证"""
    user_input = "42"

    # 检查是否为有效数字且在范围内
    is_valid_guess = user_input.isdigit() and (1 <= int(user_input) <= 100)

    assert is_valid_guess is True


def test_guess_number_validation_out_of_range():
    """测试：猜数字输入验证 - 超出范围"""
    user_input = "150"

    is_valid_guess = user_input.isdigit() and (1 <= int(user_input) <= 100)

    assert is_valid_guess is False


def test_guess_number_validation_not_number():
    """测试：猜数字输入验证 - 不是数字"""
    user_input = "abc"

    is_valid_guess = user_input.isdigit() and (1 <= int(user_input) <= 100)

    assert is_valid_guess is False


def test_game_over_condition():
    """测试：游戏结束条件（次数用完或猜中）"""
    attempts = 5
    max_attempts = 5
    guessed_correctly = False

    # 次数用完或猜中，游戏结束
    game_over = attempts >= max_attempts or guessed_correctly

    assert game_over is True


def test_should_continue_guessing():
    """测试：是否应该继续猜测"""
    attempts = 2
    max_attempts = 5
    guessed_correctly = False

    # 还有次数且没猜中，继续
    should_continue = attempts < max_attempts and not guessed_correctly

    assert should_continue is True


def test_password_strength_check():
    """测试：密码强度检查（至少 8 位且包含数字和字母）"""
    password = "abc12345"

    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    is_long_enough = len(password) >= 8

    is_strong = has_letter and has_digit and is_long_enough

    assert is_strong is True


def test_password_strength_too_short():
    """测试：密码强度检查 - 太短"""
    password = "ab1"

    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    is_long_enough = len(password) >= 8

    is_strong = has_letter and has_digit and is_long_enough

    assert is_strong is False


def test_password_strength_no_digit():
    """测试：密码强度检查 - 缺少数字"""
    password = "abcdefgh"

    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    is_long_enough = len(password) >= 8

    is_strong = has_letter and has_digit and is_long_enough

    assert is_strong is False


# ============================================================================
# 测试运算符优先级
# ============================================================================

def test_operator_precedence_comparison_vs_logical():
    """测试：比较运算符优先级高于逻辑运算符"""
    # 5 > 3 and 10 > 5
    # 等价于 (5 > 3) and (10 > 5)
    result = 5 > 3 and 10 > 5

    assert result is True


def test_operator_precedence_parentheses_matter():
    """测试：括号改变优先级"""
    # not (5 > 3 and 10 > 5)  vs  (not 5 > 3) and 10 > 5
    assert (not (5 > 3 and 10 > 5)) is False
    assert ((not 5 > 3) and 10 > 5) is False


def test_operator_precedence_or_vs_and():
    """测试：and 优先级高于 or"""
    # True or False and False
    # = True or (False and False)
    # = True or False
    # = True
    result = True or False and False
    assert result is True

    # (True or False) and False
    # = True and False
    # = False
    result_with_parens = (True or False) and False
    assert result_with_parens is False
