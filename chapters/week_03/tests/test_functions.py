"""
测试函数定义、参数和返回值

Week 03 核心知识点：
- 使用 def 语句定义函数
- 理解参数的作用
- 使用 return 返回计算结果
- 理解 return 和 print 的区别
"""

import pytest


# ============================================================================
# 测试函数定义（def 语句）
# ============================================================================

def test_function_definition_basic():
    """测试：基本函数定义"""
    def say_hello():
        return "Hello"

    assert say_hello() == "Hello"


def test_function_definition_with_docstring():
    """测试：带文档字符串的函数定义"""
    def greet():
        """向用户问好"""
        return "Hello"

    assert callable(greet)
    assert greet.__doc__ == "向用户问好"


def test_function_naming_convention():
    """测试：函数命名规范（小写加下划线）"""
    # 好的命名：小写，用下划线分隔
    def calculate_sum():
        return 1 + 1

    def get_user_name():
        return "Alice"

    assert calculate_sum() == 2
    assert get_user_name() == "Alice"


def test_function_must_be_called_to_execute():
    """测试：定义函数不等于执行，必须调用"""
    execution_count = []

    def define_only():
        execution_count.append(1)

    # 定义后不会自动执行
    assert len(execution_count) == 0

    # 调用后才执行
    define_only()
    assert len(execution_count) == 1


# ============================================================================
# 测试参数（parameter）
# ============================================================================

def test_single_parameter():
    """测试：单参数函数"""
    def double(x):
        return x * 2

    assert double(5) == 10
    assert double(10) == 20
    assert double(-3) == -6


def test_multiple_parameters():
    """测试：多参数函数"""
    def add(a, b, c):
        return a + b + c

    assert add(1, 2, 3) == 6
    assert add(10, 20, 30) == 60


def test_parameter_as_variable():
    """测试：参数本质上是函数内部的变量"""
    def use_parameter(value):
        # 参数可以在函数内部像变量一样使用
        temp = value * 2
        return temp + value

    assert use_parameter(5) == 15  # 5*2 + 5 = 15


def test_parameter_order_matters():
    """测试：参数顺序很重要"""
    def divide(a, b):
        return a / b

    # 参数顺序不同，结果不同
    assert divide(10, 2) == 5.0
    assert divide(2, 10) == 0.2


def test_parameter_name_does_not_affect_caller():
    """测试：参数名不影响调用者的变量"""
    def some_function(any_name):
        return any_name * 2

    x = 5
    result = some_function(x)
    assert result == 10
    assert x == 5  # 原变量未改变


# ============================================================================
# 测试返回值（return）
# ============================================================================

def test_return_basic():
    """测试：基本返回值"""
    def get_value():
        return 42

    assert get_value() == 42


def test_return_vs_print():
    """测试：return 和 print 的区别"""
    def with_return():
        return 42

    def with_print():
        print(42)  # 注意：这里会打印到控制台

    # return 返回值可以存储和使用
    result = with_return()
    assert result == 42

    # print 函数返回 None
    result = with_print()
    assert result is None


def test_return_early():
    """测试：return 会提前结束函数"""
    def check_positive(x):
        if x < 0:
            return "negative"
        return "positive"

    assert check_positive(-5) == "negative"
    assert check_positive(5) == "positive"


def test_return_multiple_values():
    """测试：返回多个值（实际是元组）"""
    def get_name_and_age():
        return "Alice", 25

    name, age = get_name_and_age()
    assert name == "Alice"
    assert age == 25

    # 也可以作为元组接收
    result = get_name_and_age()
    assert result == ("Alice", 25)


def test_return_different_types():
    """测试：返回不同类型的值"""
    def return_int():
        return 42

    def return_float():
        return 3.14

    def return_string():
        return "hello"

    def return_list():
        return [1, 2, 3]

    def return_dict():
        return {"key": "value"}

    assert isinstance(return_int(), int)
    assert isinstance(return_float(), float)
    assert isinstance(return_string(), str)
    assert isinstance(return_list(), list)
    assert isinstance(return_dict(), dict)


def test_return_expression_result():
    """测试：可以返回表达式的结果"""
    def calculate(a, b):
        return a + b * 2

    assert calculate(3, 4) == 11  # 3 + 4*2 = 11


