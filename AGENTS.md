# Agent Instructions (python-agentic-textbook)

本仓库用于生成《Python 程序设计（Agentic Coding）》教材的"每周章包"交付物（见 `chapters/`）。

## 写作质量（最高优先级）

**所有写正文的 agent 在动笔前必须先读 `shared/writing_exemplars.md`。**

核心要求：
- 场景驱动叙事，禁止模板化结构
- 每章必须有贯穿案例（渐进式小项目）
- `student-qa` 叙事质量评分 >= 4 分才能 release

详见：`shared/style_guide.md` + `shared/writing_exemplars.md`

## Project DoD（必须遵守）

- `python3 scripts/validate_week.py --week week_XX --mode release` 通过
- `python3 -m pytest chapters/week_XX/tests -q` 通过
- 任务 subject 必须以 `[week_XX]` 开头（hooks 依赖）

## Agent 团队（9 个专职角色）

| Agent | 职责 | 关键约束 |
|-------|------|---------|
| `syllabus-planner` | 章节结构 + 贯穿案例设计 | 必须输出贯穿案例 |
| `chapter-writer` | 场景驱动写正文 | 先读 writing_exemplars.md |
| `prose-polisher` | 深度改写（可重组结构） | 三级改写权限 |
| `student-qa` | 知识理解 + 叙事质量审读 | 输出 1-5 分评分 |
| `example-engineer` | 示例代码 + 反例 | 与贯穿案例关联 |
| `test-designer` | pytest 用例矩阵 | 正例 + 边界 + 反例 |
| `exercise-factory` | 分层作业 + rubric | 基础/进阶/挑战 |
| `consistency-editor` | 术语/格式/引用统一 | 对齐 glossary.yml |
| `error-fixer` | 修复校验失败 | 逐条修复再验证 |

## Skill 命令（9 个）

| 命令 | 作用 |
|------|------|
| `/new-week` | 创建新周目录和模板文件 |
| `/draft-chapter` | 完整写作流水线（规划→写→润色→QA→修订回路） |
| `/polish-week` | 对已有章节做深度改写 |
| `/make-assignment` | 生成作业 + 评分标准 |
| `/qa-week` | 单周质量检查 |
| `/release-week` | 发布前闸门检查 |
| `/team-week` | 生成 agent team kickoff 提示词 |
| `/qa-book` | 跨周一致性检查 |
| `/scaffold-book` | 批量创建 week_01..week_14 |

## Gitea PR 流程（Week 06+ 必做）

分支 → 多次提交 → push → PR → review → merge
参考：`shared/gitea_workflow.md`
