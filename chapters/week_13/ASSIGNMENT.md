# Week 13 作业：用 AI Agent 协作开发

> "Alone we can do so little; together we can do so much."
> — Helen Keller

## 作业概述

本周你将实践 **agent team 模式**——不是"让 AI 代替你写代码"，而是"设计一个 AI 团队，你当技术负责人"。你将实现 reader、writer、reviewer 三个 agent，让它们协作完成"从学习笔记生成学习计划"的任务。

核心思想：**你负责设计流程和审查结果，AI 负责执行具体任务**。

---

## 学习目标

完成本周作业后，你将能够：

1. 设计简单的 agent team 流程（reader → writer → reviewer）
2. 用 dataclass 定义 agent 之间的消息格式
3. 设计 review checklist 来审查 AI 生成的代码质量
4. 实现失败驱动迭代（测试失败 → 修复 → 再测试）
5. 理解 "human-in-the-loop" 的工作模式

---

## 背景知识回顾

### Agent team 的三个原则

1. **职责单一**：每个 agent 只做一件事（reader 读文件，writer 生成内容，reviewer 检查质量）
2. **消息传递**：agent 之间通过 dataclass 传递消息（reader 的输出 → writer 的输入）
3. **Human-in-the-loop**：你是技术负责人，负责设计、决策和审查

### Review checklist 的核心

AI 生成的代码常见问题：
- 缺少错误处理（文件不存在、权限不足时崩溃）
- 忽略边界情况（空输入、负数、超大值）
- 过度工程化（用复杂的库解决简单问题）
- 缺少日志（出问题后无法追溯）

### 失败驱动迭代

```
测试失败 → 修复 → 再测试 → 通过
   (红)    (绿)   (验证)
```

类似 Week 08 的 TDD 循环：失败不是终点，是改进的起点。

---

## 练习 1（基础）：实现 Reader + Writer 流程

### 任务描述

实现一个最简单的 agent team：
- **Reader Agent**：读取并分析 Markdown 学习笔记，提取标题和主题
- **Writer Agent**：根据笔记信息生成学习计划

### 输入

一个 Markdown 学习笔记文件 `notes/week06_exceptions.md`：

```markdown
# Week 06: 异常处理

让程序不崩。try/except 是你的朋友。
```

### 输出

生成的学习计划（打印到控制台）：

```
[reader] 读取笔记: Week 06: 异常处理
  主题: ['异常处理', 'try-except']
  难度: medium
[writer] 生成学习计划: Week 6 - 异常处理
  前置知识: ['函数', '文件']
  优先级: medium
```

### 提示

1. 用 `@dataclass` 定义消息格式：
   - `NoteInfo`（reader 的输出）：title, topics, difficulty
   - `StudyPlan`（writer 的输出）：week, title, prerequisites, priority

2. Reader agent 用简单的正则或字符串操作提取信息（不需要复杂的 NLP）：
   - 从文件名提取周次（如 `week06` → `6`）
   - 从第一个 `#` 标题提取标题
   - 从内容中推断主题（如包含 "异常" → 加 "异常处理"）

3. Writer agent 根据周次推断前置知识（硬编码即可）：
   - Week 06 → 前置 ["函数", "文件"]
   - Week 08 → 前置 ["异常处理", "函数"]

### 常见错误

- ❌ 忘记用 `try/except` 处理文件读取失败
- ❌ 文件不存在时程序直接崩溃
- ❌ 没有检查空文件（空文件也会"一本正经"地生成内容）
- ❌ dataclass 字段类型标注错误（如 `List[str]` 忘记导入）

### 自测

```bash
# 创建测试笔记
mkdir -p notes
echo "# Week 06: 异常处理

让程序不崩。try/except 是你的朋友。" > notes/week06_exceptions.md

# 运行你的代码
python3 starter_code/agent_basic.py

# 应该看到：
# [reader] 读取笔记: Week 06: 异常处理
# [writer] 生成学习计划: Week 6 - 异常处理
```

---

## 练习 2（进阶）：添加 Reviewer Agent 和 Review Checklist

### 任务描述

在练习 1 的基础上，添加 **Reviewer Agent**：
- 检查 writer 生成的学习计划是否符合质量标准
- 使用 review checklist 逐项检查

### Review Checklist

你的 reviewer agent 应该检查以下项目：

1. **前置知识不能为空**（Week 06+ 必须有前置知识）
2. **前置知识必须在课程主题列表中**（不能凭空出现）
3. **优先级不能为空**（必须是 high/medium/low 之一）
4. **估算时长必须合理**（4-15 小时之间）

