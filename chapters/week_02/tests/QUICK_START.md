# Week 02 测试快速参考

## 快速运行

### 运行所有测试
```bash
python3 -m pytest chapters/week_02/tests -q
```

### 运行特定测试文件
```bash
# 基线测试（验证环境）
python3 -m pytest chapters/week_02/tests/test_smoke.py -v

# 条件判断测试
python3 -m pytest chapters/week_02/tests/test_conditionals.py -v

# 循环测试
python3 -m pytest chapters/week_02/tests/test_loops.py -v

# 布尔表达式测试
python3 -m pytest chapters/week_02/tests/test_booleans.py -v
```

### 按关键词运行测试
```bash
# 所有边界测试
python3 -m pytest chapters/week_02/tests -k "boundary" -v

# 所有参数化测试
python3 -m pytest chapters/week_02/tests -k "parametrize" -v

# 所有猜数字相关测试
python3 -m pytest chapters/week_02/tests -k "guess" -v

# 所有难度相关测试
python3 -m pytest chapters/week_02/tests -k "difficulty" -v
```

### 运行单个测试
```bash
# 完整路径
python3 -m pytest chapters/week_02/tests/test_conditionals.py::test_score_grade_excellent -v

# 使用关键词（更方便）
python3 -m pytest chapters/week_02/tests -k "test_score_grade_excellent" -v
```

## 测试输出说明

### 安静模式（-q）
```bash
$ python3 -m pytest chapters/week_02/tests -q
153 passed
```
- 只显示进度条和总结
- 适合快速验证

### 详细模式（-v）
```bash
$ python3 -m pytest chapters/week_02/tests/test_smoke.py -v
test_smoke.py::test_basic_if_statement PASSED     [  8%]
test_smoke.py::test_basic_for_loop PASSED         [ 16%]
...
```
- 显示每个测试的名称和状态
- 适合定位具体失败的测试

### 超详细模式（-vv）
```bash
$ python3 -m pytest chapters/week_02/tests -vv
```
- 显示最详细的输出
- 包括每个断言的详细信息

### 显示 print 输出（-s）
```bash
$ python3 -m pytest chapters/week_02/tests -v -s
```
- 显示测试中的 print 语句
- 适合调试

### 只显示失败的测试
```bash
$ python3 -m pytest chapters/week_02/tests -x
```
- `-x`：第一个失败就停止
- 适合快速定位第一个错误

## 常见问题

### Q: 测试失败怎么办？
1. 查看失败的测试名称，了解是哪个功能出错
2. 使用 `-v` 查看详细错误信息
3. 使用 `-s` 查看 print 输出（如果测试中有）
4. 阅读测试代码，理解预期行为

### Q: 如何只运行一个测试？
```bash
# 方法 1：完整路径
python3 -m pytest chapters/week_02/tests/test_conditionals.py::test_score_grade_excellent -v

# 方法 2：使用 -k 关键词（更方便）
python3 -m pytest chapters/week_02/tests -k "test_score_grade_excellent" -v
```

### Q: 如何查看测试覆盖了什么？
阅读测试文件中的注释和文档字符串：
- `test_smoke.py`：基础功能验证
- `test_conditionals.py`：条件判断逻辑
- `test_loops.py`：循环和 range()
- `test_booleans.py`：布尔表达式和逻辑运算

### Q: 测试会修改我的代码吗？
不会。测试只运行断言，不会修改任何源代码文件。

### Q: 为什么有 153 个测试？
这是为了全面覆盖 Week 02 的所有知识点：
- 条件判断的各种情况
- 循环的各种模式
- 布尔表达式的各种组合
- 边界值和异常情况

## 测试统计

| 文件 | 测试数量 | 覆盖内容 |
|------|---------|---------|
| test_smoke.py | 12 | 基础功能验证 |
| test_assignment_contract.py | 2 | 作业入口契约 |
| test_conditionals.py | 37 | if/elif/else 逻辑 |
| test_loops.py | 38 | for/while 循环 |
| test_booleans.py | 64 | 布尔表达式 |
| **总计** | **153** | **Week 02 全部内容** |

## 下一步

1. 运行所有测试，确保环境正常：`python3 -m pytest chapters/week_02/tests -q`
2. 阅读 README.md 了解测试设计
3. 阅读 TEST_SUMMARY.md 查看详细覆盖情况
4. 开始完成 Week 02 的作业，用测试验证你的代码
