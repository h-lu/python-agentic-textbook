# Week 08 作业：测试与调试——让你的代码值得信赖

## 作业说明

本周你将学会用 pytest 给代码写自动化测试。从简单的 `assert` 断言开始，到使用 fixture 管理测试数据，再到参数化测试覆盖边界情况，最后体验完整的 TDD 开发流程。

**提交方式**：将代码提交到你的 Git 仓库，运行测试确保通过，完成 Pull Request。

**参考实现**：如果你遇到困难，可以参考 `starter_code/solution.py` 中的示例代码。

---

## 基础作业（必做）

### 练习 1：Todo Manager 测试补全

**目标**：学会编写基本的 pytest 测试用例，覆盖正常路径和边界情况。

`starter_code/todo_manager.py` 提供了一个待办事项管理器，包含以下功能：
- `add_task(tasks, task_name)` —— 添加任务
- `mark_done(tasks, index)` —— 标记任务完成
- `delete_task(tasks, index)` —— 删除任务
- `list_tasks(tasks)` —— 列出所有任务（打印）

你的任务是创建 `test_todo_manager.py`，为这个模块编写测试。

**要求**：

1. **至少 5 个测试函数**，覆盖以下场景：
   - 正常添加任务
   - 标记任务完成（正常路径）
   - 删除任务（正常路径）
   - 标记不存在的任务（边界情况，返回 False）
   - 删除不存在的任务（边界情况，返回 False）

2. **测试函数命名规范**：
   - 必须以 `test_` 开头
   - 函数名要能说明测试内容，如 `test_add_task_success`

3. **使用 `assert` 进行断言验证**：
   - 验证返回值是否符合预期
   - 验证任务列表的状态变化

**输入/输出示例**：

```python
# 测试 add_task 的正常路径
def test_add_task_success():
    tasks = []
    result = add_task(tasks, "买牛奶")

    assert len(result) == 1
    assert result[0]["name"] == "买牛奶"
    assert result[0]["done"] == False

# 测试 mark_done 的边界情况
def test_mark_done_invalid_index():
    tasks = [{"name": "买牛奶", "done": False}]
    result = mark_done(tasks, 99)  # 索引 99 不存在

    assert result == False
    assert tasks[0]["done"] == False  # 任务状态不应改变
```

**验证方法**：
```bash
pytest test_todo_manager.py -v
```

**常见错误**：
- 测试函数名不以 `test_` 开头，pytest 无法发现
- 忘记导入被测函数（`from todo_manager import add_task`）
- 断言条件写反了（如 `assert result == True` 但实际返回的是列表）
- 测试之间互相依赖（一个测试修改了全局数据，影响另一个测试）

---

### 练习 2：Fixture 练习

**目标**：学会使用 pytest fixture 管理测试数据准备。

**要求**：

1. 创建一个名为 `sample_tasks` 的 fixture，返回一个包含 3 个任务的列表：
   ```python
   [
       {"name": "买牛奶", "done": True},
       {"name": "写作业", "done": False},
       {"name": "运动", "done": False}
   ]
   ```

2. 创建至少 2 个测试函数，使用这个 fixture：
   - 一个测试 `mark_done` 功能
   - 一个测试 `delete_task` 功能

3. 再创建一个名为 `empty_tasks` 的 fixture，返回空列表，用于测试添加功能。

**使用 fixture 的示例**：

```python
import pytest
from todo_manager import mark_done, delete_task

@pytest.fixture
def sample_tasks():
    """提供包含 3 个任务的测试数据"""
    return [
        {"name": "买牛奶", "done": True},
        {"name": "写作业", "done": False},
        {"name": "运动", "done": False}
    ]

def test_mark_done_with_fixture(sample_tasks):
    """使用 fixture 测试标记完成"""
    result = mark_done(sample_tasks, 2)  # 标记第二个任务

    assert result == True
    assert sample_tasks[1]["done"] == True
```

**验证方法**：
```bash
pytest test_todo_manager.py -v
```

**常见错误**：
- fixture 函数没有加 `@pytest.fixture` 装饰器
- 忘记在测试函数的参数列表中写 fixture 名
- fixture 返回了可变对象，导致测试之间互相影响（每个测试应该使用独立的数据副本）

