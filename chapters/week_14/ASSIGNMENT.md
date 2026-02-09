# Week 14 作业：整理并发布你的 Python 项目

> "The finish line is just the beginning of a new race."
> — Unknown

## 作业概述

这是全书的最后一周作业——也是一个特殊的作业。你不会写新功能，而是要完成**代码收敛**和**项目发布**。

本周你将：
1. 选择自己这 14 周写的一个项目（建议用 PyHelper 或习惯追踪器）
2. 整理项目结构（删除冗余、统一风格、补全测试）
3. 写 README.md（项目的"门面"）
4. 写 release notes（假设发布 v1.0.0）
5. 用 Git tag 创建版本发布

这不是"练习"，而是**真实的工程实践**——从"能跑的代码"到"可发布的软件"。

---

## 学习目标

完成本周作业后，你将能够：

1. 理解**代码收敛**的概念和步骤（删除冗余、统一风格、补全测试）
2. 撰写专业的 README（让用户 30 秒内了解项目）
3. 写清晰的 release notes（告诉用户"改了什么"）
4. 用 Git tag 做版本发布（语义化版本规范）
5. 回顾全书知识，建立自己的学习地图

---

## 背景知识回顾

### 代码收敛是什么？

代码收敛不是"重写"，而是"整理"：
- **删除冗余**：提取重复代码到公共函数
- **统一风格**：变量命名、导入顺序、代码格式
- **补全测试**：确保核心功能有测试覆盖
- **优化结构**：模块划分清晰，职责单一

### README vs Release Notes

| 文档 | 目的 | 回答的问题 |
|------|------|-----------|
| README | 如何使用 | 这是什么？怎么安装？怎么用？ |
| Release Notes | 这个版本改了什么 | 新增了什么？修复了什么？如何升级？ |

### 语义化版本规范

```
v 主版本.次版本.修订号
  ↓      ↓      ↓
 Major  Minor  Patch
```

- **Major**（主版本）：不兼容的 API 变更（如 v1.x → v2.0）
- **Minor**（次版本）：向后兼容的新功能（如 v1.0 → v1.1）
- **Patch**（修订号）：bug 修复（如 v1.0.0 → v1.0.1）

---

## 练习 1（基础）：代码收敛

### 任务描述

选择你之前写的一个项目（推荐 PyHelper 或习惯追踪器），进行代码收敛：

1. **删除冗余代码**：提取重复逻辑到公共函数
2. **统一代码风格**：变量命名、导入顺序、代码格式
3. **优化项目结构**：模块划分清晰，符合 Python 最佳实践
4. **补全测试**：核心功能至少有一个测试

### 输入

你之前写的项目代码（可能存在以下问题）：

```python
# 可能存在的问题（示例）：
def add_note(data, content):
    if not content or not content.strip():
        raise ValueError("笔记内容不能为空")
    # ... 添加逻辑

def update_note(data, note_id, new_content):
    if not new_content or not new_content.strip():
        raise ValueError("笔记内容不能为空")  # 重复校验

# 导入顺序混乱
import sys
from .storage import save_data
from pathlib import Path
import json
```

### 输出

整理后的项目结构：

```
your_project/
├── your_project/        # 源代码包
│   ├── __init__.py
│   ├── cli.py           # CLI 入口
│   ├── commands/        # 子命令模块
│   ├── models.py        # dataclass 数据模型
│   ├── storage.py       # 数据存储
│   └── utils.py         # 工具函数（公共校验等）
├── tests/               # 测试目录
│   └── test_commands.py
├── examples/            # 示例文件
├── README.md            # 项目说明
└── main.py              # 入口点
```

### 提示与常见错误

**提示**：
- 用 `isort` 自动整理导入顺序（可选）：`pip install isort`
- 用 `black` 自动格式化代码（可选）：`pip install black`
- 删除"死代码"：永远不会被调用的函数
- 提取重复代码：如果同样的逻辑出现 2 次以上，提取成函数

**常见错误**：
- ❌ 删了"暂时没用"的代码，但其实未来会需要（收敛不是重写）
- ❌ 统一风格时改错了逻辑（比如 `if not x` 和 `if x is None` 不一样）
- ❌ 测试写的全是"正常情况"，没测边界情况
- ❌ 只整理了一个文件，其他文件还是老样子（要全局整理）

### 自测检查点

