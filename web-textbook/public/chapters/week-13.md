# Week 13：用 AI Agent 协作开发

> "Alone we can do so little; together we can do so much."
> — Helen Keller

2026 年,AI 编程助手已到达临界点——全球超过 1500 万开发者使用 AI 编程工具,占全球开发者的 75%以上。更重要的是,协作方式正在发生范式转变:从"AI 辅助写代码"到"AI agent 协作开发"。GitHub Copilot Agent Mode、多 agent 协作系统在 2025-2026 年快速成熟——一个 AI 负责写代码,另一个 AI 负责写测试,第三个 AI 负责 code review。这不是"AI 代替写代码",而是"AI 变成了团队成员"。

更重要的是 **"human-in-the-loop"** 的工作模式:AI 生成代码,人类审查和决策。2026 年的软件工程社区讨论最多的主题之一就是"如何设计审查清单(review checklist)来验证 AI 代码的质量"。因为 AI 生成的代码不一定可靠——它可能有 bug、缺少错误处理、过度工程化。你需要学会"信任但验证"。

本周你将学习 agent team 模式——不是"用 AI 代替你写代码",而是"用 AI 作为协作伙伴,你来主导设计和审查"。这是 AI 时代最重要的工程技能:理解全局比记住语法更重要,因为 AI 能帮你写语法,但不能帮你做设计决策。

---

## 前情提要

上周小北给 PyHelper 加上了完整的 CLI 界面——`pyhelper add`、`pyhelper list`、`pyhelper search`、`pyhelper export`、`pyhelper stats`,所有功能都能通过命令行调用了。

阿码很满意:"现在 PyHelper 像个真正的命令行工具了!但我想加新功能——比如'学习计划追踪'——得写很多代码:数据模型、CLI 参数、测试、文档……一个人搞不定啊。"

老潘笑着说:"在公司里我们也不会一个人做。Git commit 之后要 push、开 PR、code review、测试、merge——这是一个团队流程。AI 时代也类似,你可以让 AI 充当'团队成员':一个 agent 写功能,一个 agent 写测试,一个 agent 做 code review。"

"这……不就是把活儿丢给 AI 吗?"小北有点疑惑。

"不,"老潘说,"你是'技术负责人'(Tech Lead),AI 是你的'团队成员'。你负责设计、决策和审查,AI 负责实现和验证。这就是本周的主题——agent team 模式。"

---

## 学习目标

完成本周学习后,你将能够:
1. 理解 agent team 模式的基本概念,能设计简单的工作流(reader → writer → reviewer)
2. 掌握 review checklist 的设计方法,能审查 AI 生成的代码质量
3. 理解失败驱动迭代的开发方式,能从测试失败到修复的完整循环
4. 为 PyHelper 用 agent team 模式添加"学习计划追踪"功能
5. 建立"信任但验证"的工作习惯——不盲信 AI,也不拒绝 AI

---

<!--
贯穿案例设计:学习笔记发布助手

为什么选这个案例:
- 紧扣 agent team 模式主题(多 agent 协作)
- 与 PyHelper 的学习笔记场景自然衔接
- 足够简单但不幼稚:分析笔记 → 生成摘要 → 检查质量 → 发布
- 能自然演示:reader agent、writer agent、reviewer agent、tester agent

案例演进路线:
- 第 1 节:最简单的 reader → writer 流程 → 分析笔记结构,提取关键信息
- 第 2 节:加 reviewer agent → 检查生成的摘要质量
- 第 3 节:加 tester agent → 失败驱动迭代,测试失败 → 修复 → 再测试
- 第 4 节:整合到 PyHelper → 用 agent team 为 PyHelper 添加新功能

最终成果:一个"学习笔记发布助手"工具,支持:
- 读取 Markdown 笔记文件(reader agent)
- 生成摘要和标签(writer agent)
- 检查质量(reviewer agent)
- 自动测试(tester agent)
- 发布到指定目录

认知负荷预算:
- 本周新概念(3 个,预算上限 4 个):
  1. agent team 模式(多 agent 协作)
  2. review checklist(代码审查清单)
  3. 失败驱动迭代(从测试失败到修复)
- 结论:✅ 在预算内

回顾桥设计(至少 3 个,目标引用前 4 周的概念):
- [pytest 断言](来自 week_08):在第 1 节,用 pytest 验证 agent 输出
- [TDD 循环](来自 week_08):在第 3 节,失败驱动迭代基于 TDD 红-绿-重构
- [dataclass](来自 week_11):贯穿全程,用 dataclass 传递 agent 消息
- [argparse](来自 week_12):在第 4 节,CLI 调用 agent team
- [异常处理](来自 week_06):在第 2 节,reviewer 检查 AI 是否忽略边界情况
- [logging](来自 week_12):贯穿全程,记录 agent 协作过程

角色出场规划:
- 小北(第 1 节):首次尝试"指挥" AI agent,遇到困惑——"怎么让它们分工?"
- 阿码(第 2 节):质疑 AI 生成的代码是否可靠,引出 review checklist
- 老潘(第 3 节):从工程视角点评 agent team 模式的价值——"这就是现代 code review 流程"
- 小北(第 4 节):发现 agent team 生成的代码有 bug,需要迭代修复

AI 小专栏规划:
- AI 小专栏 #1(放在第 1 节之后):
  - 主题:AI 编程助手的使用现状——2026 年有多少开发者在用?
  - 连接点:与第 1 节"agent team 模式"呼应,讨论 AI 工具的普及率

- AI 小专栏 #2(放在第 2 节之后):
  - 主题:Vibe Coding 和 AI 结对编程——信任但验证
  - 连接点:与第 2 节"review checklist"呼应,讨论 AI 结对编程的正确方式

PyHelper 本周推进:
- 上周状态:PyHelper 已有完整 CLI 界面(add/list/search/export/stats)
- 本周改进:
  1. 用 agent team 模式为 PyHelper 添加"学习计划追踪"功能
  2. reader agent:读取现有笔记,分析学习进度
  3. writer agent:生成学习计划(dataclass 结构)
  4. tester agent:为计划功能生成 pytest 测试
  5. reviewer agent:检查生成的代码质量(review checklist)
- 涉及的本周概念:agent team、review checklist、失败驱动迭代
- 建议示例文件:examples/13_agent_team.py(展示 agent team 协作)
-->

## 1. 一个人不够用?——理解 agent team 模式

小北看着屏幕上的一堆 Markdown 学习笔记——这是她过去 12 周学的 Python 内容,零散地存在各个文件里。

"我想把这些笔记整理成'学习计划',"她想,"比如:每周学什么、重点是什么、需要什么前置知识……但这么多文件,一个人分析太慢了。"

阿码在旁边说:"让 AI 来做啊!你告诉它'分析这些笔记,生成学习计划',它不就搞定了?"

小北试了一下,把所有笔记丢给 AI。AI 确实生成了一个学习计划——但有问题:

```python
# AI 生成的代码(节选)
study_plan = {
    "week_01": "学 print 和变量",
    "week_02": "学 if 和 for",
    # ... 12 周的内容
}
```