---

## 进阶作业（选做）

### 练习 3：参数化测试设计

**目标**：学会使用 `@pytest.mark.parametrize` 设计测试矩阵，覆盖多种输入情况。

**要求**：

1. 使用 `@pytest.mark.parametrize` 为 `add_task` 设计参数化测试，覆盖以下情况：
   - 正常任务名（如 "买牛奶"）
   - 带前后空格的任务名（如 "  买牛奶  "，测试是否能正确处理）
   - 带 emoji 的任务名（如 "🥛 买牛奶"）
   - 中英文混合（如 "完成 Python 作业"）

2. 使用 `@pytest.mark.parametrize` 为 `mark_done` 设计边界测试，覆盖以下索引：
   - 正常索引（1, 2, 3）
   - 边界索引（0，超出范围）
   - 负数索引（-1）

3. 运行测试时，你应该看到类似这样的输出：
   ```
   test_todo_manager.py::test_add_task_parametrized[买牛奶] PASSED
   test_todo_manager.py::test_add_task_parametrized[  买牛奶  ] PASSED
   test_todo_manager.py::test_add_task_parametrized[🥛 买牛奶] PASSED
   ```

**参数化测试示例**：

```python
@pytest.mark.parametrize("task_name", [
    "买牛奶",
    "  买牛奶  ",
    "🥛 买牛奶",
    "完成 Python 作业"
])
def test_add_task_parametrized(task_name):
    """测试各种任务名的处理"""
    tasks = []
    result = add_task(tasks, task_name)

    assert len(result) == 1
    # 注意：如果 add_task 内部做了 strip()，这里需要相应调整断言
```

**验证方法**：
```bash
pytest test_todo_manager.py -v
```

**常见错误**：
- 参数列表格式写错（应该用列表包含元组）
- 忘记在测试函数的参数列表中声明参数名
- 参数值和断言逻辑不匹配（如测试 strip() 但断言没考虑）

---

### 练习 4：TDD 实践

**目标**：体验完整的 TDD（测试驱动开发）循环：红-绿-重构。

**任务**：为 Todo Manager 添加一个新功能——**任务优先级**（priority）。

**TDD 流程**：

**Step 1：红（写测试，看到失败）**

在 `test_todo_manager.py` 中，先写测试（此时功能还不存在）：

```python
def test_add_task_with_priority():
    """测试添加带优先级的任务"""
    from todo_manager import add_task_with_priority

    tasks = []
    result = add_task_with_priority(tasks, "紧急任务", priority="high")

    assert len(result) == 1
    assert result[0]["name"] == "紧急任务"
    assert result[0]["priority"] == "high"
    assert result[0]["done"] == False
```

运行测试，确认它失败（红）。

**Step 2：绿（写最少代码让测试通过）**

在 `todo_manager.py` 中实现 `add_task_with_priority`：

```python
def add_task_with_priority(tasks, task_name, priority="medium"):
    """添加带优先级的任务

    priority 可以是 "high", "medium", "low"
    """
    tasks.append({
        "name": task_name,
        "done": False,
        "priority": priority
    })
    return tasks
```

运行测试，确认它通过（绿）。

**Step 3：重构（在测试保护下改进代码）**

1. 添加更多测试覆盖边界情况：
   - 无效优先级值的处理
   - 优先级排序功能（如 `get_high_priority_tasks`）

2. 重构代码，保持测试通过。

**提交物**：
- 完整的测试文件（包含 TDD 过程中写的所有测试）
- 实现后的 `todo_manager.py`
- 一个简短的 `TDD_NOTES.md`，记录：
  - 你在每个步骤中做了什么
  - 遇到的困难
  - 对 TDD 的感受（是否觉得有帮助？）

**常见错误**：
- 先写实现再写测试（这不是 TDD）
- 第一步没有看到测试失败（测试可能在测空气）
- 重构时改动太大，导致测试失败无法恢复

---

## 挑战作业（选做）

### 练习 5：PyHelper 测试套件

**目标**：为 Week 07 的 PyHelper 项目添加完整测试，达到 80%+ 的代码覆盖率。

**任务**：