- [ ] 代码中没有明显的重复逻辑（同样代码出现 2 次以上）
- [ ] 变量命名统一（snake_case，不是 camelCase 混用）
- [ ] 导入顺序符合 PEP 8（标准库 → 第三方库 → 本地模块）
- [ ] 核心功能至少有一个测试
- [ ] 项目结构清晰（源代码在包里，测试在单独目录）

### 示例：删除冗余代码

**收敛前**（重复校验）：
```python
def add_note(data, content):
    if not content or not content.strip():
        raise ValueError("笔记内容不能为空")
    # ... 添加逻辑

def update_note(data, note_id, new_content):
    if not new_content or not new_content.strip():
        raise ValueError("笔记内容不能为空")
    # ... 更新逻辑
```

**收敛后**（提取公共函数）：
```python
# utils.py
def validate_content(content: str) -> None:
    """校验笔记内容"""
    if not content or not content.strip():
        raise ValueError("笔记内容不能为空")

# notes.py
from .utils import validate_content

def add_note(data, content):
    validate_content(content)
    # ... 添加逻辑

def update_note(data, note_id, new_content):
    validate_content(new_content)
    # ... 更新逻辑
```

---

## 练习 2（进阶）：写 README.md

### 任务描述

为你的项目写一个专业的 README.md。

### README 的黄金结构

```markdown
# 项目名称（一句话说明）

> 一句话标语（让用户快速理解价值）

## 简介
2-3 句话介绍项目功能和目标用户

## 安装
```bash
# 安装步骤
```

## 快速开始
最简单的使用示例（3-5 行命令）

## 主要功能
- 功能 1：一句话说明
- 功能 2：一句话说明
- 功能 3：一句话说明

## 示例
一个完整的例子（用户能照着跑）

## 配置
如果需要配置文件，说明怎么配置

## 常见问题
用户最常问的 2-3 个问题

## 贡献
如果接受贡献，说明怎么参与

## 许可证
开源协议
```

### 输入

你的项目（可能功能很全，但 README 很简单）

### 输出

一个专业的 README.md（用户能在 30 秒内理解项目）

### 提示与常见错误

**提示**：
- **简洁第一**：用户不应该在 README 里看到长篇大论的技术细节
- **示例可跑**：README 中的示例代码必须能直接复制运行
- **回答三个问题**：这是什么？怎么安装？怎么用？

**常见错误**：
- ❌ 只有一行项目名称，用户不知道这是干什么的
- ❌ 安装步骤太复杂（应该是一条命令搞定）
- ❌ 没有快速示例，用户不知道"怎么用"
- ❌ 示例代码跑不通（最糟糕的错误）
- ❌ 写了太多技术细节（用户不关心你用了什么设计模式）

### 自测检查点

- [ ] README 第一段有项目简介（一句话说明这是什么）
- [ ] 有安装步骤（用户能照着安装）
- [ ] 有快速开始示例（用户能照着运行）
- [ ] 有主要功能列表（用户知道这工具能干什么）
- [ ] 示例代码能跑（复制粘贴不报错）
- [ ] 有常见问题（FAQ）或配置说明

### 示例：PyHelper 的 README（节选）

```markdown
# PyHelper — 你的命令行学习助手

> 记录笔记、管理进度、生成学习计划，一个工具全搞定。

PyHelper 是一个命令行工具，帮你记录 Python 学习笔记、管理学习进度、自动生成学习计划。适合正在学 Python 的初学者使用。

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourname/pyhelper.git
cd pyhelper

# 安装依赖
pip install -e .
```

## 快速开始

```bash
# 添加一条笔记
pyhelper add "今天学了异常处理，try/except 很有用"

# 列出所有笔记
pyhelper list

# 搜索笔记
pyhelper search "异常"
```

## 主要功能

- **笔记管理**：添加、列出、搜索、删除学习笔记
- **进度追踪**：统计学习时长、笔记数量
- **学习计划**：根据笔记自动生成学习计划
- **数据导出**：支持导出为 JSON、CSV、Markdown 格式
```

---

## 练习 3（挑战）：写 Release Notes + Git Tag 发布

### 任务描述

为你的项目写一份专业的 release notes（假设发布 v1.0.0），并用 Git tag 创建版本发布。

### Release Notes 的黄金结构

```markdown
# 版本标题（v1.0.0）

## 发布日期
YYYY-MM-DD

## 主要变化
### 新增功能
- 功能 1
- 功能 2

