"""pytest 配置和 fixture

为 Week 14 的测试提供共享的 fixtures。
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_project_dir():
    """创建一个临时项目目录，用于测试项目结构

    Yields:
        Path: 临时目录的路径对象
    """
    # 创建临时目录
    temp_dir = Path(tempfile.mkdtemp())

    yield temp_dir

    # 清理临时目录
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_readme_content():
    """提供一个标准的 README 内容示例

    Returns:
        str: README 文件的内容
    """
    return """# PyHelper — 你的命令行学习助手

> 记录笔记、管理进度、生成学习计划，一个工具全搞定。

PyHelper 是一个命令行工具，帮你记录 Python 学习笔记、管理学习进度、自动生成学习计划。适合正在学 Python 的初学者使用。

## 安装

```bash
git clone https://github.com/yourname/pyhelper.git
cd pyhelper
pip install -e .
```

## 快速开始

```bash
pyhelper add "今天学了异常处理"
pyhelper list
pyhelper search "异常"
```

## 主要功能

- **笔记管理**：添加、列出、搜索、删除学习笔记
- **进度追踪**：统计学习时长、笔记数量
- **学习计划**：根据笔记自动生成学习计划
- **数据导出**：支持导出为 JSON、CSV、Markdown 格式

## 示例

```bash
pyhelper add "学了 dataclass，用 @dataclass 装饰器定义数据类"
pyhelper stats
pyhelper plan generate
```

## 常见问题

**Q: 数据会丢失吗？**
A: 不会。所有数据保存在本地 `~/.pyhelper/` 目录。

## 许可证

MIT License
"""


@pytest.fixture
def sample_release_notes_content():
    """提供一个标准的 release notes 内容示例

    Returns:
        str: release notes 文件的内容
    """
    return """# PyHelper v1.0.0

## 发布日期
2026-02-15

## 主要变化

### 新增功能
- **笔记管理**：添加、列出、搜索、删除学习笔记
- **进度追踪**：统计学习时长、笔记数量、学习天数
- **学习计划**：根据笔记自动生成学习计划（包含前置知识、优先级、估算时长）
- **数据导出**：支持导出为 JSON、CSV、Markdown 格式
- **命令行界面**：完整的 CLI（argparse），支持子命令和可选参数

### 技术亮点
- 使用 dataclass 定义数据模型（类型安全）
- 完整的 pytest 测试覆盖（核心功能 100% 覆盖）
- logging 日志记录（方便调试）
- 异常处理（优雅处理错误输入）

## 升级指南

这是第一个发布版本，无需升级。

## 已知问题

- Windows 上中文文件名可能显示乱码（计划在 v1.0.1 修复）
"""


@pytest.fixture
def valid_project_structure(temp_project_dir):
    """创建一个符合 Python 最佳实践的项目结构

    Args:
        temp_project_dir: 临时目录 fixture

    Returns:
        Path: 项目根目录
    """
    # 创建标准 Python 项目结构
    (temp_project_dir / "pyhelper").mkdir()
    (temp_project_dir / "pyhelper" / "__init__.py").write_text("")
    (temp_project_dir / "pyhelper" / "cli.py").write_text("# CLI 入口")
    (temp_project_dir / "pyhelper" / "models.py").write_text("# 数据模型")
    (temp_project_dir / "pyhelper" / "storage.py").write_text("# 存储")

    (temp_project_dir / "tests").mkdir()
    (temp_project_dir / "tests" / "__init__.py").write_text("")
    (temp_project_dir / "tests" / "test_commands.py").write_text("# 测试")

    (temp_project_dir / "examples").mkdir()
    (temp_project_dir / "README.md").write_text("# PyHelper\n\n项目说明")
    (temp_project_dir / "CHANGELOG.md").write_text("# 版本历史")
    (temp_project_dir / "pyproject.toml").write_text("[project]\nname = 'pyhelper'")

    return temp_project_dir


@pytest.fixture
def invalid_project_structure(temp_project_dir):
    """创建一个不符合规范的项目结构（用于测试）

    Args:
        temp_project_dir: 临时目录 fixture

    Returns:
        Path: 项目根目录
    """
    # 创建混乱的项目结构
    (temp_project_dir / "main.py").write_text("# 主程序")
    (temp_project_dir / "notes.py").write_text("# 笔记")
    (temp_project_dir / "storage.py").write_text("# 存储")
    # 没有 tests 目录
    # 没有 README
    # 文件散落在根目录

    return temp_project_dir