1. 在 PyHelper 项目目录下创建 `tests/` 目录

2. 为以下模块编写测试：
   - `storage.py` —— 测试文件读写功能（使用 `tmp_path` fixture）
   - `records.py` —— 测试学习记录的增删改查
   - `input_handler.py` —— 测试输入校验逻辑

3. **使用 fixture 准备测试环境**：
   - 创建 `sample_records` fixture 提供示例学习记录
   - 创建 `temp_data_file` fixture 提供临时文件路径

4. **达到 80%+ 代码覆盖率**：
   - 覆盖正常路径和边界情况
   - 至少包含 10 个测试函数

**测试示例**：

```python
# tests/test_storage.py
import pytest
import json
from storage import save_learning_log, load_learning_log

def test_save_and_load(tmp_path):
    """测试保存和加载学习记录"""
    file_path = tmp_path / "test.json"
    records = [{"date": "2026-02-09", "content": "学了 pytest"}]

    save_learning_log(records, file_path)
    loaded = load_learning_log(file_path)

    assert loaded == records

def test_load_nonexistent_file(tmp_path):
    """测试加载不存在的文件"""
    file_path = tmp_path / "not_exist.json"
    result = load_learning_log(file_path)

    assert result == []  # 应该返回空列表而不是报错
```

**验证方法**：
```bash
# 安装 coverage 工具
pip install pytest-cov

# 运行测试并生成覆盖率报告
pytest tests/ --cov=. --cov-report=term-missing

# 或者只运行测试
pytest tests/ -v
```

**评分要点**：
- 测试是否覆盖核心业务逻辑
- fixture 使用是否合理
- 边界情况是否考虑周全
- 测试代码本身是否清晰可读

---

## AI 协作练习（可选）

### 练习 6：用 AI 辅助生成测试用例

**背景**：阿码听说 AI 可以帮忙写测试，于是他用某个 AI 工具生成了下面这组测试用例。你的任务是审查这些测试，找出问题并补充遗漏的边界情况。

#### AI 生成的测试代码

```python
# ai_generated_tests.py （AI 生成）

import pytest
from todo_manager import add_task, mark_done, delete_task

def test_add_task():
    """测试添加任务"""
    tasks = []
    add_task(tasks, "买牛奶")
    assert len(tasks) == 1

def test_mark_done():
    """测试标记完成"""
    tasks = [{"name": "买牛奶", "done": False}]
    mark_done(tasks, 1)
    assert tasks[0]["done"] == True

def test_delete_task():
    """测试删除任务"""
    tasks = [{"name": "买牛奶", "done": False}]
    delete_task(tasks, 1)
    assert len(tasks) == 0
```

#### 审查清单

请仔细检查这段 AI 生成的测试代码：

- [ ] **测试函数命名是否规范？**
  - 是否以 `test_` 开头？
  - 命名是否清晰地说明了测试内容？

- [ ] **断言是否完整？**
  - 除了检查列表长度，是否检查了任务内容？
  - 是否检查了返回值？

- [ ] **边界情况是否覆盖？**
  - 是否测试了空任务名？
  - 是否测试了无效索引（如 0、负数、超出范围）？
  - 是否测试了空列表的情况？

- [ ] **fixture 是否使用？**
  - 是否有重复的测试数据准备代码？
  - 是否应该使用 fixture 来复用测试数据？

- [ ] **异常路径是否测试？**
  - 是否测试了函数应该抛出异常的情况？
  - 是否使用了 `pytest.raises`？

- [ ] **测试之间是否独立？**
  - 测试是否修改了共享数据？
  - 测试顺序是否会影响结果？

#### 你的任务

1. **找出至少 3 个问题**：列出你发现的问题，说明为什么它们是问题

2. **修复并改进**：基于 AI 的代码，写出更好的测试版本

3. **补充边界情况**：至少添加 3 个 AI 遗漏的测试用例

4. **撰写审查报告**：创建 `ai_review_report.md`，包含：
   - AI 生成代码的优点
   - 发现的问题清单
   - 你的改进版本
   - 对 "AI 生成测试 vs 人工编写测试" 的思考

