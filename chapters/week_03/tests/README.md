# Week 03 测试套件

## 概述

本测试套件为 Week 03（函数）提供全面的测试覆盖，包括：
- 函数定义和调用
- 参数传递
- 返回值
- 作用域
- 单位换算器功能
- PyHelper 函数

## 测试文件

### test_smoke.py
**基线测试** - 验证 Python 基础功能正常工作

覆盖内容：
- 函数定义和调用
- 参数传递
- 返回值机制
- 作用域规则
- 基本数学运算

**运行命令：**
```bash
python3 -m pytest chapters/week_03/tests/test_smoke.py -v
```

### test_functions.py
**函数核心功能测试** - 全面测试函数的定义、参数和返回值

覆盖内容：
- 函数定义（def 语句）
- 单参数和多参数
- return vs print
- 返回值类型
- 函数组合
- 默认参数
- 可变参数（*args, **kwargs）
- 递归函数
- 闭包
- lambda 函数

**运行命令：**
```bash
python3 -m pytest chapters/week_03/tests/test_functions.py -v
```

### test_converter.py
**单位换算器测试** - 测试贯穿案例：单位换算器

覆盖内容：
- 长度换算（公里 ↔ 英里）
- 重量换算（公斤 ↔ 磅）
- 温度换算（摄氏度 ↔ 华氏度）
- 边界情况（0、负数、极大/极小值）
- 往返转换精度
- 换算常量验证

**运行命令：**
```bash
python3 -m pytest chapters/week_03/tests/test_converter.py -v
```

### test_pyhelper.py
**PyHelper 测试** - 测试 PyHelper 的函数重构版本

覆盖内容：
- 欢迎信息
- 菜单显示
- 选择验证
- 心情推荐
- 名言返回
- 函数模块化设计
- 扩展性测试

**运行命令：**
```bash
python3 -m pytest chapters/week_03/tests/test_pyhelper.py -v
```

## 快速开始

### 运行所有测试
```bash
python3 -m pytest chapters/week_03/tests -q
```

### 运行特定测试文件
```bash
python3 -m pytest chapters/week_03/tests/test_functions.py -v
```

### 运行特定测试用例
```bash
python3 -m pytest chapters/week_03/tests/test_functions.py::test_function_definition_basic -v
```

### 运行带参数标记的测试
```bash
python3 -m pytest chapters/week_03/tests/test_converter.py -k "parameterized" -v
```

## 测试统计

| 测试文件 | 测试用例数 | 覆盖主题 |
|---------|----------|---------|
| test_smoke.py | 25 | 基础功能 |
| test_assignment_contract.py | 2 | 作业入口契约 |
| test_functions.py | 65 | 函数核心概念 |
| test_converter.py | 79 | 单位换算 |
| test_pyhelper.py | 54 | PyHelper 功能 |
| **总计** | **225** | **Week 03 全部内容** |

## 测试覆盖的核心概念

### 1. 函数定义
- ✅ def 语句语法
- ✅ 函数命名规范
- ✅ 文档字符串
- ✅ 函数对象

### 2. 参数
- ✅ 单参数
- ✅ 多参数
- ✅ 位置参数
- ✅ 关键字参数
- ✅ 默认参数
- ✅ 可变参数
- ✅ 参数解包

### 3. 返回值
- ✅ return 语句
- ✅ 返回不同类型
- ✅ 返回多个值
- ✅ return vs print
- ✅ 提前返回

### 4. 作用域
- ✅ 局部变量
- ✅ 全局变量
- ✅ 变量遮蔽
- ✅ 参数作用域

### 5. 单位换算
- ✅ 长度换算公式
- ✅ 重量换算公式
- ✅ 温度换算公式
- ✅ 边界值处理
- ✅ 精度验证

### 6. 函数设计
- ✅ 单一职责
- ✅ 函数组合
- ✅ 可复用性
- ✅ 模块化设计
- ✅ 扩展性

## 使用 conftest.py 中的 fixtures

测试套件提供了多个可复用的 fixtures：

```python
def test_example(km_to_miles_func):
    """使用 fixture 提供的函数"""
    result = km_to_miles_func(10)
    assert result == 6.21371
```

可用的 fixtures：
- `km_to_miles_func` - 公里转英里函数
- `kg_to_pounds_func` - 公斤转磅函数
- `celsius_to_fahrenheit_func` - 摄氏度转华氏度函数
- `get_advice_func` - 获取建议函数
- `get_quote_func` - 获取名言函数
- `valid_moods` - 有效心情选项
- `sample_km_values` - 示例公里值
- `boundary_values` - 边界值测试数据

## 测试最佳实践

### 1. 测试命名
使用描述性的测试名称：
```python
def test_km_to_miles_zero():  # 好
def test_conversion_1():       # 不好
```

### 2. 测试结构
使用 AAA 模式（Arrange-Act-Assert）：
```python
def test_km_to_miles_basic():
    # Arrange（准备）
    km = 10

    # Act（执行）
    result = km_to_miles(km)

    # Assert（断言）
    assert result == 6.21371
```

### 3. 参数化测试
使用 `@pytest.mark.parametrize` 减少重复：
```python
@pytest.mark.parametrize("km, expected", [
    (0, 0),
    (1, 0.621371),
    (10, 6.21371),
])
def test_km_to_miles(km, expected):
    assert km_to_miles(km) == expected
```

## 故障排除

### 测试失败时查看详细信息
```bash
python3 -m pytest chapters/week_03/tests -v --tb=long
```

### 只运行失败的测试
```bash
python3 -m pytest chapters/week_03/tests --lf
```

### 运行测试并在第一个失败时停止
```bash
python3 -m pytest chapters/week_03/tests -x
```

### 显示测试的打印输出
```bash
python3 -m pytest chapters/week_03/tests -s
```

## 贡献指南

添加新测试时，请确保：
1. 测试名称清晰描述测试内容
2. 测试独立（不依赖其他测试）
3. 测试遵循 AAA 模式
4. 添加适当的文档字符串
5. 考虑添加参数化测试来覆盖多个场景

## 许可证

本测试套件是《Python 程序设计（Agentic Coding）》教材的一部分。