### 改进
- 改进 1
- 改进 2

### 修复
- 修复 1
- 修复 2

## 安装
```bash
# 安装命令
```

## 快速开始
```bash
# 使用示例
```

## 升级指南
如果需要迁移步骤，说明如何从旧版本升级

## 已知问题
如果存在已知问题，列出

## 致谢
如果有贡献者，感谢
```

### 输入

你的项目（可能功能完整，但没有版本发布）

### 输出

1. **CHANGELOG.md**：版本历史文件
2. **Git tag v1.0.0**：版本标记
3. **Release Notes**：在 GitHub 上创建 Release

### Git Tag 操作步骤

```bash
# 1. 查看当前 commit
git log --oneline -n 3

# 2. 创建带注释的 tag
git tag -a v1.0.0 -m "你的项目 v1.0.0 发布"

# 3. 查看 tag 详情
git show v1.0.0

# 4. 推送 tag 到远程
git push origin v1.0.0

# 5. 在 GitHub 上创建 Release
# 访问：https://github.com/你的用户名/你的项目/releases
# 点击 "Draft a new release"
# 选择 tag v1.0.0，粘贴 release notes
# 点击 "Publish release"
```

### 提示与常见错误

**提示**：
- **这是第一个发布版本**，所以 release notes 里主要写"新增功能"
- **版本号用 v1.0.0**（语义化版本：主版本.次版本.修订号）
- **已知问题**可以写 1-2 个（比如"Windows 上中文可能乱码，计划下个版本修复"）
- **发布日期**用当天日期

**常见错误**：
- ❌ release notes 只写"bug 修复"、"性能优化"（太模糊，要写具体）
- ❌ 没有升级指南（如果这个版本和未来版本不兼容，必须说明如何升级）
- ❌ 写太多技术细节（用户不关心"重构了模块结构"，他们关心"更快了"）
- ❌ 忘记推送 tag（tag 创建后只在本地，GitHub 上看不到）
- ❌ 版本号不规范（如用 `final`、`release` 而不是 `v1.0.0`）

### 自测检查点

- [ ] 创建了 Git tag（`git tag` 能看到 v1.0.0）
- [ ] tag 已推送到远程（`git push origin v1.0.0`）
- [ ] 在 GitHub 上创建了 Release
- [ ] release notes 包含：发布日期、主要变化、安装、快速开始
- [ ] release notes 说明了"新增功能"（不是只写"bug 修复"）
- [ ] 版本号符合语义化规范（v1.0.0）

### 示例：PyHelper v1.0.0 Release Notes（节选）

```markdown
# PyHelper v1.0.0

## 发布日期
2026-02-15

## 主要变化

### 新增功能
- **笔记管理**：添加、列出、搜索、删除学习笔记
- **进度追踪**：统计学习时长、笔记数量、学习天数
- **学习计划**：根据笔记自动生成学习计划（包含前置知识、优先级）
- **数据导出**：支持导出为 JSON、CSV、Markdown 格式
- **命令行界面**：完整的 CLI（argparse），支持子命令和可选参数

### 技术亮点
- 使用 dataclass 定义数据模型（类型安全）
- 完整的 pytest 测试覆盖（核心功能 100% 覆盖）
- logging 日志记录（方便调试）
- 异常处理（优雅处理错误输入）

## 安装

```bash
git clone https://github.com/yourname/pyhelper.git
cd pyhelper
git tag v1.0.0  # 检出 v1.0.0 版本
pip install -e .
```

## 快速开始

```bash
# 添加笔记
pyhelper add "今天学了异常处理"

# 列出笔记
pyhelper list

# 生成学习计划
pyhelper plan generate
```

## 升级指南

这是第一个发布版本，无需升级。

## 已知问题

- Windows 上中文文件名可能显示乱码（计划在 v1.0.1 修复）
- 导出为 CSV 时，超长笔记可能被截断（计划在 v1.1.0 支持 Excel 格式）
```

---

## 练习 4（挑战，可选）：全书知识地图

### 任务描述

回顾这 14 周的学习，画一张自己的**知识地图**。

### 要求

1. **列出你认为最重要的 10 个概念**（从 14 周中选）
2. **为每个概念写一句话说明**（你自己的理解，不是复制定义）
3. **标注你掌握的程度**（熟练/掌握/了解/需要复习）
4. **写 3 条"学完 Python 之后"的学习计划**

### 输出格式

```markdown
# 我的 Python 学习地图

