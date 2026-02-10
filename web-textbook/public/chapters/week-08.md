# Week 08：测试与调试——让你的代码值得信赖

> "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it."
> — Brian Kernighan

2025 年，AI 编程工具已经无处不在。GitHub Copilot 的用户数突破千万，Cursor 和 Windsurf 成为开发者的新宠。但一个悖论随之浮现：代码写得越快，隐藏的 bug 也越多。根据行业报告，超过七成的 QA 专业人员已经开始使用 AI 工具生成测试用例，但与此同时，AI 生成的代码在复杂业务逻辑上的错误率依然令人担忧。当一行 AI 生成的代码能在三秒内完成，我们还需要花三十分钟写测试吗？答案是：更需要。测试不再是"可选项"，而是 AI 时代代码质量的守门人。本周你将学习 pytest——Python 最流行的测试框架，掌握让代码值得信赖的核心技能。

---

## 前情提要

上周你把 PyHelper 从单文件拆成了多模块项目——`storage.py` 管文件读写，`input_handler.py` 管输入校验，`records.py` 管业务逻辑，`main.py` 作为入口。每个模块职责清晰，还能独立运行测试。

但小北心里一直有个疑问："我怎么知道这些模块真的工作正常？"

"运行一下看看呗，"阿码说，"输入几个数据，看看输出对不对。"

"可问题是，"小北皱着眉头，"每次改完代码，我都要手动测试一遍所有功能吗？那也太累了吧。而且万一我忘了测某个边界情况呢？"

老潘正好路过，听到了这段对话："你们说的这个问题，在工程上叫'回归测试'——每次改代码后，确保原来的功能没坏。手动做回归测试，既慢又容易漏。"

"那怎么办？"小北问。

"写**自动化测试**（automated testing），"老潘说，"用代码来测试代码。这周你们将学习 pytest——Python 最流行的测试框架。"

---

## 学习目标

完成本周学习后，你将能够：
1. 理解自动化测试的价值，能编写基本的 pytest 测试用例
2. 使用 fixture 管理测试数据和资源
3. 使用参数化测试覆盖多种边界情况
4. 体验 TDD（测试驱动开发）的完整循环
5. 给已有代码补全测试套件，确保代码质量

---

<!--
贯穿案例设计：待办事项管理器（Todo Manager）
- 第 1 节：手动测试的困境 → 从最简单的 add_task() 函数开始，手动测试发现问题
- 第 2 节：pytest 入门 → 引入 pytest，写第一个测试用例验证 add_task()
- 第 3 节：fixture 解决重复准备 → 用 fixture 管理测试前的数据准备
- 第 4 节：参数化测试覆盖边界 → 用 @pytest.mark.parametrize 覆盖空任务、超长任务、特殊字符等边界情况
- 第 5 节：TDD 体验 → 先写测试再写实现，体验"红-绿-重构"循环
最终成果：一个拥有完整测试覆盖的 Todo Manager，读者能展示给朋友看
-->

<!--
认知负荷预算：
- 本周新概念（4 个，预算上限 5 个）：
  1. pytest 断言（assert）
  2. fixture
  3. 参数化测试（@pytest.mark.parametrize）
  4. TDD 循环（红-绿-重构）
- 结论：✅ 在预算内

回顾桥设计（至少 2 个，目标引用前 3 周的概念）：
- [函数定义]（来自 week_03）：在第 1 节，测试就是调用函数并检查结果
- [异常处理]（来自 week_06）：在第 2 节，测试异常路径（pytest.raises）
- [模块导入]（来自 week_07）：在第 2 节，测试文件需要导入被测模块
- [字典操作]（来自 week_04）：贯穿案例中，todo 列表用字典存储

角色出场规划：
- 小北（第 2 节）：第一次写测试时出错——忘记以 test_ 开头命名函数，导致 pytest 没发现测试
- 阿码（第 1 节）：质疑"为什么要写测试，直接运行看不就行了？"引出测试的必要性
- 老潘（第 5 节）：分享工作中因为没写测试而踩坑的真实经历，强调测试的工程价值

AI 小专栏规划：
- AI 小专栏 #1（放在第 2 节之后）：
  - 主题：AI 辅助测试生成——让 AI 帮你写测试用例，以及为什么需要人工审查
  - 连接点：与第 2 节"pytest 入门"呼应，讨论 AI 生成测试的利弊
  - 建议搜索词："GitHub Copilot test generation 2025", "AI generated unit tests quality 2025"

- AI 小专栏 #2（放在第 4 节之后）：
  - 主题：TDD 与 AI 编程的关系——在 AI 时代，TDD 还有意义吗？
  - 连接点：与第 5 节"TDD 体验"呼应，讨论 AI 生成代码时代测试驱动开发的价值
  - 建议搜索词："TDD AI programming 2025", "test driven development LLM code generation 2025"

PyHelper 本周推进：
- 上周状态：PyHelper 已拆成多模块项目（storage.py, input_handler.py, records.py, main.py）
- 本周改进：为核心模块（storage.py 和 records.py）添加 pytest 测试
- 涉及的本周概念：pytest 断言、fixture（用于准备测试数据）、参数化测试（测试多种输入）
- 建议示例文件：examples/pyhelper/tests/
-->

## 1. 手动测试的困境

阿码最近写了一个简单的待办事项管理器。他兴冲冲地展示给小北看：

```python
# todo_manager.py

def add_task(tasks, task_name):
    """添加任务到列表"""
    tasks.append({"name": task_name, "done": False})
    return tasks

def list_tasks(tasks):
    """列出所有任务"""
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else " "
        print(f"{i}. [{status}] {task['name']}")

def mark_done(tasks, index):
    """标记任务为完成"""
    if 1 <= index <= len(tasks):
        tasks[index - 1]["done"] = True
        return True
    return False
```

"来，试试！"阿码运行了程序，手动输入了几个任务，又标记了一个完成。"看，一切正常！"