def test_return_without_value_returns_none():
    """测试：没有值的 return 返回 None"""
    def return_none():
        return

    assert return_none() is None


def test_function_without_return_statement():
    """测试：没有 return 语句的函数返回 None"""
    def no_return():
        x = 42

    assert no_return() is None


# ============================================================================
# 测试函数的组合使用
# ============================================================================

def test_function_as_argument():
    """测试：函数可以作为另一个函数的参数"""
    def apply_operation(x, operation):
        return operation(x)

    def square(x):
        return x * x

    def double(x):
        return x * 2

    assert apply_operation(5, square) == 25
    assert apply_operation(5, double) == 10


def test_function_return_value_as_argument():
    """测试：函数返回值可以作为另一个函数的参数"""
    def add(a, b):
        return a + b

    def multiply(a, b):
        return a * b

    # add(3, 4) 的结果作为 multiply 的参数
    result = multiply(add(2, 3), 4)
    assert result == 20  # (2+3) * 4 = 20


def test_nested_function_calls():
    """测试：嵌套调用函数"""
    def add_one(x):
        return x + 1

    def add_two(x):
        return x + 2

    result = add_one(add_two(add_one(5)))
    assert result == 9  # ((5+1)+2)+1 = 9


# ============================================================================
# 测试函数的副作用
# ============================================================================

def test_function_can_modify_list_parameter():
    """测试：函数可以修改传入的可变对象（如列表）"""
    def add_item(lst, item):
        lst.append(item)
        return lst

    my_list = [1, 2, 3]
    result = add_item(my_list, 4)

    assert result == [1, 2, 3, 4]
    assert my_list == [1, 2, 3, 4]  # 原列表也被修改了


def test_function_cannot_modify_immutable_parameter():
    """测试：函数无法修改不可变对象（如数字、字符串）"""
    def try_to_change(x):
        x = x + 1
        return x

    original = 5
    result = try_to_change(original)

    assert result == 6
    assert original == 5  # 原变量未改变


# ============================================================================
# 测试边界情况
# ============================================================================

def test_function_with_zero_parameters():
    """测试：零参数函数"""
    def no_params():
        return 42

    assert no_params() == 42


def test_function_with_many_parameters():
    """测试：多参数函数"""
    def many_params(a, b, c, d, e):
        return a + b + c + d + e

    assert many_params(1, 2, 3, 4, 5) == 15


def test_function_returning_zero():
    """测试：函数可以返回 0"""
    def return_zero():
        return 0

    assert return_zero() == 0


def test_function_returning_empty_string():
    """测试：函数可以返回空字符串"""
    def return_empty():
        return ""

    assert return_empty() == ""


def test_function_returning_empty_list():
    """测试：函数可以返回空列表"""
    def return_empty():
        return []

    assert return_empty() == []


def test_function_with_negative_parameter():
    """测试：负数作为参数"""
    def absolute(x):
        if x < 0:
            return -x
        return x

    assert absolute(-5) == 5
    assert absolute(5) == 5
    assert absolute(0) == 0


def test_function_with_zero_as_parameter():
    """测试：0 作为参数"""
    def divide_by_zero(x):
        if x == 0:
            return "undefined"
        return 10 / x

    assert divide_by_zero(0) == "undefined"
    assert divide_by_zero(2) == 5.0


def test_function_with_large_number():
    """测试：大数作为参数"""
    def square(x):
        return x * x

    result = square(1000000)
    assert result == 1000000000000


# ============================================================================
# 测试函数文档字符串（docstring）
# ============================================================================

def test_docstring_single_line():
    """测试：单行文档字符串"""
    def func():
        """这是一个函数"""
        pass

    assert func.__doc__ == "这是一个函数"


def test_docstring_multi_line():
    """测试：多行文档字符串"""
    def func():
        """
        这是一个多行文档字符串

        可以写更多说明
        """
        pass

    assert "这是一个多行文档字符串" in func.__doc__


# ============================================================================
# 测试函数的类型提示（可选，Python 3.5+）
# ============================================================================

def test_type_hints_basic():
    """测试：基本的类型提示"""
    def add(x: int, y: int) -> int:
        return x + y

    # 类型提示不影响运行
    assert add(3, 5) == 8


