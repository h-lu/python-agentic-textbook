# Agent Instructions (python-agentic-textbook)

本仓库用于生成《Python 程序设计（Agentic Coding）》教材的"每周章包"交付物（见 `chapters/`）。

## 写作质量（最高优先级）

**所有写正文的 agent 在动笔前必须先读 `shared/writing_exemplars.md` + `shared/characters.yml`。**

核心要求：
- 场景驱动叙事，禁止模板化结构
- 每章必须有贯穿案例（渐进式小项目）+ PyHelper 超级线推进
- 循环角色（小北/阿码/老潘）每章至少出场 2 次
- `student-qa` 四维评分总分 >= 18/20 才能 release
- 新概念数不超过认知负荷预算，回顾桥数量达标
- **章首导入**：每章标题后必须有引言格言 + 时代脉搏段落（200-300 字，连接 AI/技术趋势与本章主题）
- **写作元数据必须注释**：Bloom 标注、概念预算表、AI 专栏规划、角色出场规划等必须用 `<!-- ... -->` 包裹
- **Context7 技术查证**：写正文前必须用 Context7 MCP 查证本章核心技术点的当前最佳实践
- **⚠️ 参考链接真实性**：绝对禁止编造参考链接和统计数据。AI 小专栏、时代脉搏中的所有 URL 必须来自搜索工具返回的真实结果（优先研究缓存 `.research_cache.md` / `WebSearch` 内置工具，备选 `perplexity` MCP / `WebFetch`）

详见：`shared/style_guide.md` + `shared/writing_exemplars.md` + `CLAUDE.md`

## Project DoD（必须遵守）

- `python3 scripts/validate_week.py --week week_XX --mode release` 通过
- `python3 -m pytest chapters/week_XX/tests -q` 通过
- 任务 subject 必须以 `[week_XX]` 开头（hooks 依赖）

## Agent 协作流水线

一周章包的完整生产流程：

```
                    ┌─────────────────┐
                    │ syllabus-planner │  ← 规划结构 + 贯穿案例 + 章首导入 + 回顾桥
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Context7 查证    │  ← 用 Context7 MCP 查证本章技术点最佳实践
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  chapter-writer  │  ← 章首导入 + 场景驱动写正文 + 循环角色
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Lead: Web研究   │  ← WebSearch/perplexity 搜索，写入 .research_cache.md
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  prose-polisher  │  ← 深度润色 + AI 小专栏（读缓存 + WebSearch 兜底）
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌────────────┐  ┌────────────┐  ┌──────────────┐
     │example-eng. │  │test-designer│  │exercise-fact.│  ← 并行产出
     └──────┬─────┘  └─────┬──────┘  └──────┬───────┘
            └──────────────┼────────────────┘
                           │
                  ┌────────▼────────┐
                  │   student-qa    │  ← 四维评分（只读审读）
                  └────────┬────────┘
                           │
              ┌──────────────────────────────────┐
              │           所有评分                │
              │     都进入修订回路（最多3轮）      │
              │  >=18: 轻量修复建议项              │
              │  14-17: 修复阻塞项                 │
              │  10-13: 结构性重写                 │
              │  <10: 重新规划                     │
              └──────────────┬───────────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  prose-polisher/     │
                  │  chapter-writer/     │
                  │  syllabus-planner    │
                  │  （根据评分选择）     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ 再跑 student-qa      │
                  │ 验证改进效果         │
                  └──────────┬──────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
    ┌──────────────────┐       ┌─────────────────────┐
    │ 评分 >= 18        │       │ 评分 < 18           │
    │ 且无阻塞项        │       │ 或仍有阻塞项        │
    │                  │       │                    │
    │ → 进入 release   │       │ → 继续修订回路     │
    │   流程           │       │   （最多3轮）       │
    └────────┬─────────┘       └──────────┬──────────┘
             │                            │
             ▼                            ▼
    ┌────────────────┐          ┌──────────────────┐
    │consistency-edit.│          │ 根据评分选择     │
    └───────┬────────┘          │ polisher/writer/ │
            │                   │ planner          │
            ▼                   └────────┬─────────┘
    ┌───────────────┐                    │
    │  error-fixer   │  ← 修复            │
    │   （如需要）   │    validate_week   │
    └───────┬───────┘    报错            │
            │                            │
            ▼                            │
       ✅ Release                        │
                                         │
                                         │
    ════════════════════════════════════╪══════════
                                        │
    修订回路（最多3轮）：                │
    - 每轮 QA 后根据反馈修订            │
    - 修订后再跑 student-qa             │
    - 直到 >= 18 且无阻塞项 或 达3轮上限 │
    ════════════════════════════════════╧══════════
```

