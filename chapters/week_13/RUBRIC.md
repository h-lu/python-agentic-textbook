# Week 13 评分标准

## 评分总览

| 练习 | 分值 | 核心能力 |
|------|------|---------|
| 练习 1（基础） | 30 分 | dataclass 定义、消息传递、异常处理 |
| 练习 2（进阶） | 40 分 | review checklist 设计、边界检查 |
| 练习 3（挑战） | 30 分 | 失败驱动迭代、agent team 协作 |
| **总分** | **100 分** | |

---

## 练习 1：Reader + Writer 流程（30 分）

### 功能正确性（20 分）

| 评分项 | 分值 | 评分标准 |
|--------|------|---------|
| ReaderAgent 能正确读取笔记 | 5 分 | 能提取标题、周次、主题；文件不存在时抛出异常或返回错误 |
| WriterAgent 能生成学习计划 | 5 分 | 能根据周次推断前置知识、设置优先级、估算时长 |
| Dataclass 定义正确 | 5 分 | `NoteInfo` 和 `StudyPlan` 字段完整、类型正确 |
| 消息传递正确 | 5 分 | Reader 的输出正确传递给 Writer |

### 代码质量（10 分）

| 评分项 | 分值 | 评分标准 |
|--------|------|---------|
| 异常处理 | 5 分 | 文件读取有 `try/except`，处理 `FileNotFoundError` |
| 变量命名 | 3 分 | 变量名清晰（如 `note_info` 而非 `data`） |
| 代码简洁 | 2 分 | 没有重复代码，逻辑清晰 |

### 扣分项

- ❌ 没有用 `@dataclass` 定义消息格式：**-10 分**
- ❌ 没有异常处理（文件不存在时崩溃）：**-5 分**
- ❌ Reader 和 Writer 之间没有消息传递（各自独立运行）：**-5 分**

### 测试支撑

```python
# tests/test_basic.py
def test_reader_extract_info():
    """测试 Reader 能提取笔记信息"""
    note = NoteInfo(title="异常处理", topics=["异常处理"], difficulty="medium")
    assert note.title == "异常处理"
    assert "异常处理" in note.topics

def test_writer_generates_plan():
    """测试 Writer 能生成学习计划"""
    plan = StudyPlan(week=6, title="异常处理", prerequisites=["函数"], priority="medium")
    assert plan.week == 6
    assert len(plan.prerequisites) > 0
```

---

## 练习 2：Reviewer Agent + Review Checklist（40 分）

### 功能正确性（25 分）

| 评分项 | 分值 | 评分标准 |
|--------|------|---------|
| ReviewerAgent 能检测所有问题 | 10 分 | 检测 4 类问题：前置知识为空、前置知识无效、优先级为空、时长不合理 |
| ReviewResult 定义正确 | 5 分 | `passed` 和 `issues` 字段完整 |
| 边界情况检查 | 10 分 | 空列表、空字符串、超出范围的值都能检测 |

### Checklist 完整性（10 分）

| 评分项 | 分值 | 评分标准 |
|--------|------|---------|
| 前置知识检查 | 3 分 | Week 06+ 必须有前置；前置必须在 `all_topics` 中 |
| 优先级检查 | 2 分 | 不能为空，必须在 high/medium/low 中 |
| 时长检查 | 3 分 | 必须在 4-15 小时之间 |
| 主题检查 | 2 分 | 前置知识必须在课程主题列表中 |

### 代码质量（5 分）

| 评分项 | 分值 | 评分标准 |
|--------|------|---------|
| 检查逻辑清晰 | 3 分 | `if` 条件正确，没有嵌套过深 |
| 问题描述清晰 | 2 分 | `issues` 列表中的信息具体（不是 "Error 1" 这种模糊描述） |

### 扣分项

- ❌ Reviewer 返回 `bool` 而非 `ReviewResult`（无法知道具体问题）：**-10 分**
- ❌ 没有检查边界情况（空输入、None）：**-5 分**
- ❌ 检查逻辑写反（`if plan.prerequisites:` 而非 `if not plan.prerequisites:`）：**-5 分**

### 测试支撑

```python
# tests/test_reviewer.py
def test_reviewer_catches_empty_prerequisites():
    """测试 Reviewer 能检测空前置知识"""
    plan = StudyPlan(week=6, title="异常处理", prerequisites=[], priority="medium")
    result = reviewer.review_plan(plan, all_topics=["函数", "文件"])
    assert not result.passed
    assert "缺少前置知识" in result.issues

def test_reviewer_catches_invalid_priority():
    """测试 Reviewer 能检测无效优先级"""
    plan = StudyPlan(week=6, title="异常处理", prerequisites=["函数"], priority="")
    result = reviewer.review_plan(plan, all_topics=["函数"])
    assert not result.passed
    assert "优先级未设置" in result.issues
```

---

## 练习 3：失败驱动迭代 + 完整 Agent Team（30 分）

### 功能正确性（20 分）

