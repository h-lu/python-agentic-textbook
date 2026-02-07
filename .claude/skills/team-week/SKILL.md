---
name: team-week
description: 需要用 agent team 并行产出一整周章包时，生成一段可直接粘贴给 Lead 的 kickoff 提示词（含角色、任务拆分、依赖与校验）。
argument-hint: "<week_id e.g. week_01>"
allowed-tools: Read, Grep, Glob, Write, Edit
disable-model-invocation: true
---

# /team-week

## 用法

```
/team-week week_XX
```

## 作用

你是 Lead（delegate mode，只拆任务与收敛，不直接写正文）。
目标：把 week_XX 产出成完整章包，并通过校验：
- python3 scripts/validate_week.py --week week_XX --mode release

强制约束：
- 所有 task subject 必须以 [week_XX] 开头（hooks 依赖）
- 交付遵循 CLAUDE.md + shared/style_guide.md
- **所有写正文的 agent 必须先读 shared/writing_exemplars.md + shared/characters.yml**
- /draft-chapter week_XX 已内置 prose-polisher + 修订回路
- **ANCHORS.yml 由 Consistency 角色统一管理**：其他角色如有 anchor 建议，在任务输出中标注（含 id/claim/evidence/verification）即可，不要直接读写 ANCHORS.yml

写作质量红线（四维评分体系）：
- student-qa 四维评分总分必须 >= 16/20
  - 叙事流畅度 >= 3
  - 趣味性 >= 3
  - 知识覆盖 >= 3
  - 认知负荷 >= 3
- 任一维度 <= 2 = 阻塞项
- 禁止每节都用相同的子标题模式
- 每章必须有贯穿案例（渐进式小项目）+ PyHelper 超级线推进
- 循环角色（小北/阿码/老潘）每章至少出场 2 次
- 新概念数不超预算，回顾桥数量达标
- 禁止连续 6+ 条 bullet list
- 小结不能全部用 bullet list
- **AI 小专栏必须 2 个，分别在前段和中段**（禁止全堆章末）；prose-polisher 必须联网搜索真实数据

请创建 team 角色（建议 5 人）：
- Writer（CHAPTER + PyHelper 进度）
- Example（examples + 讲解段落 + PyHelper 示例代码）
- Assignment（ASSIGNMENT + RUBRIC + AI 协作练习）
- QA（student-qa，四维评分 + 知识理解 + 叙事质量审读）
- Consistency（consistency-editor，术语/格式/引用/角色一致性）

Task list（注意依赖）：
- [week_XX] Outline + 贯穿案例 + Bloom 标注 + 回顾桥 + 超级线 + 角色出场（syllabus-planner）
- [week_XX] Draft CHAPTER.md + 循环角色 + 回顾桥 + PyHelper 进度（chapter-writer）
- [week_XX] Deep polish + AI sidebar + 趣味性诊断 + 角色一致性（prose-polisher）
- [week_XX] Produce examples + PyHelper 示例代码（example-engineer）
- [week_XX] Design tests（test-designer）
- [week_XX] Write assignment + rubric + AI 协作练习（exercise-factory）
- [week_XX] QA sweep — 四维评分 + 知识理解（student-qa）
- [week_XX] 修订回路：如果 QA 总分 < 16，按质量升级路径回传修复
- [week_XX] Consistency sweep + 角色一致性检查（consistency-editor）
- [week_XX] Green check + release（/qa-week -> /release-week）

关键检查点（**仅产出阶段角色**完成任务时需要过，规划阶段的 syllabus-planner 不用）：
- python3 -m pytest chapters/week_XX/tests -q
- python3 scripts/validate_week.py --week week_XX --mode task

> 注意：syllabus-planner 只产出 CHAPTER.md 大纲，此时其他文件尚未就绪，不要运行校验。校验从 Example/Assignment 角色开始适用。

收敛规则：
- QA_REPORT 的"阻塞项"必须清零（不允许 - [ ]）才能 release
- 四维评分总分必须 >= 16/20 才能 release
- 不要为了"写完"牺牲可运行/可验证：tests/anchors/terms 要能对上
