---
name: draft-chapter
description: 生成本周正文：规划（含 Bloom/回顾桥/超级线/角色）→ 场景驱动写正文 → 深度润色 → 四维 QA → 修订回路 → 落盘 QA_REPORT。
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

- `CHAPTER.md`：叙事流畅、有贯穿案例 + PyHelper 超级线、循环角色出场、回顾桥达标、读起来像真人教材（不是模板填空）
- `QA_REPORT.md`：写入 StudentQA 的四维评分 + 阻塞项/建议项

## 核心原则

**写作质量是第一优先级。** 通过验证是必要条件，但不是充分条件。一篇通过了所有检查但读起来像模板的文章，仍然是失败的交付。

## 步骤（按顺序）

### 第 1 步：规划结构 + 贯穿案例 + 认知负荷 + 超级线 + 角色

调用 subagent `syllabus-planner`：

- 产出章节结构（小节标题 + 每节学习目标 + Bloom 层次）
- **必须设计本章的贯穿案例**：一个渐进式小项目，每节推进一步，章末可运行
- **必须规划 2 个 AI 小专栏的位置和主题**（第 1 个在前段，第 2 个在中段；含建议搜索词）
- **必须做认知负荷检查**：新概念数在预算内，回顾桥设计达标
- **必须规划 PyHelper 超级线推进**
- **必须规划循环角色出场位置**
- 写入 `chapters/week_XX/CHAPTER.md`

### 第 2 步：场景驱动写正文

调用 subagent `chapter-writer`：

- **必须先读 `shared/writing_exemplars.md` + `shared/characters.yml`**
- 以贯穿案例为主线，用"场景 → 困惑 → 解法 → 深化"的叙事弧线写每一节
- 使用循环角色（小北/阿码/老潘）增强代入感，每章至少 2 次出场
- 写回顾桥：在新场景中自然引用前几周概念
- 写 PyHelper 进度小节
- 严禁所有节使用相同的子标题模式
- 严禁用 bullet list 堆砌做小结

### 第 3 步：深度润色 + AI 小专栏

调用 subagent `prose-polisher`：

- **必须先读 `shared/writing_exemplars.md` + `shared/characters.yml`**
- 执行诊断清单 + 趣味性诊断清单，判断需要哪个级别的改写
- 检查角色一致性（对照 `shared/characters.yml`）
- 可做结构性重组（不仅仅是换词）
- **必须插入 2 个 AI 时代小专栏**：
  - 按 `syllabus-planner` 规划的位置和主题插入
  - 必须尝试联网搜索真实数据（用 WebSearch 或 Bash curl）
  - 位置硬约束：一个在前段、一个在中段，禁止全堆章末

### 第 4 步：学生视角四维审读

调用 subagent `student-qa`：

- 只读审读，输出四维评分 + 问题清单
- 四维评分：叙事流畅度 / 趣味性 / 知识覆盖 / 认知负荷（各 1-5 分）
- 总分 >= 16/20 才能通过

### 第 5 步：修订回路

**如果 student-qa 总分 < 16 或有阻塞项**：

| 总分范围 | 处理方式 |
|---------|---------|
| 12-15 | 把具体维度的阻塞项传回 `prose-polisher` 修复 |
| 8-11 | 回传 `chapter-writer` 做结构性重写 |
| < 8 | 回传 `syllabus-planner` 重新规划 |

**最多迭代 2 轮**。如果 2 轮后仍不达标，记录到 QA_REPORT 中由人工处理。

### 第 6 步：落盘 QA_REPORT

把最终的 StudentQA 输出落盘到 `chapters/week_XX/QA_REPORT.md`：

- 四维评分写在顶部
- 阻塞项放到"## 阻塞项"下（checkbox）
- 建议项放到"## 建议项"下（checkbox）