def test_type_hints_optional():
    """测试：类型提示是可选的"""
    def with_hints(x: int) -> int:
        return x * 2

    def without_hints(x):
        return x * 2

    # 两者功能相同
    assert with_hints(5) == without_hints(5)


# ============================================================================
# 测试函数的调用方式
# ============================================================================

def test_positional_arguments():
    """测试：位置参数"""
    def greet(first, last):
        return f"Hello, {first} {last}"

    assert greet("Alice", "Smith") == "Hello, Alice Smith"


def test_keyword_arguments():
    """测试：关键字参数"""
    def greet(first, last):
        return f"Hello, {first} {last}"

    assert greet(last="Smith", first="Alice") == "Hello, Alice Smith"


def test_mixed_arguments():
    """测试：混合使用位置参数和关键字参数"""
    def greet(first, last, title):
        return f"{title}. {first} {last}"

    # 位置参数必须在关键字参数之前
    assert greet("Alice", last="Smith", title="Dr") == "Dr. Alice Smith"


# ============================================================================
# 测试递归函数（简单例子）
# ============================================================================

def test_simple_recursion():
    """测试：简单的递归函数"""
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    assert factorial(1) == 1
    assert factorial(3) == 6  # 3*2*1
    assert factorial(5) == 120  # 5*4*3*2*1


def test_recursive_sum():
    """测试：递归求和"""
    def recursive_sum(n):
        if n <= 0:
            return 0
        return n + recursive_sum(n - 1)

    assert recursive_sum(5) == 15  # 5+4+3+2+1+0
    assert recursive_sum(10) == 55


# ============================================================================
# 测试 lambda 函数（可选）
# ============================================================================

def test_lambda_basic():
    """测试：基本的 lambda 函数"""
    # lambda 是匿名函数
    square = lambda x: x * x

    assert square(5) == 25


def test_lambda_with_multiple_parameters():
    """测试：多参数 lambda 函数"""
    add = lambda a, b: a + b

    assert add(3, 5) == 8


def test_lambda_vs_regular_function():
    """测试：lambda 和普通函数功能相同"""
    def regular(x):
        return x * 2

    lambda_func = lambda x: x * 2

    assert regular(5) == lambda_func(5)


# ============================================================================
# 测试函数作为返回值
# ============================================================================

def test_return_function():
    """测试：函数可以返回另一个函数"""
    def get_operation(operation):
        if operation == "add":
            def add(x, y):
                return x + y
            return add
        elif operation == "multiply":
            def multiply(x, y):
                return x * y
            return multiply

    add_func = get_operation("add")
    multiply_func = get_operation("multiply")

    assert add_func(3, 5) == 8
    assert multiply_func(3, 5) == 15


# ============================================================================
# 测试闭包（函数嵌套）
# ============================================================================

def test_closure_basic():
    """测试：基本的闭包"""
    def outer(x):
        def inner():
            return x * 2
        return inner

    triple = outer(3)
    assert triple() == 6


def test_closure_multiple_calls():
    """测试：闭包可以保持状态"""
    def make_counter():
        count = [0]  # 用列表实现可变状态

        def increment():
            count[0] += 1
            return count[0]

        return increment

    counter1 = make_counter()
    counter2 = make_counter()

    assert counter1() == 1
    assert counter1() == 2
    assert counter2() == 1  # counter2 独立计数


# ============================================================================
# 测试函数的默认参数值
# ============================================================================

def test_default_parameter_value():
    """测试：参数可以有默认值"""
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}"

    assert greet("Alice") == "Hello, Alice"
    assert greet("Bob", "Hi") == "Hi, Bob"


def test_default_parameter_with_multiple_defaults():
    """测试：多个参数可以有默认值"""
    def func(a, b=10, c=20):
        return a + b + c

    assert func(1) == 31  # 1+10+20
    assert func(1, 2) == 23  # 1+2+20
    assert func(1, 2, 3) == 6  # 1+2+3


def test_default_parameter_must_come_last():
    """测试：有默认值的参数必须在无默认值的参数之后"""
    # 正确：无默认值的在前
    def correct(a, b=10):
        return a + b

    assert correct(5) == 15
    assert correct(5, 20) == 25


# ============================================================================
# 测试可变参数（*args 和 **kwargs）
# ============================================================================