| 评分项 | 分值 | 评分标准 |
|--------|------|---------|
| 迭代循环正确 | 8 分 | 最多 3 次迭代；成功时提前退出；失败时返回最后一次结果 |
| Writer 能修复问题 | 7 分 | 根据 `issues` 参数修复（不是重新生成一遍） |
| 完整流程能运行 | 5 分 | reader → writer → reviewer → 修复 → 通过 |

### 迭代逻辑（5 分）

| 评分项 | 分值 | 评分标准 |
|--------|------|---------|
| 终止条件正确 | 2 分 | 成功时 `return`，失败时继续迭代 |
| 保留最后结果 | 2 分 | 3 次后不丢弃，返回并警告 |
| 迭代次数限制 | 1 分 | 没有无限循环 |

### 代码质量（5 分）

| 评分项 | 分值 | 评分标准 |
|--------|------|---------|
| 日志记录 | 2 分 | 用 `logging` 记录每次迭代（如 "迭代 1/3"） |
| 错误处理 | 2 分 | 传入无效参数时不会崩溃 |
| 代码结构 | 1 分 | 没有重复代码，迭代逻辑清晰 |

### 扣分项

- ❌ 无限迭代（没有最大迭代次数限制）：**-10 分**
- ❌ Writer 的修复没有使用 `issues` 参数（只是重新生成）：**-7 分**
- ❌ 没有保留最后一次结果（3 次后全部丢弃）：**-5 分**

### 测试支撑

```python
# tests/test_agent_team.py
def test_failure_driven_iteration():
    """测试失败驱动迭代"""
    analysis = NoteAnalysis(week=6, title="异常处理", topics=["异常处理"], difficulty="medium")

    plan = iterative_generation(analysis, all_topics=["函数", "文件"])

    # 应该在迭代内修复问题
    assert plan.week == 6
    assert len(plan.prerequisites) > 0  # 前置知识被修复

def test_max_iterations():
    """测试最大迭代次数限制"""
    # 模拟一个永远无法修复的场景
    # 验证 3 次后停止并返回最后一次结果
    ...
```

---

## AI 协作练习审查（可选）

如果学生提交了 AI 协作练习的审查报告，额外评分：

| 评分项 | 分值 | 评分标准 |
|--------|------|---------|
| 发现了真实问题 | 5 分 | 指出 AI 代码的实际问题（不是虚构的） |
| 修改合理 | 3 分 | 修改确实解决了问题 |
| 报告清晰 | 2 分 | 报告结构清晰，能看懂做了什么 |

### 扣分项

- ❌ 直接复制 AI 代码，没有审查：**0 分**（整个 AI 练习不得分）
- ❌ 报告内容空洞（"AI 生成的代码很好，没问题"）：**-3 分**

---

## 代码质量通用标准（所有练习）

### 命名规范（2 分）

- ✅ 变量名用蛇形命名（`note_info` 而非 `noteInfo`）
- ✅ 类名用大驼峰（`ReaderAgent` 而非 `readerAgent`）
- ✅ 避免单字母变量（除 `i`, `x`, `y` 在循环中）

### 类型标注（2 分）

- ✅ 函数参数有类型标注（如 `def read_note(file_path: Path) -> NoteInfo:`）
- ✅ 用 `from typing import List, Optional` 导入类型

### 文档字符串（2 分）

- ✅ 类和主要函数有 docstring（用 `"""` 三引号）
- ✅ Docstring 说明"做什么"（不需要写"怎么做"）

### 异常处理（2 分）

- ✅ 文件操作用 `try/except`
- ✅ 异常信息具体（不是 `except: pass`）

### 测试覆盖（2 分）

- ✅ 每个主要函数有至少一个测试
- ✅ 测试边界情况（空输入、无效值）

---

## 总分换算

| 分数区间 | 等级 | 描述 |
|---------|------|------|
| 90-100 | 优秀 | 完成所有练习，代码质量高，有额外思考 |
| 75-89 | 良好 | 完成基础+进阶，挑战题部分完成 |
| 60-74 | 及格 | 完成基础+进阶，代码能运行但质量一般 |
| 0-59 | 不及格 | 基础题未完成或有严重错误 |

---

## 验证命令

```bash
# 运行所有测试
python3 -m pytest chapters/week_13/tests -v

# 只测基础
python3 -m pytest chapters/week_13/tests/test_basic.py -v

# 只测进阶
python3 -m pytest chapters/week_13/tests/test_reviewer.py -v

# 只测挑战
python3 -m pytest chapters/week_13/tests/test_agent_team.py -v

# 查看测试覆盖率
python3 -m pytest chapters/week_13/tests --cov=. --cov-report=term-missing
```

---

## 评分提醒

1. **功能优先**：代码能跑、测试通过是第一位的
2. **渐进评分**：基础题能拿大部分分数，挑战题是加分项
3. **鼓励理解**：如果代码逻辑对但有 bug，扣 2-3 分而不是 0 分
4. **AI 协作是可选**：不参与 AI 练习不影响满分
