# Week 06 作业：异常处理与防御性编程

**截止时间**：Week 07 上课前
**预计用时**：基础 30-45 分钟 | 进阶 45-60 分钟 | 挑战 60-90 分钟
**提交方式**：在 `chapters/week_06/starter_code/solution.py` 中完成实现，跑通 `pytest` 后发起 PR

---

## 作业概述

这周的作业围绕一个核心目标：**让程序"不崩"**。你会从修复一个"会崩溃的除法器"开始，逐步学会用 `try/except` 捕获异常、用 `raise` 抛出异常、用 LBYL/EAFP 两种风格处理不同场景。

最终，你会给 PyHelper 添加异常处理——让它"不怕坏输入"。

**本周核心技能**：
- 用 `try/except` 捕获特定异常（不是裸的 `except:`）
- 用 `raise` 主动抛出异常，设计友好的错误消息
- 理解 LBYL vs EAFP，知道什么时候用哪种
- 设计"输入校验"函数，防止程序崩溃

---

## 基础作业（40 分）

**目标**：巩固 `try/except` 的基本用法，能捕获常见异常并给出友好的错误消息。

### 题 1：修复崩溃的除法器（10 分）

小北写了一个除法器，但一遇到坏输入就崩：

```python
# 这段代码会崩溃
numerator = int(input("请输入分子："))
denominator = int(input("请输入分母："))
result = numerator / denominator
print(f"结果：{result}")
```

**你的任务**：用 `try/except` 改进这段代码，让它能处理以下情况：
- 用户输入非数字（如 `"abc"`）
- 用户输入除以零（分母为 `0`）

**要求**：
1. 捕获特定异常（`ValueError` 和 `ZeroDivisionError`），不要用裸的 `except:`
2. 为每种异常给出**不同的错误提示**
3. 出错后程序不能崩溃，应该友好地提示用户

**输入/输出示例**：

```
请输入分子：10
请输入分母：0
错误：分母不能为零
```

```
请输入分子：abc
错误：请输入数字，不要输入文字
```

```
请输入分子：10
请输入分母：2
结果：5.0
```

**常见错误**：
- 用裸的 `except:` 捕获所有异常（-5 分）
- 没有区分不同异常类型（-3 分）
- 错误消息不清晰（-2 分）

**提交**：在 `chapters/week_06/starter_code/solution.py` 中实现 `safe_divide()`；`chapters/week_06/tests/test_week06.py` 会测试这个函数。

---

### 题 2：访问字典不崩溃（10 分）

下面这段代码会在字典中找不到键时崩溃：

```python
# 这段代码会崩溃
scores = {"小北": 85, "阿码": 90, "老潘": 95}
name = input("请输入学生姓名：")
print(f"{name} 的分数：{scores[name]}")
```

**你的任务**：用 EAFP 风格（`try/except`）改进这段代码。

**要求**：
1. 捕获 `KeyError` 异常
2. 找不到学生时给出友好提示，而不是崩溃

**输入/输出示例**：

```
请输入学生姓名：小北
小北 的分数：85
```

```
请输入学生姓名：张三
错误：找不到这个学生
```

**常见错误**：
- 用 LBYL 风格（`if name in scores`）而不是 EAFP（不扣分，但这题要求练习 EAFP）
- 用裸的 `except:` 捕获所有异常（-5 分）

**提示**：EAFP 风格的核心是"先尝试，失败再处理"，不要提前检查。

**提交**：在 `chapters/week_06/starter_code/solution.py` 中实现 `get_dictionary_value(dictionary, key, default=None)`；`chapters/week_06/tests/test_week06.py` 会测试这个函数。

---

### 题 3：文件读取不崩溃（10 分）

下面这段代码会在文件不存在时崩溃：

```python
# 这段代码会崩溃
filename = input("请输入文件名：")
with open(filename, "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
```

**你的任务**：用 EAFP 风格改进这段代码。

**要求**：
1. 捕获 `FileNotFoundError` 异常
2. 文件不存在时给出友好提示