小北问："那你怎么知道它真的正常？"

"我运行了呀，"阿码说，"我添加了'买牛奶'，然后列出看看有没有，再标记完成，再看看状态变了没有——都没问题。"

"但如果我现在改了一行代码，"小北追问，"比如把 `mark_done` 里的逻辑改了一下，你怎么知道其他功能没坏？"

阿码愣了一下："那……我就再手动测一遍呗。添加任务、列出、标记完成……"

"每个功能测一遍？"小北说，"那如果我有十个功能呢？每次改代码都要手动点十次？"

阿码挠挠头："好像确实有点麻烦。"

---

三天后，阿码真的遇到了麻烦。

他在 `add_task` 里加了个功能：自动去除任务名前后的空格。代码看起来很简单：

```python
def add_task(tasks, task_name):
    """添加任务到列表"""
    task_name = task_name.strip()  # 新增：去除首尾空格
    tasks.append({"name": task_name, "done": False})
    return tasks
```

"就改了一行，应该没问题吧？"阿码心想，懒得手动测试了，直接提交了。

结果第二天小北跑来抱怨："你的待办管理器出 bug 了！我添加任务后，列表显示不对！"

原来，阿码那行代码虽然让 `add_task` 正常工作了，却意外影响了其他地方——他忘了检查 `mark_done` 在边界情况下的行为。当用户尝试标记一个不存在的任务时，程序没有给出正确的错误提示。

"我就改了一行代码……"阿码很委屈。

"这就是问题所在，"老潘正好路过，听到了这段对话，"你改了一行代码，却影响了整个程序的行为。但你只测试了改动的那个功能，没测试其他功能。"

"那我该怎么办？每次改代码都把所有功能手动测一遍？"阿码问。

"理论上是的，"老潘说，"但手动测试太慢、太容易漏了。在工程上，我们用**自动化测试**（automated testing）——写代码来测试代码。"

"用代码测试代码？"小北好奇地问。

"对。你想想，你写的 `add_task` 是一个函数，输入是任务列表和任务名，输出是更新后的列表。测试就是：调用这个函数，检查返回值是否符合预期。"

小北恍然大悟："这不就是 Week 03 学的函数调用吗？只是调用之后要检查一下结果对不对。"

"正是如此，"老潘点头，"测试的本质就是**调用函数并验证行为**。只不过我们要把验证过程也写成代码，让电脑帮我们做重复检查。"

阿码若有所思："所以如果我写了自动化测试，改完代码后跑一遍测试，就能知道有没有破坏原有功能？"

"没错。而且测试跑得快，几秒钟就能验证几十个场景，比手动点快多了。"老潘说，"这周你们将学习 pytest——Python 最流行的测试框架。"

## 2. 你的第一个 pytest 测试

既然手动测试又慢又容易漏，那我们就让电脑来帮忙。

**pytest** 是 Python 最流行的测试框架，它的设计理念很简单：测试应该写起来像普通代码，而不是像配置文件。

### 安装 pytest

首先，确保你已经安装了 pytest：

```bash
pip install pytest
```

安装完成后，你可以验证一下：

```bash
pytest --version
```

### 写第一个测试

小北决定给阿码的 `add_task` 函数写个测试。她新建了一个文件叫 `test_todo.py`：

```python
# test_todo.py
from todo_manager import add_task

def test_add_task():
    """测试添加任务功能"""
    tasks = []
    result = add_task(tasks, "买牛奶")

    assert len(result) == 1
    assert result[0]["name"] == "买牛奶"
    assert result[0]["done"] == False
```

"看起来挺简单的，"小北心想，"就是调用函数，然后用 `assert` 检查结果。这和 Week 03 学的函数调用、参数传递、返回值是一样的——测试本质上就是调用函数，然后验证返回值是否符合预期。"

她运行了测试：

```bash
pytest test_todo.py
```

结果 pytest 输出：

```
======================== test session starts =========================
platform darwin -- Python 3.11.0, pytest-7.4.0
rootdir: /Users/xiaobei/code
plugins: none
collected 0 items

======================== no tests ran =========================
```

"什么？没有测试被收集到？"小北懵了。

她检查了三遍代码，确认没写错。最后只好去问老潘。

老潘看了一眼，笑了："你函数名是不是没以 `test_` 开头？"

小北低头一看——她把函数名写成了 `add_task_test()`，而不是 `test_add_task()`。

"pytest 默认只收集以 `test_` 开头的函数作为测试用例，"老潘解释道，"这是约定，这样 pytest 能快速识别哪些函数是测试，哪些是普通辅助函数。"

小北改了过来，再次运行：

```bash
pytest test_todo.py
```

这次输出变了：

```
======================== test session starts =========================
platform darwin -- Python 3.11.0, pytest-7.4.0
rootdir: /Users/xiaobei/code
plugins: none
collected 1 item

test_todo.py .                                                 [100%]

======================== 1 passed =========================
```

"通过了！"小北兴奋地喊道。那个绿色的小点 `.` 表示一个测试通过，看起来特别有成就感。

### 测试失败长什么样

阿码凑过来："如果测试失败呢？会报错吗？"

"试试不就知道了，"小北故意把预期结果写错：

```python
def test_add_task_wrong():
    """故意写错的测试"""
    tasks = []
    result = add_task(tasks, "买牛奶")

    assert result[0]["name"] == "买面包"  # 故意写错
```

运行结果：

```
test_todo.py F                                                 [100%]

======================== FAILURES =========================
________________________ test_add_task_wrong ________________________

    def test_add_task_wrong():
        """故意写错的测试"""
        tasks = []
        result = add_task(tasks, "买牛奶")

>       assert result[0]["name"] == "买面包"
E       AssertionError: assert '买牛奶' == '买面包'
E         - 买面包
E         + 买牛奶

test_todo.py:15: AssertionError
```

"哇，pytest 的报错信息好详细！"阿码惊叹，"它甚至用 `+` 和 `-` 标出了哪里不一样。"