def test_args_basic():
    """测试：*args 接收任意数量的位置参数"""
    def sum_all(*args):
        total = 0
        for num in args:
            total += num
        return total

    assert sum_all(1, 2, 3) == 6
    assert sum_all(1, 2, 3, 4, 5) == 15
    assert sum_all() == 0


def test_kwargs_basic():
    """测试：**kwargs 接收任意数量的关键字参数"""
    def print_info(**kwargs):
        result = []
        for key, value in kwargs.items():
            result.append(f"{key}={value}")
        return ", ".join(result)

    assert print_info(name="Alice", age=25) == "name=Alice, age=25"
    assert print_info(x=1, y=2, z=3) == "x=1, y=2, z=3"


def test_args_and_kwargs_together():
    """测试：*args 和 **kwargs 可以一起使用"""
    def func(*args, **kwargs):
        return (args, kwargs)

    result = func(1, 2, 3, name="Alice", age=25)
    assert result == ((1, 2, 3), {"name": "Alice", "age": 25})


# ============================================================================
# 测试函数的参数解包
# ============================================================================

def test_unpacking_list():
    """测试：列表解包作为参数"""
    def add(a, b, c):
        return a + b + c

    numbers = [1, 2, 3]
    assert add(*numbers) == 6


def test_unpacking_dict():
    """测试：字典解包作为关键字参数"""
    def greet(name, age):
        return f"{name} is {age} years old"

    info = {"name": "Alice", "age": 25}
    assert greet(**info) == "Alice is 25 years old"


# ============================================================================
# 测试函数的内存和身份
# ============================================================================

def test_function_is_object():
    """测试：函数是对象"""
    def my_func():
        return 42

    # 函数有类型
    assert type(my_func).__name__ == "function"

    # 函数有身份
    assert id(my_func) == id(my_func)

    # 函数可以赋值给变量
    another_name = my_func
    assert another_name() == 42


def test_function_can_have_attributes():
    """测试：函数可以有自己的属性"""
    def my_func():
        return 42

    # 动态添加属性
    my_func.custom_attribute = "custom value"

    assert my_func.custom_attribute == "custom value"


# ============================================================================
# 测试函数的比较
# ============================================================================

def test_function_equality():
    """测试：函数的相等性比较"""
    def func1():
        return 42

    def func2():
        return 42

    # 不同函数对象不相等
    assert func1 is not func2

    # 但调用结果可能相等
    assert func1() == func2()


# ============================================================================
# 测试函数的字符串表示
# ============================================================================

def test_function_repr():
    """测试：函数的字符串表示"""
    def my_function():
        pass

    # 函数的 __repr__ 包含函数名和内存地址
    repr_str = repr(my_function)
    assert "my_function" in repr_str


# ============================================================================
# 测试函数的可调用性
# ============================================================================

def test_callable():
    """测试：callable() 函数检查对象是否可调用"""
    def my_func():
        return 42

    assert callable(my_func) is True

    not_callable = 42
    assert callable(not_callable) is False

    # 类也是可调用的（调用构造函数）
    assert callable(list) is True

# ---------------------------------------------------------------------------
# Anchor contract aliases — keep ANCHORS.yml executable and stable.
# ---------------------------------------------------------------------------

def test_function_definition():
    def greet(name):
        return f"你好，{name}"

    assert greet("小北") == "你好，小北"


def test_parameters():
    def multiply(a, b):
        return a * b

    assert multiply(3, 4) == 12
    assert multiply(5, 6) == 30


def test_return_values():
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5
    assert result * 2 == 10


def test_scope():
    global_name = "outside"

    def make_local_name():
        local_name = "inside"
        return global_name, local_name

    assert make_local_name() == ("outside", "inside")
    assert "local_name" not in globals()


def test_print_vs_return():
    def add_with_print(a, b):
        print(a + b)

    def add_with_return(a, b):
        return a + b

    assert add_with_print(1, 2) is None
    assert add_with_return(1, 2) == 3


def test_call_without_definition():
    calls = []

    def record_call():
        calls.append("called")

    assert calls == []
    record_call()
    assert calls == ["called"]


def test_avoid_globals():
    total = 10

    def add_bonus(value, bonus):
        return value + bonus

    assert add_bonus(total, 5) == 15
    assert total == 10