**输入/输出示例**：

```
请输入文件名：data.txt
<文件内容>
```

```
请输入文件名：不存在的文件.txt
错误：文件不存在
```

**思考题**（不测试）：如果用 LBYL 风格（先 `os.path.exists()` 检查）会有什么问题？（提示：竞态条件）

**提交**：在 `chapters/week_06/starter_code/solution.py` 中实现 `safe_read_file(filepath)` 和 `safe_write_file(filepath, content)`；`chapters/week_06/tests/test_week06.py` 会测试文件读写行为。

---

### 题 4：理解 else 和 finally（10 分）

**判断题**（在代码注释中写出答案）：

```python
# 问题 1：else 什么时候会执行？
try:
    result = 10 / 2
except ZeroDivisionError:
    print("除以零")
else:
    print("计算成功")

# else 会执行吗？答：


# 问题 2：finally 什么时候会执行？
try:
    result = 10 / 0
except ZeroDivisionError:
    print("除以零")
finally:
    print("finally 执行了")

# finally 会执行吗？答：


# 问题 3：如果 try 里 return，finally 还会执行吗？
def test():
    try:
        return "try 的返回值"
    finally:
        print("finally 执行了")

# 调用 test() 时，finally 会执行吗？答：
```

**要求**：在注释中写出答案（写"会"或"不会"）。

**提示**：`finally` 的特点是"**无论是否出错都执行**"。

---

## 进阶作业（30 分）

**目标**：综合应用 `try/except`、`raise`、输入校验，设计"不会崩"的程序。

### 题 5：设计输入校验函数（15 分）

**你的任务**：实现一个"获取正整数"的函数，要求：

1. 用 `while` 循环让用户**重试直到输入正确**
2. 用 LBYL 风格（先用 `if` 检查）验证输入
3. 输入不合法时给出**清晰的错误提示**

**函数签名**：

```python
def get_positive_integer(prompt: str) -> int:
    """
    获取一个正整数（会重试直到输入正确）

    Args:
        prompt: 提示信息（如 "请输入你的年龄："）

    Returns:
        用户输入的正整数
    """
    # 你的代码
```

**要求**：
- 输入非数字时提示："错误：请输入一个正整数"
- 输入 `<= 0` 时提示："错误：请输入大于 0 的整数"
- 输入正确时返回整数

**输入/输出示例**：

```
请输入购买数量：abc
错误：请输入一个正整数
请输入购买数量：-5
错误：请输入大于 0 的整数
请输入购买数量：10
购买数量：10
```

**常见错误**：
- 用 `try/except` 而不是 LBYL（不扣分，但本题要求练习 LBYL）
- 忘记 `return` 导致无限循环（-5 分）
- 错误消息不清晰（-3 分）

**提示**：用 `str.isdigit()` 检查字符串是否为数字。

**提交**：在 `chapters/week_06/starter_code/solution.py` 中实现 `get_positive_integer(prompt)`。自动测试还会覆盖同文件中的 `is_positive_integer()` 和 `get_positive_integer_with_retry()`。

---

### 题 6：用 raise 上报错误（15 分）

**你的任务**：实现一个"获取年龄"的函数，要求：

1. 调用题 5 的 `get_positive_integer` 获取整数
2. **额外校验**年龄是否在 18-120 之间
3. 如果不满足，用 `raise ValueError` 抛出异常（不是 `print`）

**函数签名**：

```python
def get_age(min_age: int = 18, max_age: int = 120) -> int:
    """
    获取年龄（在指定范围内，不在范围会抛出 ValueError）

    Args:
        min_age: 最小年龄（默认 18）
        max_age: 最大年龄（默认 120）

    Returns:
        用户输入的年龄

    Raises:
        ValueError: 年龄不在 [min_age, max_age] 范围内
    """
    # 你的代码
```