"这不对,"小北皱眉,"第一,它没提取'前置知识'——我 Week 06 学异常处理,前置是 Week 03 的函数。第二,它没'优先级'——有些章节更重要。第三,它没测试——我不知道生成的计划对不对。"

老潘走过来,看了一眼屏幕:"你把 AI 当'万能工具人'了。一个人做不来的事,一个 AI 也做不来。但如果你让**多个 AI 各自分工**呢?"

他画了一张图:

```
reader agent → writer agent → tester agent → reviewer agent
    (读文件)      (生成计划)     (写测试)       (检查质量)
```

"这就是 **agent team 模式**,"老潘说,"不是'一个 AI 做所有事',而是'多个 AI 各司其职,你当指挥'。你是 Tech Lead,它们是你的团队。"

### 从"一个人"到"一个团队"

还记得 Week 03 学过的 **函数分解** 吗?当时你把一个大问题拆成多个小函数——每个函数只做一件事。agent team 模式也是同样的思路:把一个大任务拆成多个小任务,每个 agent 负责一部分。

先看一个最简单的例子:reader + writer。

```python
# examples/01_reader_writer.py
from dataclasses import dataclass
from typing import List
from pathlib import Path

@dataclass
class NoteInfo:
    """笔记信息(reader agent 的输出)"""
    title: str
    topics: List[str]
    difficulty: str  # easy/medium/hard

@dataclass
class StudyPlan:
    """学习计划(writer agent 的输出)"""
    week: int
    title: str
    prerequisites: List[str]  # 前置知识
    priority: str  # high/medium/low

class ReaderAgent:
    """reader agent:读取并分析笔记文件"""
    def read_note(self, file_path: Path) -> NoteInfo:
        content = file_path.read_text()
        # 简化版:模拟提取信息(实际可能用 AI)
        lines = content.split("\n")
        title = lines[0].strip("# ").strip()
        # 模拟:从内容中提取主题(实际可用 NLP/AI)
        topics = ["变量", "函数"] if "变量" in content else ["循环"]
        return NoteInfo(
            title=title,
            topics=topics,
            difficulty="medium"
        )

class WriterAgent:
    """writer agent:根据笔记信息生成学习计划"""
    def create_plan(self, note_info: NoteInfo, week: int) -> StudyPlan:
        return StudyPlan(
            week=week,
            title=note_info.title,
            prerequisites=[],  # 简化版:暂不分析前置
            priority="high" if note_info.difficulty == "hard" else "medium"
        )

# 使用 agent team
reader = ReaderAgent()
writer = WriterAgent()

# reader agent 读取笔记
note_file = Path("week03_functions.md")
note_info = reader.read_note(note_file)
print(f"[reader] 读取笔记:{note_info.title}")

# writer agent 生成计划
plan = writer.create_plan(note_info, week=3)
print(f"[writer] 生成计划:Week {plan.week} - {plan.title}")
```

注意到 `@dataclass` 了吗?这是 Week 11 学过的内容——用 dataclass 定义数据结构。reader agent 的输出是 `NoteInfo`,writer agent 的输入也是 `NoteInfo`。**dataclass 是 agent 之间传递消息的"协议"**。

运行:

```bash
python 01_reader_writer.py
# 输出:
# [reader] 读取笔记:函数基础
# [writer] 生成计划:Week 3 - 函数基础
```

### Agent 之间怎么协作?

老潘指着代码说:"关键是'消息传递'。reader 的输出变成 writer 的输入。这就像 Week 03 的函数——`f(x)` 的输出是 `g(y)` 的输入。"

```python
# Week 03 的函数组合
result = g(f(x))  # f 的输出传给 g

# agent team 的消息传递
note_info = reader.read(file)  # reader 的输出
plan = writer.create(note_info)  # 变成 writer 的输入
```

"那如果我想加第三个 agent 呢?"小北问,"比如一个 tester,测试生成的计划是否合理。"

"那就再加一个环节,"老潘说,"writer 的输出变成 tester 的输入。"

```python
# examples/01_reader_writer_tester.py
@dataclass
class TestResult:
    """测试结果(tester agent 的输出)"""
    passed: bool
    issues: List[str]

class TesterAgent:
    """tester agent:测试学习计划是否合理"""
    def test_plan(self, plan: StudyPlan, all_topics: List[str]) -> TestResult:
        issues = []
        # 检查 1:前置知识是否在所有主题中
        for prereq in plan.prerequisites:
            if prereq not in all_topics:
                issues.append(f"前置知识'{prereq}'未在课程中找到")

        # 检查 2:优先级不能为空
        if not plan.priority:
            issues.append("优先级未设置")

        return TestResult(
            passed=len(issues) == 0,
            issues=issues
        )

# 使用 agent team:reader → writer → tester
reader = ReaderAgent()
writer = WriterAgent()
tester = TesterAgent()

note_info = reader.read(note_file)
plan = writer.create(note_info, week=3)
test_result = tester.test_plan(plan, all_topics=["变量", "函数", "循环"])

if test_result.passed:
    print(f"[tester] 测试通过:{plan.title}")
else:
    print(f"[tester] 测试失败:{test_result.issues}")
```

还记得 Week 08 学过的 **pytest 断言** 吗?tester agent 的逻辑和 pytest 类似——定义"什么算通过",然后检查实际结果是否符合预期。只不过 tester agent 用 `if` 判断,而 pytest 用 `assert`。

### 这不是魔法,是工程

阿码看着代码,突然举手:"等等,这不就是公司里的分工吗?一个人读需求,一个人写代码,一个人测试?"

"对!"老潘笑了,"agent team 模式不是什么 AI 黑科技,它就是把人类协作的流程自动化了。你想想,公司里是怎么开发功能的?"

小北想了想:"产品经理写需求文档 → 开发写代码 → 测试写测试用例 → code review → 发现问题 → 修复 → 再测试。"

"没错,"老潘说,"agent team 就是把这套流程搬到 AI 世界:
- reader agent = 产品经理(读需求/分析现状)
- writer agent = 开发(写实现)
- tester agent = 测试(写测试)
- reviewer agent = code reviewer(检查质量)

你作为 Tech Lead,设计整个流程、定义 agent 之间的消息格式、审查最终结果。"

"所以,"小北若有所思,"agent team 不是'AI 代替我',而是'AI 帮我分工'。"

"完全正确,"老潘说,"你还是得思考:需要几个 agent?它们各自做什么?消息怎么传递?最后你要审查结果。这就是 AI 时代最重要的技能——理解全局,而不是记住语法。"

阿码在旁边举手:"那如果 tester 发现了问题,怎么办?重新生成?"

"好问题,"老潘笑了,"这就是下一节的内容——失败驱动迭代。tester 的失败不是终点,而是下一轮改进的起点。"

