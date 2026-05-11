# Week 07 作业：模块化重构

## 作业说明

本周你将学会把"一坨代码"拆成"模块化项目"。你将从使用 Python 标准库开始，逐步学会拆分自己的代码，最终把一个单文件项目重构成清晰的多模块结构。

**提交方式**：将代码提交到你的 Git 仓库，运行测试确保通过，完成 Pull Request。

**参考实现**：如果你遇到困难，可以参考 `starter_code/solution.py` 中的示例代码。

---

## 基础作业（必做）

### 练习 1：使用标准库模块

**目标**：学会使用 `import` 导入 Python 标准库模块。

在 `starter_code/` 下创建文件 `practice1_standard_library.py`，完成以下功能：

1. 使用 `import math` 导入 math 模块
2. 使用 `from random import choice, randint` 导入 random 模块的特定函数
3. 使用 `import datetime as dt` 给 datetime 模块起别名
4. 实现以下功能：
   - 计算圆的面积（用户输入半径，使用 `math.pi` 和 `math.pow`）
   - 随机抽奖（从一个列表中随机选择一个幸运儿）
   - 显示当前日期（使用 `dt.datetime.now()`）

**输入示例**：
```
请输入圆的半径：5
抽奖候选人名单（用逗号分隔）：小北,阿码,老潘,小红
```

**输出示例**：
```
圆的面积：78.53981633974483
幸运同学：阿码
当前日期：2026-02-09
```

**要求**：
- 使用三种不同的 import 语法
- 对用户输入进行基本的异常处理（如半径必须是数字）
- 代码要有清晰的注释

**常见错误**：
- 忘记导入模块就使用（`NameError`）
- 使用 `math.pi` 时不加 `math.` 前缀（除非用 `from math import pi`）
- 把 `import` 语句写在函数里面（应该放在文件顶部）

---

### 练习 2：拆分单文件项目

**目标**：学会按功能把单文件代码拆成多个模块。

有一个单文件项目 `todo_list.py`（已提供在 `starter_code/`），它把所有功能都写在一个文件里：
- 添加待办事项
- 查看所有待办
- 标记完成
- 保存到文件

你的任务是把这"一坨代码"拆成以下结构（放在 `starter_code/` 下）：

```
starter_code/todo_app/
├── main.py              # 主入口，菜单循环
├── storage.py           # 文件读写操作
├── todo_manager.py      # 待办事项的业务逻辑
└── input_handler.py     # 输入校验
```

**拆分指导**：

1. **storage.py** 应该包含：
   - `load_todos()` —— 从文件加载待办列表
   - `save_todos(todos)` —— 保存待办列表到文件
   - `get_data_file()` —— 返回数据文件的路径
   - 使用 `if __name__ == "__main__":` 添加测试代码

2. **todo_manager.py** 应该包含：
   - `add_todo(todos, title)` —— 添加待办
   - `complete_todo(todos, index)` —— 标记完成
   - `show_todos(todos)` —— 显示所有待办
   - 使用 `if __name__ == "__main__":` 添加测试代码

3. **input_handler.py** 应该包含：
   - `get_choice(min_val, max_val)` —— 获取用户选择
   - `get_todo_title()` —— 获取待办标题（非空校验）
   - 使用 `if __name__ == "__main__":` 添加测试代码

4. **main.py** 应该：
   - 导入上面三个模块
   - 实现菜单循环
   - 调用各模块的函数完成任务
   - 使用 `if __name__ == "__main__":` 启动程序

**验证方法**：
```bash
cd chapters/week_07/starter_code/todo_app

# 单独测试每个模块
python3 storage.py
python3 todo_manager.py
python3 input_handler.py

# 运行主程序
python3 main.py
```

**常见错误**：
- 导入时模块名写错（`import Storage` 而不是 `import storage`）
- 模块文件不在同一目录下导致 `ImportError`
- 把所有代码都放在 `if __name__ == "__main__":` 里面（导入的函数应该在外面）

---

### 练习 3：添加 __name__ 守卫

**目标**：理解并正确使用 `if __name__ == "__main__":` 守卫。