**要求**：
- 年龄 `< min_age` 时抛出：`ValueError(f"年龄必须大于等于 {min_age}")`
- 年龄 `> max_age` 时抛出：`ValueError(f"年龄超出合理范围（最大 {max_age}）")`
- 不要用 `print` 处理错误，用 `raise` 上报给调用者

**调用示例**：

```python
try:
    age = get_age(min_age=18, max_age=120)
    print(f"你的年龄：{age}")
except ValueError as e:
    print(f"输入错误：{e}")
```

**输入/输出示例**：

```
请输入你的年龄（18-120）：15
输入错误：年龄必须大于等于 18
```

```
请输入你的年龄（18-120）：150
输入错误：年龄超出合理范围（最大 120）
```

```
请输入你的年龄（18-120）：25
你的年龄：25
```

**常见错误**：
- 用 `print` 而不是 `raise`（-10 分，这是核心考点）
- 错误消息不清晰（-5 分）
- 忘记调用 `get_positive_integer`（-5 分）

**思考题**：为什么用 `raise` 而不是 `print`？（提示：调用者需要知道"成功还是失败"）

**提交**：在 `chapters/week_06/starter_code/solution.py` 中实现 `get_age(min_age=18, max_age=120)`。自动测试还会覆盖同文件中的 `validate_age()`、`InvalidInputError` 和 `OutOfRangeError`。

---

## 挑战作业（20 分）

**目标**：综合应用异常处理、输入校验、LBYL/EAFP，实现一个"健壮的用户输入处理器"。

### 题 7：带重试次数限制的输入函数（10 分）

**你的任务**：改进题 5 的 `get_positive_integer`，添加"最多重试 3 次"的功能。

**函数签名**：

```python
def get_positive_integer_with_retry(prompt: str, max_attempts: int = 3) -> int:
    """
    获取一个正整数（最多重试 max_attempts 次）

    Args:
        prompt: 提示信息
        max_attempts: 最大尝试次数（默认 3）

    Returns:
        用户输入的正整数

    Raises:
        ValueError: 重试次数用完仍输入错误
    """
    # 你的代码
```

**要求**：
1. 用 `for` 循环限制重试次数（不是 `while`）
2. 每次出错时提示"剩余尝试次数：X"
3. 重试次数用完后抛出 `ValueError`

**输入/输出示例**：

```
请输入购买数量：abc
错误：请输入一个正整数（剩余尝试次数：2）
请输入购买数量：-5
错误：请输入大于 0 的整数（剩余尝试次数：1）
请输入购买数量：xyz
错误：请输入一个正整数（剩余尝试次数：0）

Traceback (most recent call last):
  ...
ValueError: 输入错误次数过多，超过 3 次
```

**提示**：
- 用 `range(max_attempts)` 创建循环
- 用 `max_attempts - attempt - 1` 计算剩余次数

**提交**：在 `chapters/week_06/starter_code/solution.py` 中实现 `get_positive_integer_with_retry(prompt, max_attempts=3)`；`chapters/week_06/tests/test_week06.py` 会测试这个函数。

---

### 题 8：健壮的菜单选择（10 分）

**你的任务**：实现一个"菜单选择"函数，要求：

1. 用 EAFP 风格（`try/except`）捕获 `ValueError`
2. 验证输入是否在有效范围内
3. 用 `while` 循环重试直到输入正确

**函数签名**：

```python
def get_menu_choice(min_choice: int, max_choice: int) -> int:
    """
    获取菜单选择（会重试直到输入正确）

    Args:
        min_choice: 最小选项（如 1）
        max_choice: 最大选项（如 5）

    Returns:
        用户输入的选项
    """
    # 你的代码
```

**输入/输出示例**：

```
请输入选择（1-5）：abc
错误：请输入数字，不要输入文字
请输入选择（1-5）：0
错误：请输入 1 到 5 之间的数字
请输入选择（1-5）：6
错误：请输入 1 到 5 之间的数字
请输入选择（1-5）：3
你选择了：3
```