"这比我自己 `print` 调试方便多了，"小北说，"而且如果我有几十个测试，一眼就能看出哪个失败了。`assert` 后面的条件判断本质上就是 Week 02 学的布尔表达式——结果为真就通过，为假就失败。"

### 测试异常情况

小北想起 Week 06 学的异常处理："那如果函数应该抛出异常呢？比如传入非法参数？"

老潘点头："用 `pytest.raises` 来测试异常。这和 Week 06 学的 `try/except` 本质一样——都是捕获异常——但 pytest 的写法更简洁，还能验证异常的具体类型（比如 ValueError、TypeError）。"

小北给 `mark_done` 写了个异常测试：

```python
import pytest
from todo_manager import add_task, mark_done

def test_mark_done_invalid_index():
    """测试标记不存在的任务应该返回 False"""
    tasks = [{"name": "买牛奶", "done": False}]
    result = mark_done(tasks, 99)  # 索引 99 不存在
    assert result == False
```

"等等，"小北突然想到，"如果我想测试函数真的会抛出异常呢？"

她想起 Week 06 学的 `try/except`，但测试里写起来有点啰嗦。pytest 提供了更简洁的方式：

```python
def test_add_task_empty_name():
    """测试添加空任务名应该抛出异常"""
    # 假设我们修改了 add_task，让它拒绝空字符串
    with pytest.raises(ValueError):
        add_task([], "")  # 空字符串应该触发 ValueError
```

`pytest.raises` 是一个**上下文管理器**（context manager），它确保代码块里确实抛出了指定的异常。如果没抛，或者抛了别的异常，测试就会失败。

"这和 Week 06 学的 `try/except` 有点像，"小北说，"但写起来更简洁，而且专门用于测试。"

"对，"老潘说，"pytest 的断言和异常测试都很直观。你不需要学一堆新的 API，用普通的 Python 语法就能写测试。"

### 测试文件的组织

小北现在有了三个测试函数，都放在 `test_todo.py` 里。她问老潘："测试文件应该怎么组织？"

"通常有两种方式："老潘说，"一种是把测试文件和被测代码放在一起，比如 `todo_manager.py` 旁边放 `test_todo_manager.py`；另一种是建一个专门的 `tests/` 目录，所有测试放里面。"

"哪种更好？"

"小项目用第一种，方便；大项目用第二种，清晰。"老潘说，"重要的是保持一致，别混着用。"

小北决定用第二种方式。她新建了一个 `tests/` 目录，把 `test_todo.py` 移了进去。

但这时她遇到了 Week 07 学过的问题：测试文件在 `tests/` 目录里，怎么导入被测模块 `todo_manager.py`？

```python
# tests/test_todo.py
from todo_manager import add_task  # ModuleNotFoundError!
```

"啊，这是 Week 07 的模块导入问题！"小北想起来了。她有两个选择：

1. 把项目根目录加到 Python 路径里
2. 用相对导入（如果包结构正确的话）

最简单的做法是在项目根目录运行 pytest，pytest 会自动把当前目录加到路径里：

```bash
# 在项目根目录运行
pytest tests/
```

这样 `from todo_manager import add_task` 就能正常工作了。

"原来 Week 07 学的模块导入知识在这里用上了，"小北感慨，"`import` 和 `from ... import` 的规则在测试文件里同样适用。测试也是代码，也要遵守模块系统的规则。"

现在小北已经能写基本的测试了。但她发现一个问题：每个测试函数开头都要创建空任务列表，代码有点重复。有没有办法让测试准备更简洁？

> **AI 时代小专栏：AI 辅助测试生成**
>
> 既然 pytest 让写测试变得简单，那能不能让 AI 来帮我们写测试？答案是：可以，但要谨慎。
>
> 2025 年的数据显示，AI 生成的测试代码覆盖率达到 75%，比人工编写的 60% 还要高。GitHub Copilot 与 Playwright MCP 的结合，甚至能将测试自动化效率提升 37%。这听起来很美好——但有一个陷阱：AI 在边界条件和复杂业务逻辑上表现不佳。它擅长生成"正常路径"的测试，却容易遗漏那些真正会出问题的边缘情况。
>
> 所以，如果你用 AI 生成测试，请务必检查以下几点：
> 1. **边界值是否覆盖**：AI 可能测试了 `add_task("买牛奶")`，但忘了测试空字符串 `""` 或超长字符串
> 2. **异常路径是否测试**：AI 可能只测了"成功添加"，没测"添加失败时应该抛什么异常"
> 3. **业务规则是否正确**：AI 不知道你的业务逻辑，它可能生成语法正确但逻辑错误的断言
>
> 老潘的建议是：让 AI 生成测试骨架，人工填充边界情况。AI 是加速器，不是替代品。你刚学的 `assert` 和 `pytest.raises`，正是审查 AI 生成代码的必备技能。
>
> 参考（访问日期：2026-02-09）：
> - https://ttcglobal.com/what-we-think/blog/how-github-copilot-playwright-mcp-boosted-test-automation-efficiency-by-up-to-37
> - https://computerfraudsecurity.com/index.php/journal/article/view/784


## 3. 用 fixture 准备测试环境

小北写了好几个测试函数，发现每个开头都差不多：

```python
def test_add_task():
    tasks = []  # 每次都创建空列表
    result = add_task(tasks, "买牛奶")
    # ...

def test_mark_done():
    tasks = []  # 又创建一次
    add_task(tasks, "买牛奶")
    result = mark_done(tasks, 1)
    # ...

def test_list_tasks():
    tasks = []  # 再创建一次
    # ...
```

"这重复代码也太多了，"小北抱怨，"而且如果我想给每个测试准备不同的初始数据，比如一个已有三个任务的列表，每个函数都要重新写一遍。"

阿码在旁边说："那你写个辅助函数呗，返回一个初始化好的任务列表。"

"是可以，但 pytest 有更好的方式——**fixture**（固定装置）。"