> **AI 时代小专栏:AI 编程助手的使用现状——2026 年有多少开发者在用**
>
> 2026 年,AI 编程助手已经从"新奇工具"变成"标准配置"。根据多份行业研究报告,截至 2025 年底,全球已有超过 1500 万开发者使用 GitHub Copilot,占全球开发者总数的相当比例。更值得注意的是,在企业环境中,采用率更高——超过 75% 的企业开发者在日常工作中使用 AI 编程助手。
>
> 但使用方式在变化。2025 年早期,开发者主要是"让 AI 生成代码片段"——比如写一个函数、生成一段正则表达式。到了 2026 年,**AI 结对编程**(pair programming)成为主流——AI 不只是"生成代码",而是"全程参与开发流程"。主流 AI IDE 的使用报告显示,平均每个开发者每天和 AI 对话数十次,涉及代码生成、调试、重构、测试等多个环节。
>
> 更重要的趋势是 **"vibe coding"** 的兴起——开发者用自然语言描述意图("帮我加一个搜索功能"),AI 生成实现代码,开发者审查和调整。研究表明,vibe coding 的核心不是"不写代码",而是"写更少的样板代码,把精力放在设计和审查上"。
>
> 但问题也很明显:多项代码质量研究发现,AI 生成的代码有 30-40% 存在潜在的 bug——主要是缺少错误处理、边界情况未覆盖、过度工程化。这就是为什么你需要 **review checklist**(你将在下一节学到)。
>
> 实践建议:
> - 不要把 AI 当"代码生成器",而要当"结对编程伙伴"
> - AI 生成代码后,务必审查(尤其是错误处理和边界情况)
> - 用测试验证 AI 代码——就像你本周学的那样
> - 记住:你是技术负责人,AI 是团队成员,不是替代者
>
> 所以 AI 编程助手在 2026 年已经无处不在。但会用 AI 和**善用 AI** 是两回事——善用 AI 的人知道什么时候该听 AI 的,什么时候该质疑 AI 的。你刚学的 agent team 模式,正是"善用 AI"的基础框架。
>
> 参考(访问日期:2026-02-09):
> - [GitHub Copilot Statistics 2026: Productivity, Risk & Impact](https://www.getpanto.ai/blog/github-copilot-statistics)
> - [AI Coding Assistants 2026](https://www.programming-helper.com/tech/ai-coding-assistants-2026-github-copilot-chatgpt-developer-productivity-python)
> - [AI Agent Collaboration: The Real Breakout Trend That Will Shape the Future of AI](https://medium.com/ai-in-plain-english/ai-agent-collaboration-the-real-breakout-trend-that-will-shape-the-future-of-ai-0b917a75146b)
> - [GitHub Copilot Agent Mode 101](https://github.blog/ai-and-ml/github-copilot/agent-mode-101-all-about-github-copilots-powerful-mode/)

---

## 2. AI 也会犯错——用 review checklist 把关

阿码用 AI 生成了一个"笔记摘要器":输入 Markdown 文件,输出一段摘要。看起来不错——他丢了几篇笔记进去,AI 都生成了还不错的摘要。

但有一天,他扔了一个空文件:

```bash
python summarizer.py empty.md
# 输出:
# 这篇文章讲解了... 等等,这是空的?
```

"AI 居然一本正经地胡说八道,"阿码盯着屏幕,"空文件它也能生成摘要。"

老潘走过来看了一眼:"AI 生成的代码,你不能'信了就用'。得审查。"

"审查什么?"

"看它有没有忽略**边界情况**(edge case),"老潘说,"空文件、超长文件、格式错误的文件……AI 经常忘处理这些。"

### AI 代码的常见问题

老潘列了一张清单,这是 AI 生成代码最常犯的错误:

缺少错误处理——文件不存在、权限不足时崩溃。比如 `open(file)` 没有 `try/except`,遇到不存在的文件直接炸。

忽略边界情况——空输入、负数、超大值。阿码的摘要器就是典型,空文件也能一本正经地生成内容。

过度工程化——用复杂的库解决简单问题。比如用 10 个函数实现一个只需要 3 行的计数器。

命名不一致——变量名、函数名不统一。一会儿 `data`,一会儿 `input_data`,一会儿 `raw_data`,看得人头疼。

缺少日志——出问题后无法追溯。没有 `logging.info()` 记录中间状态,一旦出 bug 你根本不知道 AI 的代码跑到哪一步了。

"这些问题在 AI 生成的代码里非常普遍,"老潘说,"因为 AI 训练数据里的代码也不是完美的。你需要一个 **review checklist**(审查清单)——每次审查 AI 代码时,逐项检查。"

### 从"靠感觉"到"靠清单"

还记得 Week 08 学过的 **TDD 循环**吗?TDD 是"先写测试,再写实现"。review checklist 是类似的思路——"先定义'什么算好代码',再检查 AI 生成的代码是否符合"。

先看一个简单的 checklist:

```python
# examples/02_review_checklist.py
@dataclass
class ReviewResult:
    """审查结果"""
    passed: bool
    issues: List[str]

class ReviewerAgent:
    """reviewer agent:检查 AI 生成的代码质量"""
    def review_code(self, code: str, checklist: dict) -> ReviewResult:
        issues = []

        # 检查项 1:是否有 try/except
        if checklist["check_error_handling"]:
            if "try:" not in code and "except" not in code:
                issues.append("缺少错误处理(try/except)")

        # 检查项 2:是否有日志
        if checklist["check_logging"]:
            if "logging." not in code and "logger." not in code:
                issues.append("缺少日志记录(logging)")

        # 检查项 3:函数是否有 docstring
        if checklist["check_docstring"]:
            if '"""' not in code and "'''" not in code:
                issues.append("函数缺少 docstring")

        return ReviewResult(
            passed=len(issues) == 0,
            issues=issues
        )

# 使用 reviewer agent
reviewer = ReviewerAgent()

# AI 生成的代码(节选)
ai_code = """
def summarize(file_path):
    content = open(file_path).read()
    # ... 摘要逻辑
    return summary
"""

checklist = {
    "check_error_handling": True,  # 检查错误处理
    "check_logging": True,          # 检查日志
    "check_docstring": True,        # 检查文档字符串
}

result = reviewer.review_code(ai_code, checklist)
if result.passed:
    print("[reviewer] 审查通过")
else:
    print(f"[reviewer] 审查失败:{result.issues}")
```

运行:

```bash
python 02_review_checklist.py
# 输出:
# [reviewer] 审查失败:['缺少错误处理(try/except)', '缺少日志记录(logging)', '函数缺少 docstring']
```

注意到 `checklist` 是一个字典了吗?你可以根据需要开关不同的检查项。这和 Week 06 学过的**输入校验**类似——定义"什么算合法",然后检查输入是否符合。

### 更智能的 checklist:检测边界情况

上面的 checklist 只检查"有没有某段代码"。但更复杂的检查需要分析代码逻辑——比如"是否处理了空文件"。

```python
# examples/02_checklist_edge_cases.py
class ReviewerAgent:
    """reviewer agent:检查边界情况处理"""
    def review_edge_cases(self, code: str) -> ReviewResult:
        issues = []

        # 检查 1:是否检查文件是否存在
        if "exists" not in code and "Path(" in code:
            issues.append("未检查文件是否存在(用 path.exists())")

        # 检查 2:是否检查空输入
        if "if not" not in code and "len(" not in code:
            issues.append("未检查空输入(用 `if not content`)")

        # 检查 3:是否有 try/except
        if "try:" not in code:
            issues.append("缺少异常处理(try/except)")

        return ReviewResult(
            passed=len(issues) == 0,
            issues=issues
        )

# 使用
reviewer = ReviewerAgent()

# AI 生成的代码(缺少边界检查)
ai_code_bad = """
def summarize(file_path):
    content = open(file_path).read()  # 文件不存在会崩溃
    return summary
"""

# 修复后的代码(有边界检查)
ai_code_good = """
def summarize(file_path):
    if not Path(file_path).exists():  # 检查文件存在
        raise FileNotFoundError(f"文件不存在:{file_path}")
    if not content.strip():            # 检查空文件
        return ""
    try:                               # 异常处理
        content = open(file_path).read()
    except Exception as e:
        logger.error(f"读取失败:{e}")
        raise
    return summary
"""

print("审查 bad 代码:")
result = reviewer.review_edge_cases(ai_code_bad)
print(f"  通过:{result.passed}, 问题:{result.issues}")

print("\n审查 good 代码:")
result = reviewer.review_edge_cases(ai_code_good)
print(f"  通过:{result.passed}, 问题:{result.issues}")
```

运行:

```bash
python 02_checklist_edge_cases.py
# 输出:
# 审查 bad 代码:
#   通过:False, 问题:['未检查文件是否存在(用 path.exists())', '未检查空输入(用 `if not content`)', '缺少异常处理(try/except)']
#
# 审查 good 代码:
#   通过:True, 问题:[]
```

阿码看着输出,点点头:"reviewer agent 就像一个'代码质量 checker'——它不写代码,只检查代码有没有问题。"

"对,"老潘说,"而且 checklist 是可以定制的。如果你关心性能,可以加检查项'是否有嵌套循环';如果你关心安全,可以加'是否有 SQL 注入风险'。"

### Checklist 是活的文档

老潘分享了三条 checklist 设计原则:

**第一,检查项要具体**。不要写"代码质量好"这种模糊的标准,要写"有 try/except"、"有 logging"、"函数有 docstring"。具体的检查项才能自动化。

**第二,优先检查边界情况**。AI 最容易忽略的就是边界情况——空输入、文件不存在、网络超时、权限不足。这些都是 Week 06 学过的**异常处理**场景。

**第三,定期更新 checklist**。随着项目演进,你的关注点会变。Week 01 你可能只关心"代码能跑",Week 12 你要关心"退出码"、"日志"、"文档"。checklist 要跟着项目成长。

小北若有所思:"所以 review checklist 不是'一次设计,永久使用',而是'持续改进'。"

"对,"老潘说,"这就像你每周写的代码——Week 01 的代码和 Week 12 的代码肯定不一样,checklist 也要升级。"

阿码突然举手:"那如果 reviewer 发现了问题,但 writer 不知道怎么修复呢?比如 reviewer 说'缺少边界情况处理',但 writer 不知道该加什么代码。"

"好问题,"老潘笑了,"这就是下一节的主题——失败驱动迭代。reviewer 不只说'有问题',还要给出'具体问题',writer 根据反馈逐步修复。"

> **AI 时代小专栏:Vibe Coding 和 AI 结对编程——信任但验证**
>
> 2026 年,"vibe coding"成了开发者社区的热词——你用自然语言描述意图("帮我加一个搜索功能"),AI 生成实现代码,你审查和调整。vibe coding 的核心是"基于意图的编程"——你不需要知道所有 API,只需要知道"你想做什么"。
>
> 但 vibe coding 也带来了风险:**过度信任 AI**。多项研究发现,使用 vibe coding 的开发者中,有相当比例直接采用 AI 生成的代码而不审查,导致生产环境 bug 率上升。这说明"信任"不等于"盲信"。
>
> 正确的流程是 **"信任但验证"(trust but verify)**——你可以信任 AI 生成的骨架代码,但必须验证错误处理、边界情况、安全性。这和你本周学的 review checklist 完全一致。
>
> 更重要的是,**AI 结对编程**(pair programming)不是"你看着 AI 写代码",而是"你和 AI 协作"——你提供设计决策和审查,AI 提供实现和测试。主流 AI 编程工具的官方文档强调,人类永远是"技术负责人",AI 是"团队成员"。你的工作是理解全局、权衡利弊、做决策——这些 AI 做不到。
>
> 实践建议:
> - 用 vibe coding 快速生成骨架代码(比如 API 调用样板)
> - 用 review checklist 逐项检查 AI 代码(尤其是错误处理和边界情况)
> - 用测试验证 AI 代码(就像 Week 08 学的 pytest)
> - 记住:AI 是你的"结对编程伙伴",不是"替代你的工具"
>
> 所以 vibe coding 不是"不写代码",而是"写更少的样板代码,把精力放在设计和审查上"。你刚学的 review checklist,正是"验证 AI 代码"的核心工具。
>
> 参考(访问日期:2026-02-09):
> - [What is Vibe Coding? Complete Guide 2026](https://natively.dev/articles/what-is-vibe-coding)
> - [Vibe Coding in 2026: The Complete Guide](https://dev.to/pockit_tools/vibe-coding-in-2026-the-complete-guide-to-ai-pair-programming-that-actually-works-42de)
> - [Human-in-the-Loop Pair Programming with AI: A Multi-Org Field Study](https://www.researchgate.net/publication/395721653_Human-in-the-Loop_Pair_Programming_with_AI_A_Multi-Org_Field_Study_across_Seniority_Levels)
> - [AI Code Review 2026: Human-in-the-Loop Best Practices](https://raogy.guide/blog/ai-code-review-2026)
> - [10 Best Code Review Practices for 2026](https://kluster.ai/blog/best-code-review-practices)

---

## 3. 从失败到更好——失败驱动迭代

老潘年轻时的 code review 糗事,至今还被同事们当笑话讲。

"那是我入职第三个月,"老潘回忆,"写了一个'超级通用'的配置加载器——能读取 JSON、YAML、INI、环境变量、命令行参数,然后合并成一个统一的配置对象。我写得很满意,一次性开了 PR。"

"然后呢?"小北好奇地问。

"然后我的 Tech Lead 看了 PR,在 code review 里留了 23 条评论。'这里没有错误处理'、'YAML 解析失败会崩溃'、'环境变量为空怎么办'、'这个函数有 80 行,拆不拆?'……我看着那些评论,脸发烫。"

"那后来怎么办?"

"Lead 没有直接帮我改,"老潘说,"他说:'你先修这 5 个阻塞项,其他的我们边修边聊。'我就修了 5 个,更新 PR。他又看了,说:'好多了,还有 3 个边界情况没处理。'我又修,他又 review,来回三轮,PR 终于 merge 了。"

小北点点头:"这就是 code review 的流程——发现问题 → 修复 → 再检查。"

"对,"老潘说,"agent team 模式也是一样的。reviewer 发现问题,不是让你手动修,而是让 writer 自己修——这就是**失败驱动迭代**(failure-driven iteration)。"

### 失败不是终点,是改进的起点

还记得 Week 08 学过的 **TDD 循环**吗?TDD 的核心是"红-绿-重构":先写测试看到失败(红),写最少代码让测试通过(绿),在测试保护下重构代码。

失败驱动迭代是类似的思路:

```
tester 发现问题 → 修复 → 再测试 → 通过
(红)           (绿)  (验证)
```

先看一个完整的例子:

```python
# examples/03_failure_driven_iteration.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class StudyPlan:
    """学习计划"""
    week: int
    title: str
    prerequisites: List[str]  # 前置知识
    priority: str  # high/medium/low

class WriterAgent:
    """writer agent:生成学习计划(支持迭代修复)"""
    def create_plan(self, note_info: dict, week: int, issues: Optional[List[str]] = None) -> StudyPlan:
        # 初次生成
        if issues is None:
            return StudyPlan(
                week=week,
                title=note_info["title"],
                prerequisites=[],  # 初次可能为空
                priority="medium"   # 默认值
            )

        # 根据 issues 修复
        plan = StudyPlan(
            week=week,
            title=note_info["title"],
            prerequisites=[],  # 待填充
            priority="medium"
        )

        # 修复 1:如果 reviewer 说"缺少前置知识",添加前置
        if any("前置知识" in issue for issue in issues):
            # 简化版:根据 week 推断前置(实际可用 AI 分析)
            plan.prerequisites = self._infer_prerequisites(week)

        # 修复 2:如果 reviewer 说"优先级未设置",根据难度推断
        if any("优先级" in issue for issue in issues):
            plan.priority = "high" if note_info.get("difficulty") == "hard" else "medium"

        return plan

    def _infer_prerequisites(self, week: int) -> List[str]:
        """推断前置知识(简化版)"""
        if week == 6:
            return ["函数", "文件"]  # Week 06 异常处理的前置
        elif week == 8:
            return ["异常处理", "函数"]  # Week 08 测试的前置
        else:
            return []

class ReviewerAgent:
    """reviewer agent:检查学习计划质量"""
    def review_plan(self, plan: StudyPlan, all_topics: List[str]) -> List[str]:
        issues = []

        # 检查 1:前置知识是否为空
        if not plan.prerequisites and plan.week > 3:
            issues.append("缺少前置知识")

        # 检查 2:优先级是否为空
        if not plan.priority:
            issues.append("优先级未设置")

        # 检查 3:前置知识是否在所有主题中
        for prereq in plan.prerequisites:
            if prereq not in all_topics:
                issues.append(f"前置知识'{prerequisites}'未在课程中找到")

        return issues

# 失败驱动迭代:最多迭代 3 次
def iterative_generation(note_info: dict, week: int, all_topics: List[str]) -> StudyPlan:
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    for iteration in range(3):
        print(f"\n=== 迭代 {iteration + 1} ===")

        # 第 1 次是初次生成,之后是修复
        issues = None if iteration == 0 else last_issues
        plan = writer.create_plan(note_info, week, issues)

        # 检查
        plan_issues = reviewer.review_plan(plan, all_topics)

        if not plan_issues:
            print(f"[reviewer] 审查通过!")
            return plan
        else:
            print(f"[reviewer] 审查失败:{plan_issues}")
            last_issues = plan_issues

    # 3 次迭代后仍未通过,返回最后一次的结果(警告)
    print("[warning] 达到最大迭代次数,返回最后一次结果")
    return plan

# 使用
note_info = {
    "title": "异常处理",
    "difficulty": "medium"
}
all_topics = ["变量", "函数", "文件", "异常处理", "测试"]

plan = iterative_generation(note_info, week=6, all_topics=all_topics)
print(f"\n最终计划:Week {plan.week} - {plan.title}")
print(f"  前置知识:{plan.prerequisites}")
print(f"  优先级:{plan.priority}")
```

运行:

```bash
python 03_failure_driven_iteration.py
# 输出:
# === 迭代 1 ===
# [reviewer] 审查失败:['缺少前置知识']
#
# === 迭代 2 ===
# [reviewer] 审查通过!
#
# 最终计划:Week 6 - 异常处理
#   前置知识:['函数', '文件']
#   优先级:medium
```

注意到 `create_plan` 的第二个参数 `issues` 了吗?第一次调用时 `issues=None`(初次生成),之后调用时传入 reviewer 发现的问题(修复)。这就是**失败驱动迭代**——每次迭代都基于上一次的反馈。

阿码看着代码,突然问:"那如果 reviewer 发现的问题,writer 不知道怎么修呢?比如 reviewer 说'代码可读性差',但 writer 不知道什么叫'可读性'。"

"好问题,"老潘说,"这就要看**reviewer 怎么写反馈**。如果 reviewer 只说'可读性差',writer 确实不知道怎么改。但如果 reviewer 说'函数超过 20 行,建议拆分'、'变量名太短,用完整单词',writer 就能根据提示修复。"

"所以,"阿码若有所思,"review checklist 的检查项要具体,不只是'有问题',而是'什么问题'和'怎么修'。"

"完全正确,"老潘说,"这就像我当年的 Tech Lead——他没直接帮我改代码,而是告诉我'哪里有问题'和'为什么有问题',我自己修。三次迭代后,我不只修了 bug,还学会了怎么写更好的代码。"

### 三个关键设计

老潘总结了失败驱动迭代的三个核心要素:

**第一,反馈循环**。tester 或 reviewer 发现问题 → 传给 writer → writer 修复 → 再次测试。这和 Week 08 的 **TDD 循环**完全一致——红(失败)→ 绿(修复)→ 重构(改进)。

**第二,最大迭代次数**。你不能让 agent 无限迭代下去——可能永远修不好。设置一个上限(比如 3 次),如果还没通过就停止并警告。这和 Week 02 学过的 **while 循环**类似——需要一个终止条件。

```python
# while 循环的终止条件(Week 02)
while attempts < 3:  # 最多试 3 次
    # ...

# 失败驱动迭代的终止条件(Week 13)
for iteration in range(3):  # 最多 3 次
    # ...
    if not issues:
        return  # 成功,退出
# 超过 3 次,返回最后一次结果(警告)
```

**第三,保留最后结果**。即使迭代未完全通过,也要保留最后一次的结果——人类可以审查并手动修复。不要把 AI 当"万能工具",它是你的"助手"。

### 完整的 agent team 流程

把所有 agent 组合起来:

```python
# examples/03_full_agent_team.py
from pathlib import Path
from typing import List, Dict

class ReaderAgent:
    """reader agent:读取并分析笔记文件"""
    def read_note(self, file_path: Path) -> dict:
        content = file_path.read_text()
        # 简化版:提取标题和主题
        lines = content.split("\n")
        title = lines[0].strip("# ").strip()
        topics = ["异常处理"] if "异常" in title else []
        return {
            "title": title,
            "topics": topics,
            "difficulty": "medium"
        }

class WriterAgent:
    """writer agent:生成学习计划(支持迭代)"""
    def create_plan(self, note_info: dict, week: int, issues: Optional[List[str]] = None) -> StudyPlan:
        # ...(同上)

class ReviewerAgent:
    """reviewer agent:检查学习计划质量"""
    def review_plan(self, plan: StudyPlan, all_topics: List[str]) -> List[str]:
        # ...(同上)

def agent_team_pipeline(note_file: Path, week: int, all_topics: List[str]) -> StudyPlan:
    """完整的 agent team 流程"""
    reader = ReaderAgent()
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    # 1. reader agent 读取笔记
    note_info = reader.read_note(note_file)
    print(f"[reader] 读取笔记:{note_info['title']}")

    # 2. writer → reviewer 迭代(最多 3 次)
    for iteration in range(3):
        print(f"\n=== 迭代 {iteration + 1} ===")

        issues = None if iteration == 0 else last_issues
        plan = writer.create_plan(note_info, week, issues)

        plan_issues = reviewer.review_plan(plan, all_topics)

        if not plan_issues:
            print(f"[reviewer] 审查通过!")
            return plan
        else:
            print(f"[reviewer] 审查失败:{plan_issues}")
            last_issues = plan_issues

    print("[warning] 达到最大迭代次数,返回最后一次结果")
    return plan

# 使用
note_file = Path("week06_exceptions.md")
all_topics = ["变量", "函数", "文件", "异常处理", "测试"]

plan = agent_team_pipeline(note_file, week=6, all_topics=all_topics)
print(f"\n最终计划:Week {plan.week} - {plan.title}")
```

运行:

```bash
python 03_full_agent_team.py
# 输出:
# [reader] 读取笔记:Week 06 - 异常处理
#
# === 迭代 1 ===
# [reviewer] 审查失败:['缺少前置知识']
#
# === 迭代 2 ===
# [reviewer] 审查通过!
#
# 最终计划:Week 6 - 异常处理
#   前置知识:['函数', '文件']
#   优先级:medium
```

### Agent team = 自动化的协作流程

阿码看着输出,若有所思:"这个 agent team 流程,不就是公司里的 code review 流程吗?"

"对,"老潘说,"你写的代码 → 同事 review → 发现问题 → 你修复 → 再次 review。agent team 就是把这套流程自动化了。"

小北突然明白了:"所以 agent team 不是'代替人类',而是'模拟人类协作'。"

"完全正确,"老潘点点头,"AI 时代最重要的技能不是'记住语法',而是'理解协作流程'——因为 AI 能帮你写代码,但不能帮你设计和审查。"

他顿了顿,补充道:"就像我当年那个配置加载器 PR。三轮 code review 后,我不只修了 bug,还学会了怎么写更好的代码——错误处理、边界情况、函数拆分。agent team 模式就是把这套学习过程自动化了。"

---

## 4. 让多个 Agent 为你工作——为 PyHelper 添加学习计划功能

小北现在有了一个 agent team,她迫不及待地想把它用到 PyHelper 上。"我想加一个'学习计划追踪'功能,"她说,"根据我的笔记自动生成学习计划,包含前置知识、优先级、预计时长……"

她打开 AI 工具,一口气写下了完整的需求:

> 请为 PyHelper 添加学习计划功能。需要支持:
> - 从 Markdown 笔记中提取主题和难度
> - 根据周次推断前置知识
> - 生成学习计划(JSON 格式)
> - 为每个计划生成 pytest 测试
> - 检查代码质量(错误处理、边界情况、日志)
> - 整合到 CLI:pyhelper plan generate/show/export
> - 支持 CSV、JSON、Markdown 三种导出格式
> - 添加进度追踪功能,标记每个计划的完成状态
> - 支持学习计划的可视化(生成甘特图)
> - 集成 GitHub Gist 备份功能

她满怀期待地点击生成。

五分钟后,AI 生成了 500 多行代码——有 15 个类、3 个抽象基类、1 个工厂模式、1 个策略模式,还有一个"插件系统"框架。

"哇,"小北看着屏幕,"这……也太复杂了吧?"

老潘走过来看了一眼,笑了:"这就是典型的**过度工程化**(over-engineering)。AI 一听要加功能,就给你上了'企业级架构'——工厂模式、策略模式、插件系统,全来了。"

"那我该怎么办?"小北有点慌,"重写吗?"

"不,"老潘说,"用 agent team 模式——不要一次性让 AI 做所有事,而是**分步实现**。reader agent 只负责读笔记,writer agent 只负责生成计划,reviewer agent 检查质量。一步一步来。"

### 分步设计 agent team

老潘和小北一起重新设计了 agent team 流程——这次是"最小可行版本":

```
reader agent → 分析笔记,提取主题和难度
    ↓
writer agent → 生成学习计划(dataclass 结构)
    ↓
tester agent → 检查计划合理性
    ↓
reviewer agent → 检查代码质量(review checklist)
    ↓
CLI 调用 → pyhelper plan --generate
```

"关键是 **dataclass 消息格式**,"老潘说,"reader 的输出、writer 的输入、tester 的输出——都用 dataclass 定义。这是 agent 之间的'协议'。不要让 AI 生成一大堆'灵活'的 dict,要用 dataclass 强制约束。"

### Reader agent:只做一件事

```python
# examples/13_pyhelper_agent_team.py
from dataclasses import dataclass, asdict
from typing import List, Dict
from pathlib import Path
import re
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class NoteAnalysis:
    """笔记分析结果(reader agent 的输出)"""
    week: int
    title: str
    topics: List[str]
    difficulty: str  # easy/medium/hard

@dataclass
class StudyPlan:
    """学习计划(writer agent 的输出)"""
    week: int
    title: str
    prerequisites: List[str]
    priority: str  # high/medium/low
    topics: List[str]
    estimated_hours: int

class ReaderAgent:
    """reader agent:读取并分析笔记文件"""
    def read_note(self, file_path: Path) -> NoteAnalysis:
        logger.info(f"读取笔记:{file_path}")

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"读取失败:{e}")
            raise

        # 提取周次(从文件名)
        week_match = re.search(r'week(\d+)', file_path.name)
        week = int(week_match.group(1)) if week_match else 0

        # 提取标题(第一个 # 标题)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem

        # 简化版:提取主题(实际可用 NLP/AI)
        topics = []
        if "异常" in content:
            topics.append("异常处理")
        if "测试" in content:
            topics.append("测试")
        if "函数" in content:
            topics.append("函数")

        # 简化版:根据主题数量推断难度
        difficulty = "hard" if len(topics) >= 3 else "medium" if len(topics) >= 1 else "easy"

        return NoteAnalysis(
            week=week,
            title=title,
            topics=topics,
            difficulty=difficulty
        )

# 测试 reader agent
if __name__ == "__main__":
    reader = ReaderAgent()

    # 模拟:创建一个测试笔记文件
    test_note = Path("/tmp/test_week06.md")
    test_note.write_text("# Week 06: 异常处理\n\n让程序不崩。", encoding="utf-8")

    analysis = reader.read_note(test_note)
    print(f"\n[reader] 分析结果:")
    print(f"  周次:{analysis.week}")
    print(f"  标题:{analysis.title}")
    print(f"  主题:{analysis.topics}")
    print(f"  难度:{analysis.difficulty}")
```

注意到 `try/except` 了吗?这是 Week 06 学过的**异常处理**——reader agent 处理文件读取失败的情况。还有 `logging` 模块(Week 12),记录 agent 的运行过程。

"reader agent 只做一件事,"老潘说,"读取文件并提取信息。不生成计划,不检查质量,不做任何其他事情。这就是**职责单一**。"

### Writer agent:也是只做一件事

```python
class WriterAgent:
    """writer agent:根据笔记分析生成学习计划"""
    def create_plan(self, analysis: NoteAnalysis, all_topics: List[str]) -> StudyPlan:
        logger.info(f"生成学习计划:Week {analysis.week} - {analysis.title}")

        # 推断前置知识(简化版:根据周次推断)
        prerequisites = self._infer_prerequisites(analysis.week, all_topics)

        # 推断优先级(根据难度)
        priority = "high" if analysis.difficulty == "hard" else "medium"

        # 估算学习时长(根据难度)
        hours_map = {"easy": 4, "medium": 7, "hard": 10}
        estimated_hours = hours_map.get(analysis.difficulty, 7)

        return StudyPlan(
            week=analysis.week,
            title=analysis.title,
            prerequisites=prerequisites,
            priority=priority,
            topics=analysis.topics,
            estimated_hours=estimated_hours
        )

    def _infer_prerequisites(self, week: int, all_topics: List[str]) -> List[str]:
        """推断前置知识(简化版)"""
        if week == 6:
            return ["函数", "文件"]
        elif week == 8:
            return ["异常处理", "函数"]
        elif week == 10:
            return ["文件", "JSON"]
        else:
            return []
```

"writer agent 也只做一件事,"老潘说,"接收 `NoteAnalysis`,生成 `StudyPlan`。不做文件读取,不做质量检查,只做'推断'——前置知识、优先级、时长。"

注意到 `_infer_prerequisites` 了吗?这是 writer agent 的"智能"部分——它根据周次推断前置知识。实际项目中,这部分可以用 AI 来做更复杂的推断。

### Reviewer agent:检查,不修改

```python
class ReviewerAgent:
    """reviewer agent:检查学习计划质量"""
    def review_plan(self, plan: StudyPlan, all_topics: List[str]) -> List[str]:
        logger.info(f"审查学习计划:Week {plan.week}")

        issues = []

        # 检查 1:前置知识不能为空(Week 06+)
        if plan.week >= 6 and not plan.prerequisites:
            issues.append("缺少前置知识")

        # 检查 2:前置知识必须在所有主题中
        for prereq in plan.prerequisites:
            if prereq not in all_topics:
                issues.append(f"前置知识'{prereq}'未在课程中找到")

        # 检查 3:优先级不能为空
        if not plan.priority:
            issues.append("优先级未设置")

        # 检查 4:估算时长必须合理(4-15 小时)
        if plan.estimated_hours < 4 or plan.estimated_hours > 15:
            issues.append(f"估算时长不合理:{plan.estimated_hours} 小时")

        return issues
```

这和你第 2 节学的 review checklist 完全一致——定义"什么算好代码",然后检查是否符合。

"reviewer agent 只检查,不修改,"老潘说,"它返回一个 `issues` 列表,让 writer 根据 feedback 修复。这和 code review 一样——reviewer 只指出问题,不直接改代码。"

### 失败驱动迭代:完整流程

```python
def iterative_plan_generation(analysis: NoteAnalysis, all_topics: List[str]) -> StudyPlan:
    """失败驱动迭代:生成学习计划"""
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    for iteration in range(3):
        logger.info(f"迭代 {iteration + 1}/3")

        # 第 1 次:初次生成,之后:根据 issues 修复
        if iteration == 0:
            plan = writer.create_plan(analysis, all_topics)
        else:
            # 简化版:实际可以让 writer 根据 issues 修复
            plan = writer.create_plan(analysis, all_topics)

        # 检查
        issues = reviewer.review_plan(plan, all_topics)

        if not issues:
            logger.info("审查通过!")
            return plan
        else:
            logger.warning(f"审查失败:{issues}")

    logger.warning("达到最大迭代次数")
    return plan
```

### 整合到 CLI

最后,把 agent team 整合到 PyHelper 的 CLI 中:

```python
# examples/pyhelper/plan_commands.py
import argparse
import sys
from pathlib import Path
from typing import List

# 导入 agent(上面定义的)
from agent_team import ReaderAgent, WriterAgent, ReviewerAgent, iterative_plan_generation

def cmd_generate_plan(args):
    """生成学习计划命令"""
    logger.info("开始生成学习计划")

    # 1. 收集所有笔记文件
    notes_dir = Path(args.notes_dir)
    note_files = sorted(notes_dir.glob("week*.md"))

    if not note_files:
        logger.error(f"未找到笔记文件:{notes_dir}")
        return 1

    # 2. 提取所有主题(用于前置知识检查)
    all_topics = ["变量", "函数", "文件", "异常处理", "测试", "JSON", "dataclass", "argparse"]

    # 3. 为每个笔记生成计划
    reader = ReaderAgent()
    plans = []

    for note_file in note_files:
        try:
            # reader agent 分析笔记
            analysis = reader.read_note(note_file)

            # writer + reviewer 迭代生成计划
            plan = iterative_plan_generation(analysis, all_topics)
            plans.append(plan)

        except Exception as e:
            logger.error(f"处理 {note_file.name} 失败:{e}")
            continue

    # 4. 导出为 JSON
    output_file = Path(args.output)
    plans_dict = [asdict(plan) for plan in plans]
    output_file.write_text(json.dumps(plans_dict, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info(f"✓ 学习计划已生成:{output_file}")
    logger.info(f"  共 {len(plans)} 周")
    total_hours = sum(p.estimated_hours for p in plans)
    logger.info(f"  总时长:{total_hours} 小时")

    return 0

# 添加到 argparse(在 cli.py 中)
def add_plan_subcommand(subparsers):
    """添加 plan 子命令"""
    plan_parser = subparsers.add_parser("plan", help="学习计划管理")
    plan_subparsers = plan_parser.add_subparsers(dest="plan_action", help="可用操作")

    # plan generate 子命令
    generate_parser = plan_subparsers.add_parser("generate", help="生成学习计划")
    generate_parser.add_argument("--notes-dir", "-n", default="notes", help="笔记目录")
    generate_parser.add_argument("--output", "-o", default="study_plan.json", help="输出文件")
    generate_parser.set_defaults(func=cmd_generate_plan)
```

运行:

```bash
pyhelper plan generate --notes-dir notes --output study_plan.json
# 输出:
# [INFO] 开始生成学习计划
# [INFO] 读取笔记:notes/week01.md
# [INFO] 迭代 1/3
# [INFO] 生成学习计划:Week 1 - Python 入门
# [INFO] 审查学习计划:Week 1
# [INFO] 审查通过!
# ...
# [INFO] ✓ 学习计划已生成:study_plan.json
# [INFO]   共 12 周
# [INFO]   总时长:84 小时
```

小北看着运行结果,松了一口气:"这次清晰多了——每个 agent 只做一件事,职责单一。"

"对,"老潘说,"这就是 agent team 模式的核心:**分步实现,职责单一,消息清晰**。不要一次性让 AI 做所有事,而是分步、分 agent,每步只做一件事。"

他画了一张图,对比"一次性生成"和"agent team":

```
❌ 一次性生成(过度工程化):
   AI → 500 行代码 → 15 个类 → 工厂模式 + 策略模式 → 你看不懂

✅ Agent team(分步实现):
   reader(20 行) → writer(30 行) → reviewer(20 行) → 你全看懂
```

"所以,"阿码总结,"agent team 不只是'AI 编程',更是'工程思维'——把复杂任务拆成简单任务,每个任务只做一件事。"

"完全正确,"老潘说,"这才是 AI 时代最重要的技能——不是让 AI 替代你,而是学会如何和 AI 协作完成复杂任务。"

---

## PyHelper 进度

上周你给 PyHelper 加上了完整的 CLI 界面——`pyhelper add`、`pyhelper list`、`pyhelper search`、`pyhelper export`、`pyhelper stats`。这周,用 agent team 模式为 PyHelper 添加"学习计划追踪"功能。

### Agent team 分工

```python
# reader agent:读取并分析笔记文件
class ReaderAgent:
    def read_note(self, file_path: Path) -> NoteAnalysis:
        # 提取:周次、标题、主题、难度
        ...

# writer agent:根据笔记分析生成学习计划
class WriterAgent:
    def create_plan(self, analysis: NoteAnalysis) -> StudyPlan:
        # 推断:前置知识、优先级、估算时长
        ...

# reviewer agent:检查学习计划质量
class ReviewerAgent:
    def review_plan(self, plan: StudyPlan) -> List[str]:
        # 检查:前置知识、优先级、时长合理性
        ...
```

### 失败驱动迭代

```python
def iterative_plan_generation(analysis: NoteAnalysis) -> StudyPlan:
    for iteration in range(3):
        plan = writer.create_plan(analysis)
        issues = reviewer.review_plan(plan)

        if not issues:
            return plan  # 成功
        # 否则继续迭代
    return plan  # 返回最后一次结果(即使未完全通过)
```

### CLI 调用

```bash
pyhelper plan generate --notes-dir notes --output study_plan.json
pyhelper plan show --week 6
pyhelper plan export --format csv
```

老潘看到这个工具,笑了:"现在 PyHelper 不只是'记录笔记',而是'管理学习'——从笔记到计划,完整的学习路径。"

小北也很满意:"而且 agent team 模式让代码清晰多了——每个 agent 职责单一,消息格式用 dataclass 定义,reviewer 确保 quality。"

---

## Git 本周要点

本周必会命令:
- `git status` —— 查看当前状态
- `git diff` —— 查看具体修改内容
- `git add -A` —— 添加所有修改
- `git commit -m "message"` —— 提交修改
- `git log --oneline -n 10` —— 查看最近 10 次提交

常见坑:
- **过度信任 AI**:AI 生成的代码必须审查,尤其是错误处理和边界情况
- **无限迭代**:设置最大迭代次数(如 3 次),避免死循环
- **缺少 dataclass**:agent 之间的消息应该用 dataclass 定义,不要用 dict
- **忘记日志**:agent team 协作过程应该用 logging 记录,方便调试

Pull Request (PR):
- 本周延续 PR 流程:分支 → 多次提交 → push → PR → review → merge
- PR 描述模板:
  ```markdown
  ## 本周做了什么
  - 学习了 agent team 模式的基本概念
  - 实现了 reader/writer/reviewer agent
  - 理解了失败驱动迭代的开发方式
  - 为 PyHelper 添加了学习计划追踪功能

  ## 自测
  - [ ] 运行 `python3 -m pytest chapters/week_13/tests -q` 通过
  - [ ] agent team 流程能正常运行
  - [ ] reviewer checklist 能检测出问题
  - [ ] PyHelper plan 命令能生成学习计划

  ## 待 review
  请重点检查 agent 分工和消息格式设计
  ```

---

## 本周小结(供下周参考)

"我有个感悟,"小北合上电脑,"这周学的不是'怎么用 AI 工具',而是'怎么和 AI 协作'。"

老潘抬头看她:"怎么说?"

"你看,"小北翻开笔记,"agent team 模式不是'让 AI 代替我',而是'让 AI 成为团队成员'——我负责设计、决策和审查,AI 负责执行和验证。"

阿码在旁边补充:"而且 review checklist 和失败驱动迭代也很重要——AI 生成的代码不一定可靠,得逐项检查;发现问题后不是放弃,而是迭代修复。"

老潘笑了:"恭喜你们,从'单兵作战'进化成'团队协作'了。"

本周你学习了 agent team 模式——理解了多 agent 协作的基本概念,掌握了 review checklist 的设计方法,实践了失败驱动迭代的开发方式。这些不只是技术技能,更是**工程思维的体现**——你在设计"如何和 AI 协作完成复杂任务"。

还记得 Week 01 你写下第一个 `print("Hello")` 吗?那时的程序只能"自说自话",没有交互。Week 12 你学了 argparse,程序可以通过命令行和世界交互。现在,你的程序可以"和其他 AI 协作"——从"单组件"变成"分布式系统"。

阿码感叹:"原来 agent team 不只是'AI 编程',更是'软件工程的自动化'——把 code review、测试、迭代这些流程自动化了。"

下周我们将进入 Week 14:Capstone 收敛发布——把前 13 周的所有技能综合起来,完成 PyHelper v1.0 的发布。这将是你的第一个完整的、可交付的命令行工具。

---

## Definition of Done(学生自测清单)

完成本周学习后,请确认你能做到以下事情:

**核心技能**:你能设计简单的 agent team 流程(reader → writer → reviewer);能用 dataclass 定义 agent 之间的消息格式;能设计 review checklist 来审查 AI 生成的代码;能实现失败驱动迭代(测试失败 → 修复 → 再测试)。

**编程哲学**:你理解 **human-in-the-loop 的工作模式**——你是技术负责人,AI 是团队成员,不是替代者。你知道**信任但验证**的重要性——AI 生成的代码必须审查,尤其是错误处理和边界情况。

**实践能力**:你能为 PyHelper 用 agent team 模式添加新功能;能为不同 agent 设计清晰的职责边界;能用 review checklist 检测 AI 代码的常见问题;能用失败驱动迭代改进 AI 生成的内容。

**工程习惯**:你至少提交了 2 次 Git(draft + verify),并且运行 `python3 -m pytest chapters/week_13/tests -q` 通过了所有测试。

---

**如果你想验证自己的掌握程度**,试着回答这些问题:

- agent team 模式和"单个 AI 生成代码"有什么区别?
- 如何用 dataclass 定义 agent 之间的消息格式?
- review checklist 应该包含哪些检查项?为什么边界情况最重要?
- 失败驱动迭代和 TDD 循环有什么相似之处?
- 如何设置最大迭代次数?为什么需要这个限制?
- 如何为 PyHelper 设计一个 agent team 来添加新功能?

如果你能自信地回答这些问题,说明你已经掌握了本周的核心内容。