## 核心概念（Top 10）

1. **变量与赋值** — 程序的记忆（熟练）
2. **if/else 控制流** — 让程序做选择（熟练）
3. **for/while 循环** — 重复执行任务（熟练）
4. **函数** — 把问题切小，代码复用（掌握）
5. **列表/字典** — 数据容器（掌握）
6. **异常处理** — 让程序不崩（掌握）
7. **模块化** — 从脚本到项目（掌握）
8. **测试** — 用 pytest 保护代码（了解）
9. **dataclass** — 用数据类建模（了解）
10. **argparse** — 命令行工具（了解）

## 学完 Python 之后

1. **深入 Web 开发**：学习 FastAPI，做一个完整的 Web 应用
2. **学习数据分析**：掌握 Pandas 和 Matplotlib，分析真实数据
3. **参与开源项目**：在 GitHub 上找小项目，从修复 issue 开始
```

### 提示

- 这是**给未来的自己**看的，不是给别人看的
- 不要追求"看起来很厉害"，要诚实标注掌握程度
- "学完 Python 之后"的计划要具体（不要写"继续学习"这种空泛的话）

---

## AI 协作练习（可选）

本周属于 AI 融合的**主导期**（Week 11-14），你可以用 AI 结对编程完成作业。

### 任务

用 AI 工具（如 Claude、ChatGPT、GitHub Copilot）辅助完成以下任务：

1. **生成 README 模板**：让 AI 根据你的项目生成 README 骨架
2. **检查代码风格**：让 AI 帮你检查代码风格一致性问题
3. **生成 release notes 草稿**：让 AI 根据你的 Git commit 历史生成 release notes 草稿

### 审查清单（你必须自己检查）

拿到 AI 生成的内容后，**不要直接提交**，必须逐项检查：

#### README 审查清单

- [ ] **项目简介准确吗？**（AI 可能凭空捏造功能）
- [ ] **安装步骤能跑吗？**（AI 可能假设了不存在的依赖）
- [ ] **示例代码可运行吗？**（复制粘贴试一下）
- [ ] **主要功能列表完整吗？**（AI 可能漏掉重要功能）
- [ ] **常见问题真的"常见"吗？**（AI 可能编造用户不会问的问题）

#### Release Notes 审查清单

- [ ] **版本号正确吗？**（AI 可能用 v1.0 而不是 v1.0.0）
- [ ] **发布日期是今天吗？**（AI 可能用随机日期）
- [ ] **主要变化准确吗？**（AI 可能编造不存在的新功能）
- [ ] **安装命令能跑吗？**（试一下）
- [ ] **已知问题真实吗？**（不要让 AI 编造 bug）

#### 代码风格审查清单

- [ ] **变量命名统一吗？**（AI 可能混用 snake_case 和 camelCase）
- [ ] **导入顺序符合 PEP 8 吗？**
- [ ] **重复代码真的被删除了吗？**（AI 可能说"删除"但实际没删）
- [ ] **测试覆盖了核心功能吗？**（AI 可能只写了"正常情况"的测试）
- [ ] **你能解释每一处改动吗？**（如果解释不了，说明你没理解，不能提交）

### 提交内容

1. AI 生成的内容（保存为 `ai_generated/` 目录）
2. 你修复后的最终版本
3. 审查报告（简短说明）：
   - AI 生成了什么？
   - 你发现了哪些问题？
   - 你做了哪些修改？

### 示例审查报告

```markdown
## AI 协作练习：README 和 Release Notes 审查报告

### AI 生成的内容

1. **README.md**：AI 根据我的项目描述生成了完整的 README
2. **release_notes.md**：AI 根据我的 Git commit 历史生成了 v1.0.0 发布说明

### 发现的问题

#### README 问题
1. AI 编造了一个不存在的功能"自动备份数据到云端"
2. 安装步骤假设了不存在的依赖 `cloud-sdk`
3. 示例代码用了错误的命令名（`pyhelper note` 而不是 `pyhelper add`）

#### Release Notes 问题
1. 版本号用的是 `v1.0` 而不是 `v1.0.0`
2. 发布日期是 `2024-01-01`（不是今天）
3. "主要变化"里列了很多不存在的"改进"

### 我的修改