### 什么是 fixture

**fixture** 是 pytest 用来管理测试准备和清理的机制。你可以把它理解成"测试的上下文环境"——每个测试运行前，fixture 帮你准备好数据；测试结束后，fixture 帮你清理资源。

小北写了一个 fixture：

```python
import pytest
from todo_manager import add_task

@pytest.fixture
def empty_tasks():
    """提供一个空的任务列表"""
    return []

def test_add_task_with_fixture(empty_tasks):
    """使用 fixture 的测试"""
    result = add_task(empty_tasks, "买牛奶")

    assert len(result) == 1
    assert result[0]["name"] == "买牛奶"
```

"等等，"小北有点困惑，"`test_add_task_with_fixture` 的参数 `empty_tasks` 是从哪来的？"

这就是 pytest 的魔法：当你把 fixture 函数名作为测试函数的参数时，pytest 会自动调用那个 fixture，把返回值传进来。

"所以 `empty_tasks` 参数接收的是 fixture 函数 `empty_tasks()` 的返回值——一个空列表？"小北恍然大悟。

"对，"老潘正好路过，"fixture 的核心思想是**依赖注入**。测试函数声明它需要什么，pytest 负责提供。这样测试代码更简洁，而且 fixture 可以在多个测试之间复用。"

### fixture 的清理功能

老潘补充道："fixture 不只是准备数据，还能做清理。比如测试时创建了临时文件，测试结束后要删除。"

他用 `yield` 改写了小北的 fixture：

```python
@pytest.fixture
def sample_tasks():
    """提供一个有三个任务的列表，测试后自动清理"""
    tasks = [
        {"name": "买牛奶", "done": True},
        {"name": "写作业", "done": False},
        {"name": "运动", "done": False}
    ]
    print("\n[fixture] 测试数据准备好了")

    yield tasks  # 把数据交给测试函数

    # 测试结束后执行清理
    print("\n[fixture] 测试结束，清理中...")
    tasks.clear()
```

"`yield` 之前的代码在测试前运行，`yield` 之后的代码在测试后运行，"老潘解释，"这有点像 Week 05 学的文件上下文管理器——`with open()` 打开文件，代码块结束后自动关闭。"

小北运行测试，加上 `-s` 参数显示 print 输出：

```bash
pytest tests/test_todo.py -s
```

输出：

```
[fixture] 测试数据准备好了
.[fixture] 测试结束，清理中...
```

"所以 fixture 不仅能准备数据，还能保证测试环境的干净，"小北说，"每个测试都用全新的数据，不会互相影响。"

"这正是单元测试的重要原则，"老潘点头，"测试之间要相互独立，不能一个测试的结果影响另一个测试。"

老潘想了想，又补充道："你可以把 fixture 想象成租房——入住前检查家具（准备），住进去使用（测试），退房时打扫干净（清理）。yield 就是'暂停执行，稍后再继续'的意思：测试前暂停，把数据交给测试函数；测试结束后再继续执行清理代码。"

小北突然笑了："那我不就成了'测试界的二房东'？专门给测试函数准备'拎包入住'的环境。"

"差不多，"老潘也笑了，"而且是个靠谱的二房东——保证每个'租客'住的都是新房，没有上一家留下的垃圾。"

### 更实用的 fixture：临时文件

小北想到 Week 05 学的文件操作："如果我要测试文件读写功能呢？比如 `storage.py` 里的 `save_tasks()` 和 `load_tasks()`？"

"pytest 内置了一个很有用的 fixture 叫 `tmp_path`，"老潘说，"它提供一个临时目录，测试结束后自动删除。"

```python
def test_save_and_load_tasks(tmp_path):
    """测试保存和加载任务"""
    from todo_manager import save_tasks, load_tasks

    # tmp_path 是一个 Path 对象，指向临时目录
    file_path = tmp_path / "tasks.json"

    tasks = [{"name": "买牛奶", "done": False}]

    # 保存
    save_tasks(tasks, file_path)

    # 加载
    loaded = load_tasks(file_path)

    assert loaded == tasks
```

"`tmp_path` 是 pytest 内置的？"小北惊讶，"不用我自己定义？"

"对，pytest 提供了很多内置 fixture，`tmp_path` 是最常用的之一。"老潘说，"在公司里写测试，几乎每次都会用到它——谁也不想测试完后留下一堆临时文件。"

小北想起 Week 04 学的字典操作："我们的任务列表是用字典存的，fixture 返回字典或列表，本质上和 Week 04 学的数据结构是一样的。"

"没错，"老潘说，"fixture 返回什么数据都行——字典、列表、对象、文件路径，都可以。它只是帮你管理这些数据的生命周期。"

现在小北的测试代码简洁多了。fixture 帮她处理了重复的数据准备，测试函数只需要关注"测什么"，不用关心"怎么准备"。

但还有一个问题：如果要测试很多不同的输入情况，比如空任务名、超长任务名、带 emoji 的任务名，难道要写几十个测试函数吗？

## 4. 参数化测试：一次覆盖多种情况

阿码看完小北的测试代码，突然想到一个问题："如果我要测试各种边界情况，比如空任务名、超长任务名、带 emoji 的任务名，难道要写十几个测试函数？"

"理论上是的，"小北说，"每个输入情况写一个测试函数。"

"那也太啰嗦了，"阿码抱怨，"这些测试的逻辑都一样，只是输入数据不同。"

小北点点头，她刚试着手动写了三个测试函数，就已经感觉到重复了："而且容易写错。我刚才就搞混了参数顺序，把预期结果和输入值写反了，排查了半天。"

老潘正好听到："用**参数化测试**（parametrized testing）。pytest 允许你用同一套测试逻辑，跑多组不同的输入数据。"

### 用 parametrize 装饰器

pytest 提供了 `@pytest.mark.parametrize` 装饰器，可以把多组参数传给同一个测试函数：

