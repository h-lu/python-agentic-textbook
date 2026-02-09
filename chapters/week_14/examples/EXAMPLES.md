# Week 14 示例代码清单

本目录包含 Week 14（Capstone 发布与总结）的所有示例代码。

## 示例清单

### 1. 01_convergence.py - 代码收敛示例

**演示内容**：
- 删除冗余代码（提取公共函数）
- 统一代码风格（snake_case 命名、类型提示、docstring）
- 优化导入结构（标准库 → 第三方 → 本地）

**运行方式**：
```bash
python3 chapters/week_14/examples/01_convergence.py
```

**输出**：
展示收敛前后的代码对比，说明改进点

**对应章节**：
- 第 1 节：代码需要"收个尾"——整理项目结构

---

### 2. 02_readme_template.md - README 模板

**演示内容**：
- 完整的 README 结构
- 项目说明、安装指南、快速开始
- 命令参考、常见问题、贡献指南

**使用方式**：
复制模板，根据实际项目修改内容

**对应章节**：
- 第 2 节：项目的"门面"——写专业的 README

---

### 3. 03_release_notes_template.md - Release Notes 模板

**演示内容**：
- 完整的 release notes 结构
- 主要变化、升级指南、已知问题
- 依赖项、性能、安全信息

**使用方式**：
复制模板，根据实际版本修改内容

**对应章节**：
- 第 3 节：告诉用户"改了什么"——写 release notes

---

### 4. 14_pyhelper_v1.py - PyHelper v1.0.0 最终版本

**演示内容**：
本书超级线的终点：整合 14 周所有核心知识
- Week 11: dataclass 数据模型（Note, NoteStatus, StudyPlan）
- Week 10: JSON 存储（序列化/反序列化）
- Week 12: argparse CLI（子命令、参数解析、退出码）
- Week 12: logging 日志（级别、格式、文件）
- Week 06: 异常处理（try/except、优雅降级）
- Week 13: agent team（reader/writer 协作）

**功能清单**：
- `add`: 添加学习笔记
- `list`: 列出笔记（支持过滤）
- `search`: 搜索笔记（关键词）
- `export`: 导出笔记（JSON/CSV/Markdown）
- `stats`: 统计信息
- `plan generate`: 生成学习计划（agent team）
- `plan show`: 显示学习计划

**运行方式**：
```bash
# 添加笔记
python3 chapters/week_14/examples/14_pyhelper_v1.py add "今天学了代码收敛"

# 列出笔记
python3 chapters/week_14/examples/14_pyhelper_v1.py list

# 搜索笔记
python3 chapters/week_14/examples/14_pyhelper_v1.py search "代码"

# 导出笔记
python3 chapters/week_14/examples/14_pyhelper_v1.py export --format json --output backup.json

# 统计信息
python3 chapters/week_14/examples/14_pyhelper_v1.py stats

# 生成学习计划
python3 chapters/week_14/examples/14_pyhelper_v1.py plan generate --notes-dir notes --output plan.json

# 显示学习计划
python3 chapters/week_14/examples/14_pyhelper_v1.py plan show --week 6
```

**预期输出**：
- 不同子命令执行对应功能
- 日志记录到 `~/.pyhelper/pyhelper.log`
- 返回正确的退出码（0=成功，1=失败）

**对应章节**：
- 全章贯穿案例：PyHelper v1.0.0 最终发布版本

**技术栈**：
```python
# 数据模型（Week 11）
@dataclass
class Note:
    id: str
    content: str
    tags: List[str]
    created_at: str
    status: NoteStatus

# 存储（Week 10）
import json
def load_notes() -> List[Note]:
    # JSON 反序列化
    ...

# CLI（Week 12）
import argparse
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# 日志（Week 12）
import logging
logging.basicConfig(filename=log_file)

# 异常处理（Week 06）
try:
    ...
except Exception as e:
    logger.error(f"操作失败：{e}")
    return 1
```

**目录结构**：
```
~/.pyhelper/
├── notes.json       # 笔记数据
├── plan.json        # 学习计划
└── pyhelper.log     # 日志文件
```

---

## 知识点覆盖

| 周次 | 知识点 | 示例文件 |
|------|--------|----------|
| Week 06 | 异常处理（try/except） | 14_pyhelper_v1.py |
| Week 07 | 模块化（import） | 14_pyhelper_v1.py |
| Week 10 | JSON 序列化 | 14_pyhelper_v1.py |
| Week 11 | dataclass | 14_pyhelper_v1.py |
| Week 12 | argparse CLI | 14_pyhelper_v1.py |
| Week 12 | logging 日志 | 14_pyhelper_v1.py |
| Week 13 | agent team | 14_pyhelper_v1.py |
| Week 14 | 代码收敛 | 01_convergence.py |
| Week 14 | README | 02_readme_template.md |
| Week 14 | release notes | 03_release_notes_template.md |

---

## 测试建议

### 测试 01_convergence.py
```bash
python3 chapters/week_14/examples/01_convergence.py
```
应该输出收敛前后的对比说明和测试结果。

### 测试 14_pyhelper_v1.py

#### 1. 添加笔记
```bash
python3 chapters/week_14/examples/14_pyhelper_v1.py add "今天学了代码收敛" --tags Python 工程化
```
预期：显示"✓ 笔记已添加：..."

#### 2. 列出笔记
```bash
python3 chapters/week_14/examples/14_pyhelper_v1.py list
```
预期：显示所有笔记列表

#### 3. 搜索笔记
```bash
python3 chapters/week_14/examples/14_pyhelper_v1.py search "代码"
```
预期：显示包含"代码"的笔记

#### 4. 导出笔记
```bash
python3 chapters/week_14/examples/14_pyhelper_v1.py export --format json --output /tmp/test_backup.json
```
预期：显示"✓ 已导出 N 条笔记到 /tmp/test_backup.json"

#### 5. 统计信息
```bash
python3 chapters/week_14/examples/14_pyhelper_v1.py stats
```
预期：显示统计信息（总笔记数、各状态数量、热门标签）

#### 6. 生成学习计划
```bash
# 先创建测试笔记目录
mkdir -p /tmp/test_notes
echo "# Week 06: 异常处理" > /tmp/test_notes/week06.md

python3 chapters/week_14/examples/14_pyhelper_v1.py plan generate --notes-dir /tmp/test_notes --output /tmp/test_plan.json
```
预期：显示"✓ 学习计划已生成"

#### 7. 查看帮助
```bash
python3 chapters/week_14/examples/14_pyhelper_v1.py --help
python3 chapters/week_14/examples/14_pyhelper_v1.py add --help
```
预期：显示帮助信息

---

## 清理测试数据

```bash
# 清理 PyHelper 数据
rm -rf ~/.pyhelper/

# 清理测试文件
rm -f /tmp/test_backup.json
rm -f /tmp/test_plan.json
rm -rf /tmp/test_notes
```

---

## 从 Week 01 到 Week 14 的演进

```
Week 01: print("Hello PyHelper!")
Week 02: input() + if/else 根据心情推荐
Week 03: 函数拆分 + 菜单
Week 04: 字典存储笔记
Week 05: 文件持久化
Week 06: 异常处理
Week 07: 模块化拆分
Week 08: pytest 测试
Week 09: 搜索和过滤
Week 10: JSON 格式
Week 11: dataclass 建模
Week 12: argparse CLI
Week 13: agent team 协作
Week 14: v1.0.0 发布 ← 这里！
```

恭喜你完成了 14 周的学习之旅！🎉