**要求**：
- 用 EAFP 风格（先尝试 `int()`，失败再捕获）
- 验证输入是否在 `[min_choice, max_choice]` 范围内
- 给出清晰的错误提示

**提交**：在 `chapters/week_06/starter_code/solution.py` 中实现 `get_menu_choice(min_choice, max_choice)`。自动测试当前覆盖同文件中的 `get_choice_with_retry(prompt, valid_choices, max_attempts=3)`。

---

## AI 协作练习（可选，10 分）

**本周主题**：审查 AI 生成的异常处理代码

根据 `ai_progression.md`，你现在处于**识别期**——目标是学会"审视 AI 代码"，找出其中的问题。

### 练习：找出 AI 代码中的问题

下面这段代码是某个 AI 工具生成的"安全除法器"。请审查它：

```python
# AI 生成的代码（故意包含 3-4 个问题）
def safe_divide_ai():
    """AI 生成的安全除法器"""
    try:
        numerator = int(input("请输入分子："))
        denominator = int(input("请输入分母："))
        result = numerator / denominator
        print(f"结果：{result}")
    except:
        print("出错了！")
```

**审查清单**（请逐项检查）：

- [ ] **代码能运行吗？** 测试各种输入（正常数字、除以零、非数字）
- [ ] **异常处理正确吗？** 是否用裸的 `except:` 捕获所有异常？
- [ ] **错误消息清晰吗？** 用户能知道"为什么出错"吗？
- [ ] **边界情况处理了吗？** （分子为 0、负数、浮点数等）
- [ ] **你能写一个让它失败的测试吗？** 设计一个输入，让代码暴露问题

**你的修复**：

在 `chapters/week_06/ai_review.md` 中提交：
1. **问题报告**：列出你发现的至少 3 个问题
2. **修复后的代码**：修复这些问题后的代码
3. **测试用例**：至少 3 个测试用例，证明修复有效

**示例问题报告**（格式参考）：

```markdown
## 发现的问题

1. **用裸的 `except:` 捕获所有异常**
   - 为什么不好：会掩盖真正的 bug，用户不知道"为什么出错"
   - 如何修复：捕获特定异常（`ValueError` 和 `ZeroDivisionError`）

2. **错误消息不清晰**
   - 为什么不好："出错了！"没有告诉用户原因
   - 如何修复：为每种异常给出不同的错误提示

3. **缺少输入验证**
   - 为什么不好：没有提示用户重试
   - 如何修复：添加 while 循环重试
```

**评分标准**：
- 发现至少 3 个问题：5 分
- 修复后的代码能通过测试：3 分
- 测试用例设计合理：2 分

**提示**：参考本周正文中的"AI 时代小专栏"。

---

## PyHelper 实践（必做，计入进阶作业）

**你的任务**：给上周的 PyHelper 添加异常处理，让它"不怕坏输入"。

### 具体要求

1. **菜单选择不崩溃**（10 分）
   - 实现 `get_choice(min_choice, max_choice)` 函数
   - 用 `try/except ValueError` 捕获非数字输入
   - 验证输入是否在有效范围内
   - 用 `while` 循环重试直到输入正确

2. **日期输入不崩溃**（10 分）
   - 实现 `get_date()` 函数
   - 校验日期格式（必须是 `MM-DD`）
   - 校验日期是否为数字
   - 用 `while` 循环重试直到输入正确

3. **心情选择不崩溃**（10 分）
   - 改进 `get_mood()` 函数
   - 用 `try/except ValueError` 捕获非数字输入
   - 输入无效时给默认值（不是崩溃）

4. **文件操作不崩溃**（10 分）
   - 改进 `load_learning_log()` 函数
   - 用 `try/except` 捕获文件读取错误
   - 出错时给提示并创建新的数据文件

**提交**：修改后的 `chapters/week_06/examples/06_pyhelper.py`