```python
import pytest
from todo_manager import add_task

@pytest.mark.parametrize("task_name,expected_name", [
    ("买牛奶", "买牛奶"),           # 普通情况
    ("  买牛奶  ", "买牛奶"),       # 带空格，应该被 strip
    ("写作业！", "写作业！"),       # 带标点
    ("Task 123", "Task 123"),       # 英文数字混合
])
def test_add_task_various_names(task_name, expected_name):
    """测试各种任务名的处理"""
    tasks = []
    result = add_task(tasks, task_name)

    assert result[0]["name"] == expected_name
```

运行结果：

```
test_todo.py::test_add_task_various_names[买牛奶-买牛奶] PASSED
test_todo.py::test_add_task_various_names[  买牛奶  -买牛奶] PASSED
test_todo.py::test_add_task_various_names[写作业！-写作业！] PASSED
test_todo.py::test_add_task_various_names[Task 123-Task 123] PASSED
```

"一个测试函数，跑了四组数据！"阿码兴奋地说，"而且 pytest 还给每组数据起了名字，一眼就能看出哪组过了、哪组挂了。"

"这比写四个几乎一样的测试函数简洁多了，"小北说，"而且如果以后要加新的测试数据，只需要在列表里加一行。"

### 测试边界情况

阿码的追问还没结束："那中文任务名呢？emoji 呢？超长任务名呢？"

"都加上呗，"小北说，"参数化测试就是用来覆盖各种边界情况的。这和 Week 06 学的输入校验是同一个思路——我们当时用条件判断检查输入是否合法，现在用测试来验证这些检查是否正确工作。"

她扩展了测试数据：

```python
@pytest.mark.parametrize("task_name,should_accept", [
    ("买牛奶", True),                    # 正常中文
    ("🥛 买牛奶", True),                 # 带 emoji
    ("", False),                         # 空字符串，应该拒绝
    ("a" * 1000, False),                 # 超长任务名，应该拒绝
    ("<script>alert('xss')</script>", True),  # 可疑字符（假设我们不过滤）
])
def test_add_task_edge_cases(task_name, should_accept):
    """测试边界情况"""
    tasks = []

    if should_accept:
        result = add_task(tasks, task_name)
        assert len(result) == 1
        assert result[0]["name"] == task_name
    else:
        # 应该抛出异常或返回错误
        with pytest.raises((ValueError, IndexError)):
            add_task(tasks, task_name)
```

"等等，"阿码指着最后一行，"`<script>` 那段是什么？"

"这是 Week 06 学的输入校验的延伸，"小北说，"我们要考虑用户可能输入什么奇怪的东西。虽然这个待办管理器只是本地运行，但如果以后变成 Web 应用，这种输入就可能带来安全问题。"

"所以你是在用测试来验证输入校验的逻辑？"阿码问。

"对。Week 06 我们学了怎么写输入校验的代码，这周我们学怎么测试那些校验代码是否真的有效。"小北说，"测试和实现是相辅相成的。"

### 多参数组合

老潘走过来，看了眼代码："参数化测试还能做笛卡尔积——如果你有两个参数，每个参数有多个值，pytest 会自动组合所有情况。"

```python
@pytest.mark.parametrize("initial_count", [0, 1, 5])
@pytest.mark.parametrize("task_name", ["任务A", "任务B"])
def test_add_task_multiple_dimensions(initial_count, task_name):
    """测试不同初始任务数量下的添加功能"""
    tasks = [{"name": f"已有任务{i}", "done": False} for i in range(initial_count)]

    result = add_task(tasks, task_name)

    assert len(result) == initial_count + 1
    assert result[-1]["name"] == task_name
```

"等等，"阿码数了数，"initial_count 有 3 个值，task_name 有 2 个值，那会产生……"

"6 个测试用例，"小北说，"就像乘法表一样，每个 initial_count 都会和每个 task_name 组合一遍："

| initial_count | task_name | 生成的测试名 |
|--------------|-----------|-------------|
| 0 | 任务A | `[0-任务A]` |
| 0 | 任务B | `[0-任务B]` |
| 1 | 任务A | `[1-任务A]` |
| 1 | 任务B | `[1-任务B]` |
| 5 | 任务A | `[5-任务A]` |
| 5 | 任务B | `[5-任务B]` |

运行 pytest，确实看到 6 个测试：

```
test_todo.py::test_add_task_multiple_dimensions[0-任务A] PASSED
test_todo.py::test_add_task_multiple_dimensions[0-任务B] PASSED
test_todo.py::test_add_task_multiple_dimensions[1-任务A] PASSED
test_todo.py::test_add_task_multiple_dimensions[1-任务B] PASSED
test_todo.py::test_add_task_multiple_dimensions[5-任务A] PASSED
test_todo.py::test_add_task_multiple_dimensions[5-任务B] PASSED
```

"这相当于写了 6 个测试函数，但代码只有一份，"老潘说，"在公司里，我们经常用这种方式测试不同配置组合下的行为。"

### 标记预期失败

小北想到一个问题："如果某个测试数据我知道现在会失败，但暂时不想修，怎么办？"

"用 `pytest.param` 标记为预期失败，"老潘说，"这样测试不会挂，但你会记得还有地方要修。"

```python
@pytest.mark.parametrize("task_name,expected", [
    ("正常任务", "正常任务"),
    pytest.param(
        "", "",  # 空任务名，目前会失败
        marks=pytest.mark.xfail(reason="空任务名校验尚未实现")
    ),
])
def test_add_task_with_xfail(task_name, expected):
    tasks = []
    result = add_task(tasks, task_name)
    assert result[0]["name"] == expected
```

标记为 `xfail` 的测试如果失败了，pytest 会显示 `X` 而不是 `F`，整个测试套件仍然能通过。但如果它意外通过了，pytest 会提醒你——说明那个 bug 已经被修好了。

"这有点像 TODO 清单，"小北说，"但比写在代码注释里更正式，因为测试框架会跟踪它。"

