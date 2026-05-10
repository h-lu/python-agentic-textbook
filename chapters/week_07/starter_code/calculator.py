"""Week 07 练习 3：可导入也可直接运行的计算器模块。"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return None
    return a / b


if __name__ == "__main__":
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(4, 5) == 20
    assert divide(8, 2) == 4
    assert divide(5, 0) is None
    print("所有测试通过！")
