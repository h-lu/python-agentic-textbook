"""Week 14 deliverable validation helper tests.

These tests validate local sample deliverable directories only. They do not
require creating or pushing real git tags.
"""

import sys
from pathlib import Path

STARTER = Path(__file__).resolve().parents[1] / "starter_code"
sys.path.insert(0, str(STARTER))
sys.modules.pop("solution", None)

from solution import (
    is_semantic_version,
    parse_semantic_version,
    validate_readme_content,
    validate_release_notes_content,
    validate_sample_deliverable,
)


def test_semantic_version_helpers():
    assert is_semantic_version("v1.0.0") is True
    assert is_semantic_version("1.2.3") is True
    assert is_semantic_version("v1.0") is False
    assert parse_semantic_version("v2.3.4") == (2, 3, 4)


def test_validate_readme_content_reports_missing_sections():
    assert validate_readme_content("# PyHelper\n\n没有更多内容") == [
        "README 缺少 ## 安装",
        "README 缺少 ## 快速开始",
        "README 缺少 ## 主要功能",
        "README 缺少代码块示例",
    ]


def test_validate_release_notes_content_reports_missing_sections():
    issues = validate_release_notes_content("# PyHelper v1.0\n\n## 主要变化\n- 初始版本")
    assert "发布说明标题缺少语义化版本号" in issues
    assert "发布说明缺少 ## 发布日期" in issues
    assert "发布说明缺少 ## 升级指南" in issues


def test_validate_sample_deliverable_accepts_local_project(tmp_path):
    project = tmp_path / "pyhelper_release"
    package = project / "pyhelper"
    tests = project / "tests"
    package.mkdir(parents=True)
    tests.mkdir()

    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "cli.py").write_text("def main():\n    return 0\n", encoding="utf-8")
    (tests / "test_cli.py").write_text("def test_placeholder():\n    assert True\n", encoding="utf-8")
    (project / "README.md").write_text(
        """# PyHelper

## 安装
```bash
pip install -e .
```

## 快速开始
```bash
pyhelper add "学习 Python"
```

## 主要功能
- 笔记管理
""",
        encoding="utf-8",
    )
    (project / "CHANGELOG.md").write_text(
        """# PyHelper v1.0.0

## 发布日期
2026-02-15

## 主要变化
- 初始发布

## 升级指南
这是第一个发布版本，无需升级。
""",
        encoding="utf-8",
    )

    assert validate_sample_deliverable(project) == []


def test_validate_sample_deliverable_reports_missing_files(tmp_path):
    project = tmp_path / "broken"
    project.mkdir()
    issues = validate_sample_deliverable(project)
    assert "缺少 README.md" in issues
    assert "缺少 CHANGELOG.md" in issues
    assert "缺少 tests" in issues
    assert "缺少带 __init__.py 的源代码包" in issues