"对，"老潘点头，"测试不仅是验证代码正确性的工具，也是管理技术债务的工具。"

现在小北和阿码的待办管理器已经有了完善的测试覆盖。参数化测试让批量验证边界情况变得简单，但这些都是"先写代码再补测试"的思路。

"如果反过来呢？"老潘突然问，"先写测试，再写代码——甚至让测试来决定要写什么代码。"

这就是 TDD（测试驱动开发），一种听起来有点反直觉，但在工程实践中被反复验证有效的开发方式。
> **AI 时代小专栏：TDD 与 AI 编程的关系**
>
> 阿码看着 TDD 的"红-绿-重构"循环，忍不住问："既然 AI 能直接生成代码，为什么还要先写测试？这不是多此一举吗？"
>
> 这个问题在 2025 年有了新答案。在 Devnexus 会议上，专家提出了 **Test-Driven Generation (TDG)** 的新范式——人类写测试，LLM 生成实现。ACM 的研究也证实，为 LLM 提供测试用例能显著提升代码生成质量。
>
> 换句话说，TDD 在 AI 时代不是过时了，而是进化了。测试不再是"验证代码对不对"的工具，而是"告诉 AI 我要什么"的规格说明书。当你先写测试，你实际上是在用代码精确描述需求——这比自然语言提示词更无歧义。
>
> 数据显示，采用 TDD 的团队缺陷密度降低 40-90%。在 AI 生成代码的时代，这个优势更加明显：测试成为人类意图与 AI 实现之间的桥梁。没有测试，你只是在"希望" AI 理解对了；有了测试，你能"确认" AI 理解对了。
>
> 所以阿码的问题应该反过来问：既然有 AI 帮忙写实现，为什么不先写测试来明确需求？
>
> 参考（访问日期：2026-02-09）：
> - https://devnexus.com/posts/tdd-generative-ai-a-perfect-pairing-bouke-nijhuis
> - https://dl.acm.org/doi/10.1145/3691620.3695527
> - https://www.builder.io/blog/test-driven-development-ai

## 5. 体验 TDD：先写测试，再写代码

小北和阿码的待办管理器还差一个功能：删除任务。阿码说："我直接写 `delete_task` 函数吧，反正逻辑很简单。"

"等等，"老潘正好路过，"要不要试试 TDD？"

"TDD？"

"**测试驱动开发**（Test-Driven Development），"老潘说，"先写测试，再写实现。"

"先写测试？"阿码不解，"函数都不存在，怎么测试？"

"就是因为它不存在，你才要想清楚它应该做什么、输入什么、返回什么。"老潘说，"测试就是你给函数定的'契约'。"

老潘坐下来，讲了一个故事："我三年前参与一个电商网站的订单系统项目，当时赶进度，大家都没有写测试。三个月后，产品经理说双十一要改一下优惠券计算逻辑——就改一行代码。我改了，本地测了一下，没问题，提交了。"

"然后呢？"小北问。

"然后线上炸了。"老潘苦笑，"那一行代码影响了我以为无关的退款流程。双十一当天，用户申请退款时金额全算错了。如果有测试，至少能在提交前发现。"

"所以 TDD 能避免这种情况？"阿码问。

"TDD 不能保证不出 bug，但能帮你更早发现问题，而且让你对重构更有信心。"老潘说，"来，我带你走一遍完整的 TDD 循环。"

### 红-绿-重构循环

TDD 的核心是三个步骤的循环：

1. **红**：写一个测试，运行，看到它失败（因为实现还不存在）
2. **绿**：写最少的代码让测试通过
3. **重构**：在测试保护下改进代码，保持测试通过

"为什么第一步要看到失败？"小北问。

"确认测试是有效的，"老潘说，"如果测试一开始就能通过，那它可能在测空气——无论实现对不对，它都显示通过。"

### 第一步：写测试（红）

他们决定给 `delete_task` 写测试。先想清楚需求：

- 输入：任务列表和要删除的索引（1-based）
- 正常情况：删除成功，返回 True
- 边界情况：索引非法，返回 False

小北写了第一个测试：

```python
# test_todo.py

def test_delete_task_success():
    """测试成功删除任务"""
    from todo_manager import delete_task

    tasks = [
        {"name": "买牛奶", "done": False},
        {"name": "写作业", "done": False}
    ]

    result = delete_task(tasks, 1)  # 删除第一个任务

    assert result == True
    assert len(tasks) == 1
    assert tasks[0]["name"] == "写作业"
```

运行测试：

```bash
pytest test_todo.py::test_delete_task_success -v
```

结果：

```
test_todo.py::test_delete_task_success FAILED

ImportError: cannot import name 'delete_task' from 'todo_manager'
```

"红了！"老潘说，"这就是第一步——确认测试会因为实现缺失而失败。"

### 第二步：写实现（绿）

现在写最少的代码让测试通过：

```python
# todo_manager.py

def delete_task(tasks, index):
    """删除指定索引的任务"""
    if 1 <= index <= len(tasks):
        tasks.pop(index - 1)
        return True
    return False
```

再次运行测试：

```
test_todo.py::test_delete_task_success PASSED
```

"绿了！"小北兴奋地说，"测试通过了。"

"现在你知道实现是对的，因为测试在保护你。"老潘说，"接下来，写更多测试覆盖边界情况。"

阿码补充了非法索引的测试：

```python
@pytest.mark.parametrize("invalid_index", [0, -1, 99])
def test_delete_task_invalid_index(invalid_index):
    """测试删除非法索引返回 False"""
    from todo_manager import delete_task

    tasks = [{"name": "买牛奶", "done": False}]
    result = delete_task(tasks, invalid_index)

    assert result == False
    assert len(tasks) == 1  # 任务列表应该保持不变
```

运行，通过。现在他们有了两个测试，覆盖了正常路径和边界情况。

### 第三步：重构

老潘看了看代码："实现能工作，但可以更简洁。注意到没有？`index - 1` 出现了两次。"