### 质量升级路径

| student-qa 总分 | 处理方式 |
|----------------|---------|
| >= 18/20 | 根据 QA 建议项进行轻量修订（prose-polisher）→ 再 QA → release |
| 14-17/20 | 把具体维度的阻塞项传回 prose-polisher 修复，最多迭代 3 轮 |
| 10-13/20 | 回传 chapter-writer 做结构性重写，可触发 prose-polisher 二次润色 |
| < 10/20 | 回传 syllabus-planner 重新规划章节结构，从头走一遍流水线 |

## Agent 团队（9 个专职角色）

| Agent | 职责 | 关键约束 |
|-------|------|---------|
| `syllabus-planner` | 章节结构 + 贯穿案例 + Bloom 标注 + 回顾桥设计 + 章首导入规划 | 必须输出贯穿案例和超级线规划；所有元数据用 `<!-- -->` 注释 |
| `chapter-writer` | 场景驱动写正文 + 章首导入 + 循环角色 + 回顾桥 | 先读 writing_exemplars.md + characters.yml；先用 Context7 查证技术点 |
| `prose-polisher` | 深度改写 + AI 小专栏（联网搜索） | 三级改写权限；趣味性诊断 |
| `student-qa` | 四维评分 + 知识理解 + 叙事质量审读 | 输出四维评分（总分 >= 18/20） |
| `example-engineer` | 示例代码 + 反例 + PyHelper 超级线代码 | 与贯穿案例关联 |
| `test-designer` | pytest 用例矩阵 | 正例 + 边界 + 反例 |
| `exercise-factory` | 分层作业 + rubric + AI 协作练习 | 基础/进阶/挑战 + 可选 AI 练习 |
| `consistency-editor` | 术语/格式/引用/角色统一 | 对齐 glossary.yml + characters.yml |
| `error-fixer` | 修复校验失败 | 逐条修复再验证 |

## 跨章一致性要求

| 检查项 | 负责 Agent | 检查方式 |
|--------|-----------|---------|
| 循环角色性格一致 | consistency-editor | 对照 `shared/characters.yml` |
| 术语写法统一 | consistency-editor | 对照 `shared/glossary.yml` |
| 新概念数在预算内 | syllabus-planner + validate_week.py | 对照 `shared/concept_map.yml` |
| 回顾桥数量达标 | chapter-writer + validate_week.py | 至少引用前几周的指定数量概念 |
| PyHelper 代码演进连续 | example-engineer | 在上周代码基础上增量修改 |
| AI 融合阶段匹配 | exercise-factory | 对照 `shared/ai_progression.md` |
| 章首导入完整 | consistency-editor | 每章有引言格言 + 时代脉搏段落 |
| 写作元数据已注释 | consistency-editor | 所有规划元数据用 `<!-- -->` 包裹，不在正文渲染 |
| 代码示例符合当前最佳实践 | chapter-writer | 写作前用 Context7 MCP 查证 |
| **参考链接真实性** | prose-polisher + consistency-editor | 所有 URL 必须来自 WebSearch/perplexity MCP 搜索结果或 .research_cache.md，禁止编造 |

## Skill 命令（9 个）

| 命令 | 作用 |
|------|------|
| `/new-week` | 创建新周目录和模板文件 |
| `/draft-chapter` | 完整写作流水线（规划→写→润色→QA→修订回路） |
| `/polish-week` | 对已有章节做深度改写 |
| `/make-assignment` | 生成作业 + 评分标准 |
| `/qa-week` | 单周质量检查 |
| `/release-week` | 发布前闸门检查 |
| `/team-week` | 完整 7 阶段章包流水线（规划→写作→联网研究→润色→产出→QA→发布） |
| `/qa-book` | 跨周一致性检查 |
| `/scaffold-book` | 批量创建 week_01..week_14 |

## Gitea PR 流程（Week 06+ 必做）

分支 → 多次提交 → push → PR → review → merge
参考：`shared/gitea_workflow.md`