### 输入

```python
plan = StudyPlan(
    week=6,
    title="异常处理",
    prerequisites=[],  # 空列表 → 应该被检测为问题
    priority="",       # 空字符串 → 应该被检测为问题
    topics=["异常处理"],
    estimated_hours=20  # 超出范围 → 应该被检测为问题
)
```

### 输出

```bash
[reviewer] 审查失败:
  ✗ 缺少前置知识
  ✗ 优先级未设置
  ✗ 估算时长不合理: 20 小时（应在 4-15 之间）
```

### 提示

1. 定义 `ReviewResult` dataclass：
   - `passed: bool`（是否通过审查）
   - `issues: List[str]`（问题列表）

2. Reviewer agent 接收两个参数：
   - `plan: StudyPlan`（要审查的计划）
   - `all_topics: List[str]`（课程所有主题，用于检查前置知识是否有效）

3. 检查逻辑用简单的 `if` 判断即可：
   ```python
   if plan.week >= 6 and not plan.prerequisites:
       issues.append("缺少前置知识")
   ```

### 常见错误

- ❌ Reviewer 返回的是 `bool` 而不是 `ReviewResult`（无法知道具体哪里有问题）
- ❌ 检查逻辑写反了（如 `if plan.prerequisites:` 而不是 `if not plan.prerequisites:`）
- ❌ 忘记导入 `List` 类型（`from typing import List`）

### 自测

```bash
# 运行进阶测试
python3 starter_code/agent_reviewer.py

# 应该看到：
# [reviewer] 审查失败: ['缺少前置知识', '优先级未设置', '估算时长不合理: 20 小时']
```

---

## 练习 3（挑战）：失败驱动迭代 + 完整 Agent Team

### 任务描述

实现完整的 agent team 流程，支持**失败驱动迭代**：

```
reader → writer → reviewer → (失败) → writer → reviewer → (通过)
                      ↓                     ↓
                   发现问题              修复问题
```

要求：
1. Reader 读取笔记
2. Writer 生成计划
3. Reviewer 检查质量
4. 如果发现问题 → Writer 根据 issues 修复 → 再次检查
5. 最多迭代 3 次，如果还没通过则警告并返回最后一次结果

### 输入

`notes/week08_testing.md`：

```markdown
# Week 08: 自动化测试

用 pytest 验证代码质量。
```

### 输出

```bash
[reader] 读取笔记: Week 08: 自动化测试
  主题: ['测试', 'pytest']
  难度: medium

=== 迭代 1/3 ===
[writer] 生成计划 (初次)
[reviewer] 审查失败:
  ✗ 缺少前置知识

=== 迭代 2/3 ===
[writer] 修复问题 (根据 issues)
[reviewer] 审查通过!

✓ 最终计划: Week 8 - 自动化测试
  前置知识: ['异常处理', '函数']
  优先级: medium
```

### 提示

1. **迭代循环**：
   ```python
   for iteration in range(3):
       if iteration == 0:
           plan = writer.create_plan(analysis)  # 初次生成
       else:
           plan = writer.fix_plan(analysis, last_issues)  # 修复

       issues = reviewer.review_plan(plan)
       if not issues:
           return plan  # 成功
       last_issues = issues
   ```

2. **Writer 的修复逻辑**（简化版）：
   - 如果 reviewer 说"缺少前置知识" → 根据周次推断并添加
   - 如果 reviewer 说"优先级未设置" → 根据难度推断

3. **Dataclass 扩展**：
   - `StudyPlan` 添加 `estimated_hours` 字段
   - 根据难度推断时长（easy=4, medium=7, hard=10）

### 常见错误

- ❌ 无限迭代（忘记设置最大迭代次数）
- ❌ Writer 的 `fix_plan` 没有根据 `issues` 参数修复（只是重新生成一遍）
- ❌ 没有记录最后一次结果（3 次后全部丢弃）
- ❌ 迭代次数用完了但没有警告（用户不知道是否成功）

### 自测

```bash
# 运行完整测试
python3 -m pytest chapters/week_13/tests/test_agent_team.py -v

# 应该看到所有测试通过
```

---

## AI 协作练习（可选）

本周属于 AI 融合的**主导期**（Week 11-14），你可以尝试用 AI 结对编程完成作业。

### 任务

用 AI 工具（如 Claude、ChatGPT、GitHub Copilot）辅助实现 **Reviewer Agent** 的 review checklist。

