# 《Python 程序设计（Agentic Coding）》写作宪法

本文件是全书的**最高约束**。所有 subagents、skills、team mate 的输出都必须遵守。

## 目标与读者

| 项目 | 说明 |
|------|------|
| 读者 | 零基础（第一次学编程）或只会一点点 Python 的初学者 |
| 目标 | 用"工程化 + agentic 工作流"掌握 Python 基本功（从脚本到可维护的小工具） |
| 语言 | 中文；关键术语括注英文 |
| 课程结构 | 14 周，三阶段：入门基础 → 工程进阶 → 综合实战 |

## 每周章包 Definition of Done (DoD)

对任意 `chapters/week_XX/`，发布前**全部**必须满足：

1. **文件齐全**：
   - `CHAPTER.md` / `ASSIGNMENT.md` / `RUBRIC.md` / `QA_REPORT.md`
   - `ANCHORS.yml` / `TERMS.yml`
   - `examples/` / `starter_code/solution.py` / `tests/`
2. **测试通过**：`python3 -m pytest chapters/week_XX/tests -q`
3. **QA 阻塞项清零**：`QA_REPORT.md` 的"阻塞项"下不存在未勾选 `- [ ]`
4. **术语同步**：`TERMS.yml` 中的 `term_zh` 必须已进入 `shared/glossary.yml`
5. **锚点完整**：`ANCHORS.yml` 的 `id` 周内唯一，`claim/evidence/verification` 齐全
6. **叙事质量**：`student-qa` 评分 >= 4 分（1-5 分制）

上述规则由 `scripts/validate_week.py` 与 `.claude/hooks/` 强制执行。

### Git/Gitea 建议项（不作为硬闸门）

- `/release-week` 前建议工作区干净（`git status --porcelain` 为空）
- 至少 2 次提交（draft + verify）
- PR 描述引用本周 DoD + 验证通过信息
- 参考：`shared/gitea_workflow.md`

## 行文风格

详见 `shared/style_guide.md` + `shared/writing_exemplars.md`。

**三条铁律**：

1. **场景驱动**：先让读者感受到"我需要这个"，再引出概念。概念是答案，不是前提。
2. **贯穿案例**：每章一个渐进式小项目，每节推进一步，章末可运行。
3. **禁止模板感**：不要每节都用相同的子标题结构；不要 bullet list 堆砌做小结。

**质量闸门**：
- `student-qa` 打分 1-5，>= 4 分才能 release
- 若正文模板化 → 运行 `/polish-week week_XX`（可做结构性改写）
- 代码块必须可运行（或注明"伪代码/节选"）
- 重要结论必须可验证 → 落到 `ANCHORS.yml`

## 术语与一致性

- 新术语先在当周 `TERMS.yml` 登记，再合入 `shared/glossary.yml`
- 中文为主，英文可选；定义必须短、清晰、可被新手复述

## Team 协作约定（强制）

- 所有 task subject 必须以 `[week_XX]` 开头（hooks 依赖）
  - 示例：`[week_01] Draft chapter outline`
- Lead 建议开启 delegate mode：只拆任务与收敛，不写正文
- **所有写正文的 agent 必须先读 `shared/writing_exemplars.md`**
- 任意 teammate 完成任务前，必须确保本周校验通过（hooks 会拦截）