在 `starter_code/` 下创建一个模块 `calculator.py`，包含以下功能：

1. 四个运算函数：`add`, `subtract`, `multiply`, `divide`
2. 每个 `divide` 函数要处理除零错误（返回 `None`）
3. 添加 `if __name__ == "__main__":` 守卫，里面包含测试代码

**要求**：
- 函数定义必须在守卫外面
- 测试代码必须在守卫里面
- 测试代码要测试正常情况和边界情况（如除零）

**测试代码示例思路**（不要直接复制）：
```python
# 测试加法
assert add(2, 3) == 5
# 测试除零
assert divide(5, 0) is None
```

**验证**：
```bash
# 直接运行应该执行测试
python3 chapters/week_07/starter_code/calculator.py
# 应该输出：所有测试通过！

# 导入时不应该执行测试
PYTHONPATH=chapters/week_07/starter_code python3 -c "from calculator import add; print(add(2, 3))"
# 应该只输出：5（不输出测试信息）
```

**常见错误**：
- 把函数定义写在守卫里面（导致导入失败）
- 守卫拼写错误（`__name__` 写成 `__nama__`）
- 忘记写守卫（导入时会自动执行测试代码）

---

### 练习 4：创建包结构

**目标**：理解包（package）的概念，会创建简单的包结构。

创建一个包 `grades`，用于管理学生成绩：

```
grades/
├── __init__.py          # 包初始化文件
├── calculator.py        # 成绩计算（平均分、总分）
├── analyzer.py          # 成绩分析（最高、最低、及格率）
└── formatter.py         # 格式化输出（打印成绩单）
```

**要求**：

1. **`__init__.py`**：
   - 可以是空文件
   - 或者导出常用函数（可选）

2. **`calculator.py`**：
   - `calculate_average(scores)` —— 计算平均分
   - `calculate_total(scores)` —— 计算总分
   - 添加 `__name__` 守卫

3. **`analyzer.py`**：
   - `find_highest(scores)` —— 找最高分
   - `find_lowest(scores)` —— 找最低分
   - `calculate_pass_rate(scores, passing_score=60)` —— 计算及格率
   - 添加 `__name__` 守卫

4. **`formatter.py`**：
   - `print_report(name, scores)` —— 打印成绩单（美观格式）
   - 添加 `__name__` 守卫

5. 在包外创建 `test_grades.py` 测试你的包：
   ```python
   from grades import calculate_average, find_highest
   from grades.formatter import print_report

   scores = {"数学": 85, "英语": 92, "Python": 88}
   avg = calculate_average(scores.values())
   print(f"平均分：{avg}")
   print_report("小北", scores)
   ```

**验证**：
```bash
# 测试各个模块
python3 -m grades.calculator
python3 -m grades.analyzer
python3 -m grades.formatter

# 运行测试文件
python3 test_grades.py
```

**常见错误**：
- 忘记创建 `__init__.py`（Python 3.3+ 虽然支持命名空间包，但显式创建仍是最佳实践）
- 导入时路径错误（`from grades.calculator import ...` 而不是 `from calculator import ...`）
- 相对导入和绝对导入混用导致混乱

---

## 进阶作业（可选）

### 练习 5：重构自己的项目

**目标**：将你之前做过的某个单文件项目重构成多模块结构。

选择你之前完成的任意一个项目（如 Week 05 的日记本、Week 04 的成绩单），按照以下步骤重构：

**Step 1**：分析现有代码，列出所有函数及其职责

**Step 2**：按功能分组，设计模块结构
- 文件操作相关 → `storage.py`
- 输入校验相关 → `input_handler.py`
- 业务逻辑相关 → `business.py` 或 `core.py`
- 主入口 → `main.py`

**Step 3**：逐个创建模块，每个模块都要有：
- 清晰的职责（只做一类事情）
- `__name__` 守卫和测试代码
- 适当的注释

**Step 4**：创建 `main.py` 导入并调用各模块

**Step 5**：验证重构后的代码功能与原代码一致