1. 删除了编造的"云备份"功能
2. 修正了安装步骤，移除不存在的依赖
3. 修正了示例代码的命令名
4. 改版本号为 `v1.0.0`
5. 更新发布日期为今天
6. 删除了不存在的"改进"，只写真实功能

### 学到了什么

- AI 生成的文档需要仔细核对事实（不要假设 AI 正确）
- 版本号和日期这种"看起来很简单"的东西，AI 经常搞错
- 示例代码必须亲自运行验证
```

### 提醒

- **禁止直接复制 AI 输出的内容**。你必须理解并审查。
- 如果 AI 生成了不存在的功能或错误信息，你**必须修复**。
- README 和 release notes 是用户看的东西，错了会误导用户。

---

## 提交要求

### 文件结构

```
chapters/week_14/
├── 你的项目/
│   ├── README.md              # 练习 2：项目说明
│   ├── CHANGELOG.md           # 练习 3：版本历史
│   ├── your_project/          # 练习 1：整理后的源代码
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── commands/
│   │   ├── models.py
│   │   ├── storage.py
│   │   └── utils.py
│   ├── tests/                 # 练习 1：测试
│   │   └── test_commands.py
│   └── examples/              # 使用示例
├── ai_generated/              # AI 协作练习：AI 生成的内容
│   ├── README_ai.md
│   └── release_notes_ai.md
└── ai_review.md               # AI 协作练习：审查报告
```

### 必做（基础 + 进阶）

- [ ] 代码收敛（删除冗余、统一风格、补全测试）
- [ ] 项目结构清晰（符合 Python 最佳实践）
- [ ] README.md（项目说明、安装、使用、示例）
- [ ] 核心功能至少有一个测试

### 加分（挑战）

- [ ] CHANGELOG.md（版本历史）
- [ ] Git tag v1.0.0（版本标记）
- [ ] Release Notes（在 GitHub 上创建 Release）
- [ ] 全书知识地图（Top 10 概念 + 学习计划）

### AI 协作练习（可选）

- [ ] 用 AI 生成 README 模板
- [ ] 用 AI 检查代码风格
- [ ] 用 AI 生成 release notes 草稿
- [ ] 提交审查报告（发现的问题 + 你的修改）

---

## 提示与帮助

### 如果遇到困难

1. **先看教材示例**：CHAPTER.md 中的 PyHelper 案例
2. **参考开源项目**：找一个你喜欢的开源项目，看它的 README 和 release notes
3. **回顾本周内容**：
   - 第 1 节：代码收敛
   - 第 2 节：写 README
   - 第 3 节：写 release notes
   - 第 4 节：Git tag 发布

### 验证命令

```bash
# 检查项目结构
ls -la your_project/

# 运行测试
python3 -m pytest tests/ -v

# 检查 README
cat README.md

# 检查 tag
git tag
git show v1.0.0

# 检查是否推送到远程
git push origin --tags
```

### 常见问题

**Q: 我的项目太简单，值得发布吗？**

A: 值得。发布不是"要做多么厉害的东西"，而是"工程实践的完整流程"。即使是一个简单的命令行工具，经历"收敛 → README → release notes → tag 发布"这个过程，你会学到很多。

**Q: 我没有 GitHub 账号怎么办？**

A: 可以只在本地创建 tag，不需要推送到远程。或者注册一个 GitHub 账号（免费）。

**Q: release notes 要写多长？**

A: 没有"标准长度"。关键是回答"这个版本改了什么"。如果是第一个版本，主要写"新增功能"。如果以后有更新，主要写"和上一版的区别"。

---

## 最后提醒

本周的重点不是"写新代码"，而是**完成一个项目的完整生命周期**：

- 从"能跑的代码"到"可发布的软件"
- 从"自己能看懂"到"别人能看懂"
- 从"本地脚本"到"有版本号的发布"

这是你从"学 Python"到"会做软件"的关键一步。

恭喜你完成了这 14 周的学习之旅！🎉

---

## 附录：评分标准

详见 `RUBRIC.md`。

**简版评分要点**：
- **代码收敛**（30 分）：删除冗余、统一风格、补全测试
- **README**（40 分）：项目说明、安装、使用、示例
- **Release Notes + Tag**（30 分）：版本发布说明、Git tag 操作
- **全书知识地图**（可选，加分）
- **AI 协作练习**（可选，加分）

总分 100 分（不含加分项），最高 120 分（含加分项）。