**提示**：
- AI 生成的代码通常能覆盖"正常路径"，但容易遗漏边界情况
- 检查 AI 是否考虑了异常处理路径
- 思考如果你是 reviewer，你会给这段测试代码打几分？

---

## 验证与提交

### 自测清单

在提交前，请确认：

- [ ] 练习 1 完成：`test_todo_manager.py` 包含至少 5 个测试函数，运行通过
- [ ] 练习 2 完成：创建了 `sample_tasks` 和 `empty_tasks` fixture，并在测试中使用
- [ ] 运行 `python3 -m pytest chapters/week_08/tests -q` 通过所有测试
- [ ] 进阶练习（如完成）：参数化测试能覆盖多种输入情况
- [ ] 进阶练习（如完成）：TDD 练习展示了红-绿-重构的过程
- [ ] 代码已提交到 Git，至少有 2 次提交（draft + verify）

### Git 提交规范

```bash
# 第一次提交（草稿）
git add chapters/week_08/test_todo_manager.py
git commit -m "draft week_08: 完成基础测试练习"

# 第二次提交（验证）
git add chapters/week_08/test_todo_manager.py
git commit -m "verify week_08: 添加 fixture 和参数化测试"

# 推送到远端
git push origin week_08
```

### Pull Request 描述模板

```markdown
## Week 08 作业完成情况

### 已完成的练习
- [x] 练习 1：Todo Manager 测试补全（5+ 测试函数）
- [x] 练习 2：Fixture 练习（2+ fixtures）

### 进阶练习（可选）
- [ ] 练习 3：参数化测试设计
- [ ] 练习 4：TDD 实践

### 挑战练习（可选）
- [ ] 练习 5：PyHelper 测试套件

### AI 协作练习（可选）
- [ ] 练习 6：审查 AI 生成的测试

### 自测结果
- 运行 `python3 -m pytest chapters/week_08/tests -q`：通过 / 失败
- 测试覆盖率（如有）：XX%

### 遇到的困难
（记录你遇到的问题和解决方法）

### 请 Review 的重点
（特别希望 reviewer 关注的地方）
```

---

## 常见问题 FAQ

**Q1: pytest 找不到我的测试函数怎么办？**

A: 检查以下几点：
1. 测试函数名是否以 `test_` 开头
2. 测试文件是否以 `test_` 开头或结尾
3. 是否在正确的目录下运行 pytest
4. 是否导入了被测函数（没有 ImportError）

**Q2: fixture 是什么？为什么要用它？**

A: fixture 是 pytest 用来管理测试准备和清理的机制。它解决了测试代码重复的问题——如果多个测试都需要同样的初始数据，可以把数据准备逻辑提取到 fixture 中，然后在测试函数的参数列表中声明使用。

**Q3: 参数化测试有什么用？**

A: 当你想用同一套测试逻辑测试多组不同的输入数据时，参数化测试非常有用。它能让你的测试代码更简洁，同时覆盖更多边界情况。

**Q4: TDD 真的有必要吗？感觉写测试比写实现还花时间。**

A: TDD 的价值在于：
1. 强迫你在写代码前想清楚需求
2. 提供安全网，让你敢于重构
3. 测试本身就是最好的文档

对于小脚本，TDD 可能显得过重；但对于需要维护的核心功能，TDD 能显著降低长期维护成本。

**Q5: 我应该测试所有函数吗？**

A: 不需要。优先测试：
1. 核心业务逻辑（如添加任务、计算成绩）
2. 容易出错的边界情况
3. 被多个地方调用的公共函数

可以暂时不测试：
1. 纯打印输出的函数
2. 简单的 getter/setter
3. 一次性的脚本代码

---

## 挑战自我

如果你想进一步挑战自己，可以尝试：

1. **Mock 测试**：学习使用 `unittest.mock` 或 `pytest-mock`，测试依赖外部服务的代码
2. **集成测试**：编写测试验证多个模块协作是否正常
3. **持续集成**：配置 GitHub Actions，每次 push 自动运行测试
4. **测试覆盖率 100%**：尝试让 PyHelper 的测试覆盖率达到 100%，看看有多难

---

祝你学习愉快！测试是编程的重要技能，掌握后你会发现改代码时更有底气，重构时更有信心。