**测试方法**：
1. 运行 PyHelper
2. 在菜单选择时输入 `"abc"`，应该提示"请输入数字"而不是崩溃
3. 在日期输入时输入 `"hello"`，应该提示"日期格式不对"而不是崩溃
4. 在心情选择时输入 `"xyz"`，应该给默认值而不是崩溃

**参考实现**：如果你遇到困难，可以参考 `starter_code/solution.py`（但不要直接复制粘贴，理解后自己写）

---

## 提交要求

### 必做

1. **基础作业**（40 分）：题 1-4
2. **进阶作业**（30 分）：题 5-6
3. **PyHelper 实践**（必做，计入进阶作业）：改进 PyHelper 的异常处理

### 可选

4. **挑战作业**（20 分）：题 7-8
5. **AI 协作练习**（10 分）：审查 AI 代码

### 提交检查

在发起 PR 前，请确认：

- [ ] 运行 `python3 -m pytest chapters/week_06/tests -q` 通过所有测试
- [ ] `chapters/week_06/starter_code/solution.py` 暴露 `safe_divide`、`get_dictionary_value`、`safe_read_file`、`get_positive_integer`、`get_age`、`get_positive_integer_with_retry`、`get_menu_choice` 等作业接口
- [ ] PyHelper 输入 `"abc"` 不会崩溃，会提示错误
- [ ] 除法器输入除以零不会崩溃，会提示错误
- [ ] 至少提交了 2 次 Git（draft + verify）
- [ ] PR 描述包含了自测结果

### PR 描述模板

```markdown
## Week 06 作业完成情况

### 完成的题目
- [x] 基础：题 1-4（修复除法器、字典访问、文件读取、理解 else/finally）
- [x] 进阶：题 5-6（输入校验函数、raise 上报错误）
- [x] PyHelper：添加异常处理（菜单选择、日期输入、文件操作）
- [ ] 挑战：题 7-8（重试次数限制、健壮菜单）
- [ ] AI 练习：审查 AI 生成的代码

### 自测结果
- 除法器测试：
  - 输入 "abc" → 提示 "请输入数字" ✅
  - 输入 "0" → 提示 "分母不能为零" ✅
  - 输入 "10/2" → 输出 "5.0" ✅
- PyHelper 测试：
  - 菜单输入 "abc" → 提示错误并重试 ✅
  - 日期输入 "hello" → 提示格式错误 ✅

### 遇到的问题
（记录你遇到的问题和解决方法）

### 待 review
请重点检查：
1. 异常处理是否完整（是否捕获了所有预期的异常）
2. 错误消息是否清晰
3. 是否有裸的 `except:` 不恰当地捕获所有异常
```

---

## 常见错误与调试技巧

### 错误 1：用裸的 `except:` 掩盖问题

**症状**：程序不崩溃，但不知道哪里出错了

**原因**：`except:` 捕获了所有异常，包括你没预料到的 bug

**解决**：捕获特定异常（`except ValueError:`）

---

### 错误 2：忘记 `raise` 上报错误

**症状**：输入校验失败后，程序继续执行

**原因**：用了 `print` 而不是 `raise`

**解决**：用 `raise ValueError("错误原因")` 上报给调用者

---

### 错误 3：`while` 循环没有 `return`

**症状**：输入正确后，函数继续循环

**原因**：忘记在成功时 `return`

**解决**：输入验证通过后，立即 `return` 结果

---

### 调试技巧

1. **打印异常信息**：用 `except Exception as e:` 然后 `print(f"错误：{e}")`
2. **故意触发错误**：测试各种边界输入（空字符串、负数、超大数）
3. **阅读 Traceback**：看清楚"错误类型"和"错误位置"

---

## 延伸阅读

- Python 官方文档：[Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- Real Python：[Exception Handling Best Practices](https://realpython.com/ref/best-practices/exception-handling/)
- PEP 8：[Programming Recommendations](https://peps.python.org/pep-0008/#programming-recommendations)

---

**祝你作业顺利！如果遇到困难，记住：防御性编程不是"防止用户犯错"，而是"假设用户一定会犯错"，然后让程序能容错。**
