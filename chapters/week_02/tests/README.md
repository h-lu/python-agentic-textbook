# Week 02 测试套件

本目录包含 Week 02（让程序做选择）的完整测试套件，覆盖条件判断、循环和布尔表达式。

## 测试文件说明

### test_smoke.py
**基线测试** - 验证 Python 基础功能是否正常工作。

覆盖内容：
- 基本的 if/else 判断
- 基本的 for/while 循环
- 基本的布尔运算（and/or/not）
- 基本的比较运算符
- range() 函数
- break/continue 语句

**用途**：如果这些测试失败，说明 Python 环境有问题，其他测试也无法通过。

### test_conditionals.py
**条件判断测试** - 专门测试 if/elif/else 逻辑。

覆盖内容：
- 单分支 if 语句
- 多分支 if/elif/else 语句
- 条件判断的顺序性（从上到下检查）
- 猜数字游戏的判断逻辑
- 难度选择逻辑
- 嵌套条件
- PyHelper 心情推荐逻辑
- 边界值测试（0、负数、极大值）

**测试数量**：30+ 个测试用例

### test_loops.py
**循环测试** - 专门测试 for/while 循环和 range()。

覆盖内容：
- range() 函数的各种模式（起点、终点、步长）
- for 循环（求和、计数、break、continue）
- while 循环（倒计时、条件控制）
- for...else 结构（正常结束 vs break 退出）
- 猜数字游戏的循环逻辑
- 嵌套循环
- 循环边界情况（零次迭代、单次迭代）
- 实际应用（阶乘、FizzBuzz）

**测试数量**：35+ 个测试用例

### test_booleans.py
**布尔表达式测试** - 专门测试比较运算符和逻辑运算符。

覆盖内容：
- 比较运算符（==, !=, <, >, <=, >=）
- 逻辑运算符（and, or, not）
- 短路求值（short-circuit evaluation）
- 复杂布尔表达式的组合
- in 和 not in 运算符
- 布尔表达式简化（可读性优化）
- 德摩根定律
- 真值判断（Truthy/Falsy）
- 实际应用场景（输入验证、密码强度、游戏条件）

**测试数量**：40+ 个测试用例

## 运行测试

### 运行所有测试
```bash
python3 -m pytest chapters/week_02/tests -v
```

### 运行单个测试文件
```bash
# 只运行基线测试
python3 -m pytest chapters/week_02/tests/test_smoke.py -v

# 只运行条件判断测试
python3 -m pytest chapters/week_02/tests/test_conditionals.py -v

# 只运行循环测试
python3 -m pytest chapters/week_02/tests/test_loops.py -v

# 只运行布尔表达式测试
python3 -m pytest chapters/week_02/tests/test_booleans.py -v
```

### 运行特定测试
```bash
# 运行单个测试函数
python3 -m pytest chapters/week_02/tests/test_conditionals.py::test_score_grade_excellent -v

# 运行包含某个关键词的所有测试
python3 -m pytest chapters/week_02/tests -k "boundary" -v
```

### 查看详细输出
```bash
# 显示 print 语句的输出
python3 -m pytest chapters/week_02/tests -v -s

# 显示更短的输出（只显示失败的测试）
python3 -m pytest chapters/week_02/tests -q

# 显示最详细的输出（包括每个断言）
python3 -m pytest chapters/week_02/tests -vv
```

### 运行标记的测试
```bash
# 运行所有参数化测试
python3 -m pytest chapters/week_02/tests -m parametrize -v
```

## 测试覆盖的知识点

### 条件判断（if/elif/else）
- ✅ 单分支判断
- ✅ 多分支判断
- ✅ 条件的顺序性
- ✅ 嵌套条件
- ✅ 边界值测试
- ✅ 默认值处理

### 循环（for/while）
- ✅ for 循环配合 range()
- ✅ while 循环的条件控制
- ✅ break 跳出循环
- ✅ continue 跳过迭代
- ✅ for...else 结构
- ✅ 嵌套循环
- ✅ 循环边界情况
- ✅ 无限循环的避免

### 布尔表达式
- ✅ 比较运算符（==, !=, <, >, <=, >=）
- ✅ 逻辑运算符（and, or, not）
- ✅ 短路求值
- ✅ 复杂表达式组合
- ✅ in 和 not in
- ✅ 真值判断
- ✅ 运算符优先级

## 测试设计原则

1. **正例（Happy Path）**：正常输入应该通过
2. **边界（Boundary Cases）**：边界值测试（如 18 岁、60 分、0 次）
3. **反例（Edge Cases）**：错误输入应该被正确处理
4. **参数化测试**：使用 `@pytest.mark.parametrize` 减少重复代码
5. **清晰的命名**：测试失败时能直接看出哪里坏了

## 预期结果

所有测试应该 **100% 通过**。如果某个测试失败：

1. 检查是否是测试本身写错了
2. 检查是否是对 Python 语法理解有误
3. 如果是 solution.py 没实现，在测试文件中加注释说明预期行为

## 测试统计

- **总测试文件数**：5 个（含作业契约测试）
- **总测试用例数**：153 个
- **代码行数**：约 1500 行
- **覆盖率**：Week 02 所有核心知识点

## 扩展阅读

- pytest 官方文档：https://docs.pytest.org/
- 参数化测试：https://docs.pytest.org/en/stable/parametrize.html
- 断言重写：https://docs.pytest.org/en/stable/assert.html