**提交物**：
- 重构前的单文件（备份为 `project_original.py`）
- 重构后的多模块项目
- 一个 `REFACTORING.md` 文件，说明：
  - 你为什么要这样拆分
  - 拆分过程中遇到的困难
  - 重构前后的对比（代码行数、可读性变化）

**评分要点**：
- 模块职责是否清晰
- 是否正确使用 `import` 和 `__name__` 守卫
- 代码是否更容易理解和维护

---

### 练习 6：设计项目目录结构

**目标**：为一个假设的大型项目设计合理的目录结构。

假设你要开发一个"图书管理系统"（Library Management System），它有以下功能：
- 图书管理（添加、删除、搜索图书）
- 用户管理（注册、登录、权限）
- 借阅管理（借书、还书、续借）
- 数据持久化（保存到文件或数据库）
- 报表统计（借阅排行、逾期统计）

请设计一个项目目录结构，并解释每个目录/文件的用途。

**要求**：
- 遵循 Python 项目的最佳实践
- 代码、测试、数据、文档分离
- 考虑未来扩展性
- 提供一个 `README.md` 说明项目的结构和运行方法

**提示**：可以参考这样的结构：
```
library_system/
├── library/              # 包目录
│   ├── __init__.py
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑
│   ├── utils/            # 工具函数
│   └── cli/              # 命令行接口
├── tests/                # 测试
├── data/                 # 数据文件
├── docs/                 # 文档
├── README.md
└── requirements.txt
```

**提交物**：
- 完整的目录结构（树状图）
- 每个 module 的职责说明
- 一个简单的 `README.md`

---

## AI 协作练习（可选）

### 练习 7：审查 AI 生成的模块化代码

**背景**：你让某个 AI 工具帮你把一个单文件项目拆成多模块，它给出了下面的代码。

**任务**：审查这段代码，找出问题并修复。

#### AI 生成的代码

```python
# storage.py （AI 生成）

if __name__ == "__main__":
    def load_data(filename):
        """从文件加载数据"""
        try:
            with open(filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print("文件不存在")
            return None

    def save_data(filename, data):
        """保存数据到文件"""
        with open(filename, 'w') as f:
            f.write(data)

    # 测试代码
    data = load_data("test.txt")
    if data:
        print(f"加载了 {len(data)} 个字符")

# main.py （AI 生成）

from storage import load_data, save_data

def main():
    data = load_data("data.txt")
    if data:
        print(f"数据：{data}")
        save_data("backup.txt", data)

main()
```

#### 审查清单

请检查以下问题：

- [ ] **代码能运行吗？**
  - 提示：尝试导入 `storage` 模块，会发生什么？
  - 提示：函数定义的位置是否正确？

- [ ] **`__name__` 守卫使用正确吗？**
  - 提示：函数定义应该在守卫的里面还是外面？
  - 提示：测试代码应该在守卫的里面还是外面？

- [ ] **异常处理完整吗？**
  - 提示：`save_data` 如果文件写入失败会怎样？
  - 提示：`load_data` 返回 `None` 时，调用者有没有处理？

- [ ] **模块职责清晰吗？**
  - 提示：`main.py` 中直接调用 `main()` 有什么问题？
  - 提示：是否应该给 `main()` 也加上守卫？

- [ ] **你能写一个让它失败的测试吗？**
  - 提示：如果传入一个不存在的文件名？
  - 提示：如果磁盘已满无法写入？

#### 你的修复

请修复上述问题，提交：
1. 修复后的 `storage_fixed.py`
2. 修复后的 `main_fixed.py`
3. 一个简短的 `ai_review.md`，说明你发现了哪些问题

**提示**：
- 函数定义应该在守卫外面
- 只有测试代码应该在守卫里面
- `main.py` 的入口应该用 `if __name__ == "__main__":` 守卫
- 异常处理要考虑更多边界情况

---

## 验证与提交

### 自测清单

在提交前，请确认：

