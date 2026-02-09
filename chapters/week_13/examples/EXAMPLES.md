# Week 13 示例代码说明

本目录包含 Week 13 "用 AI Agent 协作开发" 的所有示例代码。

## 示例列表

### 1. Reader + Writer 基础流程

**文件**: `01_reader_writer.py`

演示最简单的 agent team 模式：
- `ReaderAgent`: 读取并分析笔记文件
- `WriterAgent`: 根据笔记信息生成学习计划
- 使用 dataclass 定义 agent 消息格式

运行:
```bash
python3 chapters/week_13/examples/01_reader_writer.py
```

---

### 2. Reader + Writer + Tester 完整流程

**文件**: `01_reader_writer_tester.py`

在 reader + writer 基础上添加 tester agent：
- `ReaderAgent`: 读取并分析笔记文件
- `WriterAgent`: 生成学习计划
- `TesterAgent`: 测试学习计划是否合理
- 演示消息链：reader → writer → tester

运行:
```bash
python3 chapters/week_13/examples/01_reader_writer_tester.py
```

---

### 3. Review Checklist - 基本检查

**文件**: `02_review_checklist.py`

演示如何审查 AI 生成的代码：
- `ReviewerAgent`: 检查代码质量
- checklist: 错误处理、日志、文档、类型提示
- 对比"坏代码"和"好代码"的审查结果

运行:
```bash
python3 chapters/week_13/examples/02_review_checklist.py
```

---

### 4. Review Checklist - 边界情况检查

**文件**: `02_checklist_edge_cases.py`

演示如何检查边界情况处理：
- 检查文件存在性
- 检查空输入
- 检查异常处理
- 检查除零风险

运行:
```bash
python3 chapters/week_13/examples/02_checklist_edge_cases.py
```

---

### 5. 失败驱动迭代

**文件**: `03_failure_driven_iteration.py`

演示失败驱动迭代的核心概念：
- `WriterAgent`: 根据反馈修复学习计划
- `ReviewerAgent`: 检查计划质量
- 迭代循环：最多 3 次，失败后修复再检查

运行:
```bash
python3 chapters/week_13/examples/03_failure_driven_iteration.py
```

---

### 6. 完整的 Agent Team 流程

**文件**: `03_full_agent_team.py`

演示完整的 agent team 流水线：
- `ReaderAgent`: 读取并分析笔记
- `WriterAgent`: 生成学习计划（支持迭代）
- `ReviewerAgent`: 检查计划质量
- 完整流程：reader → writer → reviewer (迭代)

运行:
```bash
python3 chapters/week_13/examples/03_full_agent_team.py
```

---

### 7. PyHelper 集成示例

**文件**: `13_pyhelper_agent_team.py`

将 agent team 集成到 PyHelper 项目中：
- 使用 dataclass 定义消息格式
- Reader/Writer/Reviewer agent 完整实现
- 支持导出 JSON 格式的学习计划
- 包含 logging 日志记录
- 可集成到 CLI 命令

运行:
```bash
python3 chapters/week_13/examples/13_pyhelper_agent_team.py
```

---

## 知识点总结

### 核心概念

1. **Agent Team 模式**
   - 多个 agent 各司其职
   - 职责单一：每个 agent 只做一件事
   - 消息传递：agent 的输出是下一个的输入

2. **Dataclass 消息格式**
   - 使用 `@dataclass` 定义数据结构
   - agent 之间的"协议"
   - 类型提示让接口清晰

3. **Review Checklist**
   - 定义"什么算好代码"
   - 检查项：错误处理、日志、文档、边界情况
   - 可定制：根据需要开关检查项

4. **失败驱动迭代**
   - 反馈循环：测试失败 → 修复 → 再测试
   - 最大迭代次数：避免无限循环
   - 基于反馈的修复

### 与之前知识的联系

- **Week 03 函数分解**: 每个 agent 是一个函数，职责单一
- **Week 06 异常处理**: try/except 处理文件读取错误
- **Week 08 TDD 循环**: 红-绿-重构，与失败驱动迭代类似
- **Week 10 JSON 序列化**: 导出学习计划为 JSON
- **Week 11 Dataclass**: 定义消息格式
- **Week 12 Logging**: 记录 agent 协作过程

---

## 测试

所有示例都可以独立运行。要运行完整的测试套件：

```bash
python3 -m pytest chapters/week_13/tests -q
```

---

## 扩展建议

1. 添加更多 agent：
   - `TesterAgent`: 自动生成 pytest 测试
   - `DocAgent`: 生成文档字符串
   - `RefactorAgent`: 代码重构

2. 改进现有 agent：
   - 用 AI/NLP 分析笔记内容
   - 更智能的前置知识推断
   - 更精确的时长估算

3. 集成到 PyHelper CLI：
   - `pyhelper plan generate`: 生成学习计划
   - `pyhelper plan show --week N`: 查看某周计划
   - `pyhelper plan export --format json`: 导出计划
