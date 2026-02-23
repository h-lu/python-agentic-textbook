---
name: qa-week
description: 三维度质量审查：一致性 + 技术正确性 + 学生视角 QA；输出并收敛 QA_REPORT。
argument-hint: "<week_id e.g. week_01>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task
disable-model-invocation: true
---

# /qa-week

## 用法

```
/qa-week week_XX
```

## 目标

执行**三维度 QA**，确保章包在发布前通过以下检查：
1. **一致性**：术语/锚点/格式/角色对齐
2. **技术正确性**：概念/代码/答案正确 + 教学法对齐
3. **学生视角**：叙事流畅/有趣/可理解

## 步骤

### Stage 1: 并行审读（可同时执行）

**1a. 调用 `consistency-editor`**：
- 对齐 `shared/style_guide.md`
- 同步 `TERMS.yml` -> `shared/glossary.yml`
- 检查循环角色使用一致性（对照 `shared/characters.yml`）
- 修复 `ANCHORS.yml` 问题（依赖 `validate_week.py` 报错定位）
- consistency-editor 内部会跑 `validate_week.py --mode task`

**1b. 调用 `technical-reviewer`**（与 consistency-editor 并行）：
- 审读 `CHAPTER.md`：概念定义准确性、代码示例正确性
- 审读 `examples/`：Python 代码规范（PEP 8）、边界情况处理
- 审读 `ASSIGNMENT.md` + `RUBRIC.md`：题意清晰度、评分覆盖
- 审读 `starter_code/solution.py`：答案正确性
- 输出问题清单（按 S1-S4 严重级别分类）

### Stage 2: 学生视角 QA

调用 `student-qa`：
- 四维评分（叙事流畅度/趣味性/知识覆盖/认知负荷，各 1-5 分）
- 总分 >= 18/20 才能 release
- 任一维度 <= 2 视为阻塞项

### Stage 3: 收敛 QA_REPORT

把三维度 QA 结果收敛到 `QA_REPORT.md`：

```markdown
# QA Report: week_XX

## 总体状态
- [ ] 一致性检查通过
- [ ] 技术审读通过（S1-S4 问题已清零）
- [ ] 学生视角评分 >= 18/20

## 四维评分
| 维度 | 分数 | 说明 |
|------|------|------|
| 叙事流畅度 | X/5 | ... |
| 趣味性 | X/5 | ... |
| 知识覆盖 | X/5 | ... |
| 认知负荷 | X/5 | ... |
| **总分** | **X/20** | |

## 技术审读问题

### S1 致命问题（必须修复）
- [ ] {问题描述}

### S2 重要问题（强烈建议修复）
- [ ] {问题描述}

### S3 一般问题（建议修复）
- [ ] {问题描述}

## 一致性问题
- [ ] {问题描述}

## 学生视角阻塞项
- [ ] {问题描述}

## 建议项
- [ ] {改进建议}
```

### Stage 4: Release 验证

最终 release 级验证：
```bash
python3 scripts/validate_week.py --week week_XX --mode release
```

## 发布条件

| 条件 | 要求 |
|------|------|
| 一致性 | 全部通过 |
| S1 问题 | **必须清零** |
| S2 问题 | **必须清零** |
| S3 问题 | **必须清零** |
| S4 问题 | **必须清零** |
| 四维总分 | >= 18/20 |
| 校验脚本 | `--mode release` 通过 |
