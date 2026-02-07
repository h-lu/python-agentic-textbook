---
name: qa-week
description: 质量审查：术语/锚点/格式一致性 + 学生视角 QA；输出并收敛 QA_REPORT。
argument-hint: "<week_id e.g. week_01>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: true
---

# /qa-week

## 用法

```
/qa-week week_XX
```

## 步骤

1. 调用 `consistency-editor`：
   - 对齐 `shared/style_guide.md`
   - 同步 `TERMS.yml` -> `shared/glossary.yml`
   - 清理 `ANCHORS.yml` 字段与重复 id
2. 调用 `student-qa`：再次审读，输出阻塞项/建议项。
3. 把 QA 结果收敛到 `QA_REPORT.md`，并把阻塞项清零（不允许存在 `- [ ]`）。
4. 验证：
   ```bash
   python3 scripts/validate_week.py --week week_XX --mode release
   ```
