---
name: draft-chapter
description: 生成本周正文：设计贯穿案例 → 场景驱动写正文 → 深度润色 → 学生视角 QA → 修订回路 → 落盘 QA_REPORT。
argument-hint: "<week_id e.g. week_01>"
allowed-tools: Read, Write, Edit, Grep, Glob
disable-model-invocation: true
---

# /draft-chapter

## 用法

```
/draft-chapter week_XX
```

## 目标

- `CHAPTER.md`：叙事流畅、有贯穿案例、读起来像真人教材（不是模板填空）
- `QA_REPORT.md`：写入 StudentQA 的阻塞项/建议项

## 核心原则

**写作质量是第一优先级。** 通过验证是必要条件，但不是充分条件。一篇通过了所有检查但读起来像模板的文章，仍然是失败的交付。

## 步骤（按顺序）

### 第 1 步：规划结构 + 贯穿案例

调用 subagent `syllabus-planner`：

- 产出章节结构（小节标题 + 每节学习目标）
- **必须同时设计本章的贯穿案例**：一个渐进式小项目，每节推进一步，章末可运行
- 写入 `chapters/week_XX/CHAPTER.md`

### 第 2 步：场景驱动写正文

调用 subagent `chapter-writer`：

- **必须先读 `shared/writing_exemplars.md`**，理解好 vs 坏的写法
- 以贯穿案例为主线，用"场景 → 困惑 → 解法 → 深化"的叙事弧线写每一节
- 严禁所有节使用相同的子标题模式
- 严禁用 bullet list 堆砌做小结

### 第 3 步：深度润色

调用 subagent `prose-polisher`：

- **必须先读 `shared/writing_exemplars.md`**
- 执行诊断清单，判断需要哪个级别的改写
- 可做结构性重组（不仅仅是换词）
- 可加入 1-2 个"AI 时代小专栏"

### 第 4 步：学生视角审读

调用 subagent `student-qa`：

- 只读审读，输出问题清单
- 除了传统的"看不懂/缺解释"，还要检查**叙事质量**：
  - 是否有模板感？
  - 贯穿案例是否连贯？
  - 是否读得下去？

### 第 5 步：修订回路（关键新增！）

**如果 student-qa 输出了阻塞项**：

1. 把阻塞项传回 `chapter-writer` 或 `prose-polisher`（取决于问题类型）
2. 让对应 agent 修复具体问题
3. 再跑一次 `student-qa` 确认阻塞项已解决

**最多迭代 2 轮**。如果 2 轮后仍有阻塞项，记录到 QA_REPORT 中由人工处理。

### 第 6 步：落盘 QA_REPORT

把最终的 StudentQA 输出落盘到 `chapters/week_XX/QA_REPORT.md`：

- 阻塞项放到"## 阻塞项"下（checkbox）
- 建议项放到"## 建议项"下（checkbox）