### 审查清单（你必须自己检查）

使用 AI 生成代码后，**不要直接提交**，必须逐项检查：

- [ ] **代码能运行吗？**（没有语法错误，能执行）
- [ ] **变量命名清晰吗？**（不是 `x`, `data1`, `temp` 这种模糊命名）
- [ ] **有错误处理吗？**（处理了空输入、None 等边界情况）
- [ ] **检查逻辑正确吗？**（`if` 条件写反了吗？`and`/`or` 用对了吗？）
- [ ] **你能解释每一行代码吗？**（如果解释不了，说明你没理解，不能提交）

### 提交内容

1. 修复后的代码（你可以基于 AI 生成的内容修改）
2. 审查报告（简短说明）：
   - AI 生成了什么？
   - 你发现了哪些问题？
   - 你做了哪些修改？

### 示例审查报告

```markdown
## AI 协作练习：Reviewer Agent 审查报告

### AI 生成的内容
AI 生成了一个 `ReviewAgent` 类，用于检查学习计划的质量。

### 发现的问题
1. AI 用了 `re` 模块做复杂的正则匹配，但简单的 `if` 判断就够了（过度工程化）
2. 没有处理 `all_topics` 为空的情况（边界情况）
3. 变量名 `res` 不清晰，改成了 `review_result`

### 我的修改
- 简化检查逻辑，用 `if not plan.prerequisites` 代替正则
- 添加 `if not all_topics` 的检查
- 重命名变量提高可读性
```

### 提醒

- **禁止直接复制 AI 输出的代码**。你必须理解并审查。
- 如果 AI 生成的代码有问题，你**必须修复**才能提交。
- 测试会检查代码质量（命名、错误处理、边界情况）。

---

## 提交要求

### 文件结构

```
chapters/week_13/
├── starter_code/
│   ├── agent_basic.py        # 练习 1：Reader + Writer
│   ├── agent_reviewer.py     # 练习 2：加 Reviewer
│   ├── agent_team.py         # 练习 3：完整流程
│   └── solution.py           # 参考实现（由 example-engineer 提供）
├── tests/
│   ├── test_basic.py         # 练习 1 测试
│   ├── test_reviewer.py      # 练习 2 测试
│   └── test_agent_team.py    # 练习 3 测试
└── 你的代码文件
```

### 必做（基础 + 进阶）

- [ ] 实现 `ReaderAgent`（能读取并分析笔记）
- [ ] 实现 `WriterAgent`（能生成学习计划）
- [ ] 实现 `ReviewerAgent`（能用 checklist 检查质量）
- [ ] 通过 `python3 -m pytest chapters/week_13/tests/test_basic.py -v`
- [ ] 通过 `python3 -m pytest chapters/week_13/tests/test_reviewer.py -v`

### 加分（挑战）

- [ ] 实现失败驱动迭代（最多 3 次迭代）
- [ ] `WriterAgent` 能根据 `issues` 修复问题（不是重新生成）
- [ ] 通过 `python3 -m pytest chapters/week_13/tests/test_agent_team.py -v`
- [ ] 添加日志记录（用 `logging` 模块记录每个 agent 的运行过程）
- [ ] 为 PyHelper 添加 `pyhelper plan generate` 命令（CLI 调用 agent team）

### AI 协作练习（可选）

- [ ] 用 AI 辅助生成部分代码
- [ ] 提交审查报告（发现的问题 + 你的修改）

---

## 提示与帮助

### 如果遇到困难

1. **先看示例**：`starter_code/solution.py` 包含完整的参考实现
2. **再看本周 CHAPTER.md**：第 1-3 节有详细的代码示例
3. **回顾之前的知识**：
   - Week 11 的 `@dataclass`（定义消息格式）
   - Week 08 的 pytest（测试驱动开发）
   - Week 06 的异常处理（`try/except`）

### 调试技巧

```python
# 打印 agent 之间的消息传递
print(f"[reader] 输出: {note_info}")
print(f"[writer] 收到: {note_info}")
print(f"[writer] 输出: {plan}")
print(f"[reviewer] 收到: {plan}")
```

---

## 最后提醒

本周的重点不是"写复杂的代码"，而是理解 **agent team 的协作模式**：

- 你是技术负责人，负责设计流程
- AI 是团队成员，负责执行任务
- Review checklist 确保"信任但验证"
- 失败驱动迭代让系统自我改进

代码本身不复杂，但背后的思想很重要。祝你完成第一个 AI 团队协作项目！