- [ ] 基础练习 1 完成：`practice1_standard_library.py` 能运行
- [ ] 基础练习 2 完成：todo_app 项目结构正确，各模块能独立测试
- [ ] 基础练习 3 完成：`calculator.py` 守卫正确，导入不执行测试
- [ ] 基础练习 4 完成：grades 包结构正确，能通过 `test_grades.py` 测试
- [ ] 运行 `python3 -m pytest chapters/week_07/tests -q` 通过所有测试
- [ ] 代码已提交到 Git，至少有 2 次提交（draft + verify）

### Git 提交规范

```bash
# 第一次提交（草稿）
git add chapters/week_07/practice*.py
git add chapters/week_07/starter_code/todo_app/
git commit -m "draft week_07: 完成基础练习 1-3"

# 第二次提交（验证）
git add chapters/week_07/grades/
git commit -m "verify week_07: 完成基础练习 4，所有测试通过"

# 推送到远端
git push origin week_07
```

### Pull Request 描述模板

```markdown
## Week 07 作业完成情况

### 已完成的练习
- [x] 练习 1：使用标准库模块
- [x] 练习 2：拆分单文件项目
- [x] 练习 3：添加 __name__ 守卫
- [x] 练习 4：创建包结构

### 进阶练习（可选）
- [ ] 练习 5：重构自己的项目
- [ ] 练习 6：设计项目目录结构

### AI 协作练习（可选）
- [ ] 练习 7：审查 AI 生成的代码

### 自测结果
- 运行 `python3 -m pytest chapters/week_07/tests -q`：通过 / 失败
- 单独测试各模块：通过 / 失败

### 遇到的困难
（记录你遇到的问题和解决方法）

### 请 Review 的重点
（特别希望 reviewer 关注的地方）
```

---

## 常见问题 FAQ

**Q1: 导入时提示 `ModuleNotFoundError` 怎么办？**

A: 检查以下几点：
1. 模块文件是否在当前目录下
2. 模块文件名是否拼写正确（区分大小写）
3. 是否在正确的目录下运行 Python

**Q2: `__name__` 守卫和普通的 `if` 语句有什么区别？**

A: `__name__` 是 Python 的特殊变量，它的值取决于模块是被直接运行还是被导入。直接运行时是 `"__main__"`，被导入时是模块名。这个守卫让模块既能当程序运行，也能被其他代码导入使用。

**Q3: 什么时候用相对导入（`from . import module`），什么时候用绝对导入（`from package import module`）？**

A:
- 在包内部导入同包的其他模块时，用相对导入（如 `from .storage import load`）
- 在包外部或导入其他包的模块时，用绝对导入（如 `from myapp.storage import load`）
- 相对导入只能在包内使用，不能在顶层脚本中使用

**Q4: 练习 2 中，我不知道该怎么拆分代码怎么办？**

A: 可以按照以下步骤：
1. 先列出所有函数
2. 按"功能相关性"分组（操作文件的放一起，处理输入的放一起）
3. 给每组起个名字（如 `storage.py`、`input_handler.py`）
4. 逐个创建模块，每创建一个就测试一个
5. 最后创建 `main.py` 把它们串起来

**Q5: `__init__.py` 必须写吗？Python 3.3+ 不是支持没有 `__init__.py` 的包吗？**

A: Python 3.3+ 确实支持"命名空间包"（namespace package），不需要 `__init__.py`。但显式创建 `__init__.py` 仍然是最佳实践，因为：
1. 明确标识"这是一个包"
2. 可以在 `__init__.py` 中写包的初始化代码
3. 兼容性更好（旧版本 Python 也支持）
4. 更符合 Python 社区的惯例

---

## 挑战自我

如果你想进一步挑战自己，可以尝试：

1. **循环导入问题**：创建两个模块 A 和 B，A 导入 B，B 导入 A，看看会发生什么？如何解决？
2. **动态导入**：使用 `importlib` 模块在运行时动态导入模块（如根据用户输入导入不同的模块）
3. **包的分发**：给你的包添加 `setup.py`，让它可以通过 `pip install` 安装
4. **探索标准库**：选择一个你从未用过的标准库模块（如 `collections`、`itertools`、`functools`），学习并使用它

---

祝你学习愉快！模块化是编程的重要技能，掌握后你会发现代码变得更优雅、更易维护。
