# Week 03 测试快速开始指南

## 为什么要运行测试？

测试可以帮助你：
- ✅ 验证你的代码是否正确
- ✅ 发现潜在的问题
- ✅ 学习函数的正确用法
- ✅ 养成良好的编程习惯

## 快速开始

### 1. 确保已安装 pytest

```bash
# 检查是否已安装
python3 -m pytest --version

# 如果未安装，运行：
pip3 install pytest
```

### 2. 运行所有测试

```bash
# 在项目根目录运行
python3 -m pytest chapters/week_03/tests -q
```

你应该看到类似输出：
```
........................................................................ [ 33%]
........................................................................ [ 66%]
.......................................................................  [100%]
225 passed
```

### 3. 查看详细输出

```bash
# 显示每个测试的名称
python3 -m pytest chapters/week_03/tests -v

# 显示更详细的输出
python3 -m pytest chapters/week_03/tests -vv
```

## 运行特定测试

### 运行单个测试文件

```bash
# 只运行函数测试
python3 -m pytest chapters/week_03/tests/test_functions.py -v

# 只运行换算器测试
python3 -m pytest chapters/week_03/tests/test_converter.py -v

# 只运行 PyHelper 测试
python3 -m pytest chapters/week_03/tests/test_pyhelper.py -v
```

### 运行特定测试用例

```bash
# 运行特定的测试
python3 -m pytest chapters/week_03/tests/test_functions.py::test_function_definition_basic -v

# 运行所有包含 "parameterized" 的测试
python3 -m pytest chapters/week_03/tests -k "parameterized" -v
```

## 理解测试输出

### 测试通过

```
test_km_to_miles_basic PASSED
```
✅ 你的代码正确实现了功能

### 测试失败

```
test_km_to_miles_basic FAILED

>       assert result == 6.21371
E       assert 6.2 == 6.21371
E        +  where 6.2 = km_to_miles(10)
```
❌ 你的代码有问题，检查：
1. 换算公式是否正确
2. 是否使用了正确的常量
3. 精度是否足够

### 测试错误

```
test_km_to_miles_basic ERROR

E       NameError: name 'km_to_miles' is not defined
```
❌ 代码有语法错误或未定义函数

## 测试文件说明

### test_smoke.py
**基线测试** - 确保 Python 基础功能正常

适合：
- 第一次运行测试
- 检查环境配置
- 验证基本理解

### test_functions.py
**函数核心测试** - 测试函数的所有概念

适合：
- 学习函数定义
- 理解参数和返回值
- 掌握作用域

### test_converter.py
**单位换算器测试** - 测试贯穿案例

适合：
- 练习单位换算
- 理解实际应用
- 验证边界情况

### test_pyhelper.py
**PyHelper 测试** - 测试重构后的代码

适合：
- 学习函数分解
- 理解模块化设计
- 实践菜单系统

## 常用测试命令

### 基础命令
```bash
# 运行所有测试（简洁输出）
python3 -m pytest chapters/week_03/tests -q

# 运行所有测试（详细输出）
python3 -m pytest chapters/week_03/tests -v

# 只运行失败的测试
python3 -m pytest chapters/week_03/tests --lf

# 遇到第一个失败就停止
python3 -m pytest chapters/week_03/tests -x
```

### 调试命令
```bash
# 显示详细错误信息
python3 -m pytest chapters/week_03/tests --tb=long

# 显示更少的错误信息
python3 -m pytest chapters/week_03/tests --tb=line

# 显示测试的打印输出
python3 -m pytest chapters/week_03/tests -s
```

### 统计命令
```bash
# 显示测试覆盖率（需要安装 pytest-cov）
python3 -m pytest chapters/week_03/tests --cov=.

# 显示最慢的 10 个测试
python3 -m pytest chapters/week_03/tests --durations=10
```

## 学习路径

### 第一步：运行基线测试
```bash
python3 -m pytest chapters/week_03/tests/test_smoke.py -v
```
确保环境正常，理解基本概念。

### 第二步：学习函数测试
```bash
python3 -m pytest chapters/week_03/tests/test_functions.py::test_function_definition_basic -v
```
逐个运行测试，理解每个概念。

### 第三步：练习单位换算
```bash
python3 -m pytest chapters/week_03/tests/test_converter.py -k "km_to_miles" -v
```
实现自己的换算函数，通过测试验证。

### 第四步：重构 PyHelper
```bash
python3 -m pytest chapters/week_03/tests/test_pyhelper.py -v
```
将 PyHelper 重构为函数版本，确保所有测试通过。

## 示例：从测试中学习

### 1. 查看测试代码

打开 `test_functions.py`，查看测试示例：

```python
def test_function_definition_basic():
    """测试：基本函数定义"""
    def say_hello():
        return "Hello"

    assert say_hello() == "Hello"
```

### 2. 理解测试期望

测试告诉你：
- 需要定义一个函数
- 函数应该返回什么
- 如何调用函数

### 3. 实现自己的代码

根据测试，实现类似的代码：

```python
def my_greeting():
    return "Hello, World!"
```

### 4. 验证你的实现

```bash
python3 -m pytest -k "my_greeting" -v
```

## 故障排除

### 问题：找不到 pytest

**解决方案：**
```bash
pip3 install pytest
```

### 问题：导入错误

**解决方案：**
确保在项目根目录运行测试：
```bash
cd /Users/wangxq/Documents/python-agentic-textbook
python3 -m pytest chapters/week_03/tests -q
```

### 问题：测试全部失败

**解决方案：**
1. 检查 Python 版本（需要 3.6+）
2. 重新安装 pytest
3. 检查测试文件路径是否正确

### 问题：某些测试失败

**解决方案：**
1. 查看失败的测试名称
2. 阅读测试代码，理解期望
3. 检查你的实现
4. 使用 `-v` 和 `--tb=long` 查看详细错误

## 下一步

### 完成作业
1. 实现 `starter_code/solution.py`
2. 运行测试验证
3. 修复失败的测试
4. 提交代码

### 深入学习
1. 阅读 `README.md` 了解测试结构
2. 查看 `TEST_SUMMARY.md` 了解测试覆盖
3. 研究 `conftest.py` 学习 fixtures
4. 尝试编写自己的测试

## 需要帮助？

- 查看测试代码中的注释
- 阅读 CHAPTER.md 相关章节
- 查看 ASSIGNMENT.md 了解作业要求
- 运行 `pytest --help` 查看所有选项

## 记住

- ✅ 测试是学习的工具，不是障碍
- ✅ 失败的测试指出需要改进的地方
- ✅ 从简单测试开始，逐步进阶
- ✅ 理解测试比通过测试更重要

祝你学习愉快！