"对，"小北说，"我们可以提取一个变量。"

重构后的代码：

```python
def delete_task(tasks, index):
    """删除指定索引的任务"""
    list_index = index - 1  # 转换为 0-based 索引
    if 0 <= list_index < len(tasks):
        tasks.pop(list_index)
        return True
    return False
```

运行所有测试——仍然通过。

"这就是 TDD 的威力，"老潘说，"你可以放心重构，因为测试会告诉你有没有破坏原有功能。如果没有测试，你敢随便改吗？"

"不敢，"阿码老实承认，"我怕改出 bug。"

老潘突然问："但如果测试通过了，就一定没问题吗？"

"什么意思？"小北疑惑。

"考考你们，"老潘说，"假设我写的测试是这样的："

```python
def test_delete_task_loose():
    """一个太宽松的测试"""
    tasks = [{"name": "买牛奶", "done": False}]
    result = delete_task(tasks, 1)
    # 只检查返回 True，不检查任务是否真的被删除了
    assert result == True
```

"这个测试会通过，"老潘说，"但如果 `delete_task` 根本没删除任务，只是返回 True，测试也发现不了。"

小北恍然大悟："所以测试的质量很重要！不仅要'有'测试，还要'测对东西'。"

"对，"老潘点头，"这就是为什么阿码刚才的测试要加 `assert len(tasks) == 1`——验证任务列表真的没变。测试就像保险，保额不够，出事时还是赔不起。"

"这就是 Week 07 学的**重构**（refactoring）和测试的结合。"老潘说，"重构是改变代码结构而不改变行为。但你怎么知道行为没变？靠测试。"

### 完整的 TDD 流程

小北总结道："所以 TDD 不是'写更多测试'，而是'测试先行'——在写实现之前，先想清楚函数应该做什么。"

"对，"老潘点头，"而且测试代码也是代码，要遵循同样的质量标准。Week 07 我们学了模块化，测试也应该模块化——每个测试只测一个概念，测试之间不要互相依赖。"

阿码看着自己的测试文件："我发现写测试其实比写实现花的时间还长。"

"正常，"老潘说，"但这是一次性投入。测试写好后，每次改代码都能快速验证，省下的时间远超写测试的时间。而且——"

老潘顿了顿："测试是最好的文档。你看 `test_delete_task_success`，它比任何注释都清楚地说明了 `delete_task` 应该怎么用、会有什么效果。"

现在小北和阿码的待办管理器有了完整的测试覆盖，包括添加、列出、标记完成、删除四个核心功能。他们体验到了 TDD 的完整循环，也理解了为什么测试在工程实践中如此重要。

---

## PyHelper 进度

上周你把 PyHelper 拆成了多模块项目——`storage.py` 管文件读写，`records.py` 管学习记录，`main.py` 作为入口。但就像待办管理器一样，你怎么知道这些模块真的工作正常？

这周，给 PyHelper 穿上测试的铠甲。

### 给 storage.py 写测试

`storage.py` 负责学习记录的存取。测试它需要处理临时文件——正好用上 `tmp_path` fixture。

```python
# tests/test_storage.py
import pytest
import json
from storage import save_learning_log, load_learning_log

def test_save_and_load_learning_log(tmp_path):
    """测试保存和加载学习记录"""
    file_path = tmp_path / "test_log.json"

    records = [
        {"date": "2026-02-09", "content": "学了 pytest 基础", "mood": "开心"},
        {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"}
    ]

    # 保存
    save_learning_log(records, file_path)

    # 加载
    loaded = load_learning_log(file_path)

    assert loaded == records

def test_load_nonexistent_file(tmp_path):
    """测试加载不存在的文件返回空列表"""
    file_path = tmp_path / "not_exist.json"

    result = load_learning_log(file_path)

    assert result == []
```

这里测试了两个场景：正常存取和文件不存在时的行为。`tmp_path` 保证了测试结束后临时文件会被自动清理。

### 给 records.py 写测试

`records.py` 处理业务逻辑，比如添加记录、统计学习天数。

```python
# tests/test_records.py
import pytest
from records import add_record, count_study_days

@pytest.fixture
def sample_records():
    """提供示例学习记录"""
    return [
        {"date": "2026-02-09", "content": "学了 pytest", "mood": "开心"},
        {"date": "2026-02-08", "content": "学了 fixture", "mood": "困惑"},
        {"date": "2026-02-07", "content": "学了异常处理", "mood": "兴奋"}
    ]

def test_add_record(sample_records):
    """测试添加新记录"""
    new_record = {"date": "2026-02-10", "content": "学了 TDD", "mood": "期待"}

    result = add_record(sample_records, new_record)

    assert len(result) == 4
    assert result[-1] == new_record

def test_count_study_days(sample_records):
    """测试统计学习天数"""
    result = count_study_days(sample_records)

    assert result == 3  # 三条记录，三天
```

`sample_records` fixture 返回一个有三条记录的列表，多个测试可以共享这个数据准备逻辑。

### 参数化测试边界情况

还记得阿码追问的边界情况吗？PyHelper 也要测试这些。

```python
@pytest.mark.parametrize("content,should_accept", [
    ("今天学了 Python", True),           # 正常内容
    ("  有空格的内容  ", True),          # 带空格
    ("", False),                          # 空内容，应该拒绝
    ("a" * 5000, False),                  # 超长内容
    ("🐍 Python 学习", True),            # 带 emoji
])
def test_add_record_validation(content, should_accept):
    """测试添加记录时的输入校验"""
    records = []
    new_record = {"date": "2026-02-09", "content": content, "mood": "开心"}

    if should_accept:
        result = add_record(records, new_record)
        assert len(result) == 1
    else:
        # 应该抛出异常
        with pytest.raises(ValueError):
            add_record(records, new_record)
```

这个测试覆盖了 Week 06 学过的输入校验场景——正常内容、带空格、空内容、超长内容、特殊字符。

