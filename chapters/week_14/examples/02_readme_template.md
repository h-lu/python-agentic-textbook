# PyHelper — 你的命令行学习助手

> 记录笔记、管理进度、生成学习计划，一个工具全搞定。

## 简介

PyHelper 是一个命令行工具，帮你记录 Python 学习笔记、管理学习进度、自动生成学习计划。适合正在学 Python 的初学者使用。

## 安装

### 从 GitHub 克隆

```bash
git clone https://github.com/yourname/pyhelper.git
cd pyhelper
pip install -e .
```

### 使用 pip 安装（如果发布到 PyPI）

```bash
pip install pyhelper
```

## 快速开始

```bash
# 添加一条笔记
pyhelper add "今天学了异常处理，try/except 很有用"

# 列出所有笔记
pyhelper list

# 搜索笔记
pyhelper search "异常"

# 生成学习计划
pyhelper plan generate

# 查看统计信息
pyhelper stats
```

## 主要功能

- **笔记管理**：添加、列出、搜索、删除学习笔记
- **进度追踪**：统计学习时长、笔记数量、学习天数
- **学习计划**：根据笔记自动生成学习计划（包含前置知识、优先级、估算时长）
- **数据导出**：支持导出为 JSON、CSV、Markdown 格式
- **命令行界面**：完整的 CLI（argparse），支持子命令和可选参数

## 示例

### 记录今天的学习

```bash
$ pyhelper add "学了 dataclass，用 @dataclass 装饰器定义数据类"
✓ 笔记已添加：20250209-143022
  内容：学了 dataclass，用 @dataclass 装饰器定义数据类...

$ pyhelper add "学了 argparse，能做命令行工具了"
✓ 笔记已添加：20250209-143123
  内容：学了 argparse，能做命令行工具了...
```

### 查看学习统计

```bash
$ pyhelper stats
PyHelper 统计
============================================================
总笔记数：15
  - 草稿：10
  - 已发布：5
  - 已归档：0

热门标签：
  - 异常处理: 3
  - 函数: 4
  - 文件: 2
```

### 生成学习计划

```bash
$ pyhelper plan generate --output plan.json
[INFO] 读取笔记:notes/week06.md
[INFO] 分析结果:Week 6 - 异常处理
[INFO] 主题:['异常处理']
[INFO] 难度:medium
...
✓ 学习计划已生成:plan.json
  共 14 周
  总时长:98 小时
```

### 搜索笔记

```bash
$ pyhelper search "异常"
找到 3 条匹配笔记：
============================================================
[20250209-101522] 今天学了异常处理，try/except 很有用...
     标签：异常处理, 错误处理
[20250208-093045] 异常处理最佳实践：不要捕获所有异常...
     标签：异常处理, 最佳实践
[20250207-152233] 常见异常类型：ValueError, TypeError...
     标签：异常处理
```

## 配置

PyHelper 的数据存储在 `~/.pyhelper/` 目录下：

- `notes.json`：笔记数据
- `plan.json`：学习计划
- `pyhelper.log`：日志文件

## 命令参考

### add - 添加笔记

```bash
pyhelper add "笔记内容" [--tags 标签1 标签2]
```

### list - 列出笔记

```bash
pyhelper list [--pending] [--published]
```

### search - 搜索笔记

```bash
pyhelper search "关键词"
```

### export - 导出笔记

```bash
pyhelper export --format json --output backup.json
pyhelper export --format csv --output backup.csv
```

### stats - 统计信息

```bash
pyhelper stats [--json]
```

### plan - 学习计划

```bash
pyhelper plan generate [--notes-dir 目录] [--output 文件]
pyhelper plan show --week 6
```

## 常见问题

### Q: 数据会丢失吗？

A: 不会。所有数据保存在本地 `~/.pyhelper/` 目录，你可以随时备份。

### Q: 支持中文吗？

A: 支持。PyHelper 使用 UTF-8 编码，完全支持中文。

### Q: 如何升级？

A: 运行 `git pull` 更新代码，数据文件不会受影响。

### Q: 如何备份笔记？

A: 使用 `pyhelper export --format json --output backup.json` 导出备份。

### Q: Windows 上能用吗？

A: 可以。PyHelper 是纯 Python 实现，跨平台兼容。

## 贡献

欢迎贡献！请先 [提 Issue](https://github.com/yourname/pyhelper/issues) 讨论你的想法。

贡献流程：
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

MIT License

## 致谢

感谢《Python 程序设计（Agentic Coding）》教材的陪伴，让我从零学会了 Python。

## 联系方式

- 作者：Your Name
- GitHub：https://github.com/yourname/pyhelper
- Issues：https://github.com/yourname/pyhelper/issues