### 运行 PyHelper 的测试

现在你可以在 PyHelper 目录下运行所有测试：

```bash
pytest tests/ -v
```

输出类似：

```
tests/test_storage.py::test_save_and_load_learning_log PASSED
tests/test_storage.py::test_load_nonexistent_file PASSED
tests/test_records.py::test_add_record PASSED
tests/test_records.py::test_count_study_days PASSED
tests/test_records.py::test_add_record_validation[今天学了 Python-True] PASSED
tests/test_records.py::test_add_record_validation[  有空格的内容  -True] PASSED
tests/test_records.py::test_add_record_validation[-False] PASSED
tests/test_records.py::test_add_record_validation[...] PASSED
tests/test_records.py::test_add_record_validation[🐍 Python 学习-True] PASSED
```

看到这一串绿色的小点，是不是很有成就感？

老潘看到这段代码，点了点头："这就对了。在公司里，我们要求每个功能都要有测试覆盖。不只是为了找 bug，更是为了——"

"为了以后改代码时有信心？"小北接话。

"对。你现在可以大胆重构 PyHelper，因为测试会告诉你有没有破坏原有功能。这就是测试的真正价值。"

---

## Git 本周要点

本周必会命令：
- `git status` —— 查看当前状态
- `git add -A` —— 添加所有修改
- `git commit -m "message"` —— 提交修改
- `git log --oneline -n 10` —— 查看最近 10 次提交

常见坑：
- **测试文件命名**：pytest 默认只收集以 `test_` 开头或结尾的文件，注意命名规范
- **__pycache__ 提交**：测试运行后会生成 `__pycache__` 和 `.pytest_cache`，建议添加到 `.gitignore`
- **测试数据残留**：测试生成的临时文件要记得清理，或用 `tmp_path` fixture

测试相关 `.gitignore` 模板：
```
__pycache__/
*.pyc
.pytest_cache/
.coverage
htmlcov/
```

Pull Request (PR)：
- 本周延续 PR 流程：分支 → 多次提交 → push → PR → review → merge
- PR 描述模板：
  ```markdown
  ## 本周做了什么
  - 学习了 pytest 基础，编写了第一个测试用例
  - 使用 fixture 管理测试数据准备
  - 使用参数化测试覆盖边界情况
  - 体验了 TDD 开发流程
  - 给 PyHelper 核心功能补全了测试

  ## 自测
  - [ ] 运行 `python3 -m pytest chapters/week_08/tests -q` 通过
  - [ ] Todo Manager 测试覆盖率达标
  - [ ] PyHelper 测试能正常运行

  ## 待 review
  请重点检查测试用例的完整性和边界情况覆盖
  ```

---

## 本周小结（供下周参考）

本周你学会了用 pytest 给代码写自动化测试——从简单的 `assert` 断言，到用 fixture 管理测试数据，再到用参数化测试覆盖多种边界情况。你还体验了完整的 TDD 循环：先写测试（红）、再写实现（绿）、最后重构，在测试的保护下改进代码。现在你的待办管理器和 PyHelper 都有了测试覆盖，改代码时更有底气了。

下周我们将进入 Week 09：文本处理——学习字符串操作和正则表达式，让你的程序能够处理更复杂的文本数据，比如从学习笔记中搜索关键词、提取日期等。

---

## Definition of Done（学生自测清单）

完成本周学习后，请确认你能做到以下事情：

**核心技能**：你能编写基本的 pytest 测试函数（以 `test_` 开头），使用 `assert` 进行断言验证；能使用 `pytest.raises` 测试异常情况；能使用 fixture 管理测试数据准备；能使用 `@pytest.mark.parametrize` 进行参数化测试；能体验完整的 TDD 循环（红-绿-重构）。

**编程哲学**：你理解**自动化测试**的价值——确保代码正确、防止回归、提高重构信心。你知道什么时候该写测试（核心业务逻辑）、什么时候可以暂时不写（一次性脚本）。你理解 TDD 的"测试先行"思维，能在新功能开发中应用这一方法。

**实践能力**：你能给已有代码补全测试套件；能设计覆盖正常路径和边界情况的测试用例；能用 pytest 运行测试并解读测试结果；能给 PyHelper 核心功能添加测试。

**工程习惯**：你至少提交了 2 次 Git（draft + verify），并且运行 `python3 -m pytest chapters/week_08/tests -q` 通过了所有测试。

---

**如果你想验证自己的掌握程度**，试着回答这些问题：

- 为什么测试函数要以 `test_` 开头？如果不用这个前缀会怎样？
- fixture 解决了什么问题？什么时候应该使用 fixture？
- 参数化测试有什么好处？什么情况下适合使用参数化测试？
- TDD 的"红-绿-重构"循环分别指什么？为什么测试要先行？
- 给已有代码补测试时，应该优先测试哪些功能？

如果你能自信地回答这些问题，说明你已经掌握了本周的核心内容。

---

<!--
章节结构骨架（供 chapter-writer 参考）：

1. 章首导入（引言格言 + 时代脉搏）——已完成
2. 前情提要——已完成
3. 学习目标——已完成
4. 贯穿案例设计说明（HTML 注释）——已完成
5. 认知负荷 + 回顾桥 + 角色出场规划（HTML 注释）——已完成
6. AI 小专栏规划（HTML 注释）——已完成
7. 第 1 节：手动测试的困境——待撰写
8. 第 2 节：你的第一个 pytest 测试——待撰写
9. AI 小专栏 #1——待撰写（放在第 2 节之后）
10. 第 3 节：用 fixture 准备测试环境——待撰写
11. 第 4 节：参数化测试——待撰写
12. AI 小专栏 #2——待撰写（放在第 4 节之后）
13. 第 5 节：体验 TDD——待撰写
14. PyHelper 进度——待撰写
15. Git 本周要点——已完成
16. 本周小结（供下周参考）——待撰写
17. Definition of Done——已完成
-->
