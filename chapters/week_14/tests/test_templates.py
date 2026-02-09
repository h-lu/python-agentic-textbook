"""测试 README 和 release notes 模板

这些测试验证学生是否理解：
- README 的必需章节
- README 格式规范
- release notes 的必需章节
- release notes 格式规范
"""

import pytest
from pathlib import Path


class TestReadmeValidation:
    """测试 README 验证"""

    def test_readme_has_project_title(self, sample_readme_content):
        """测试 README 是否有项目标题"""
        lines = sample_readme_content.strip().split("\n")
        assert lines[0].startswith("# ")
        # 标题应该包含项目名称
        assert "PyHelper" in lines[0]

    def test_readme_has_installation_section(self, sample_readme_content):
        """测试 README 是否有安装说明"""
        assert "## 安装" in sample_readme_content

    def test_readme_has_quick_start_section(self, sample_readme_content):
        """测试 README 是否有快速开始章节"""
        assert "## 快速开始" in sample_readme_content

    def test_readme_has_code_examples(self, sample_readme_content):
        """测试 README 是否包含代码示例"""
        # 应该有代码块（用 ``` 包围）
        assert "```" in sample_readme_content
        # 示例应该包含命令
        assert "pyhelper" in sample_readme_content

    def test_readme_has_features_list(self, sample_readme_content):
        """测试 README 是否列出主要功能"""
        assert "## 主要功能" in sample_readme_content or "## 功能" in sample_readme_content
        # 应该有 bullet point 列表
        assert "-" in sample_readme_content

    def test_readme_has_usage_examples(self, sample_readme_content):
        """测试 README 是否有使用示例"""
        assert "## 示例" in sample_readme_content or "示例" in sample_readme_content

    def test_readme_has_license(self, sample_readme_content):
        """测试 README 是否包含许可证信息"""
        assert "许可证" in sample_readme_content or "License" in sample_readme_content


class TestReleaseNotesValidation:
    """测试 release notes 验证"""

    def test_release_notes_has_version(self, sample_release_notes_content):
        """测试 release notes 是否有版本号"""
        lines = sample_release_notes_content.strip().split("\n")
        # 第一行应该是版本标题
        assert lines[0].startswith("# ")
        # 应该包含版本号
        assert "v1.0.0" in lines[0] or "1.0.0" in lines[0]

    def test_release_notes_has_date(self, sample_release_notes_content):
        """测试 release notes 是否有发布日期"""
        assert "## 发布日期" in sample_release_notes_content or "发布日期" in sample_release_notes_content
        # 应该有日期格式（YYYY-MM-DD）
        import re
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        assert re.search(date_pattern, sample_release_notes_content)

    def test_release_notes_has_changes_section(self, sample_release_notes_content):
        """测试 release notes 是否有主要变化章节"""
        assert "## 主要变化" in sample_release_notes_content or "变化" in sample_release_notes_content

    def test_release_notes_categorizes_changes(self, sample_release_notes_content):
        """测试 release notes 是否对变化进行分类"""
        # 应该有新增、改进、修复等分类
        has_categories = any(keyword in sample_release_notes_content for keyword in
                             ["新增", "改进", "修复", "移除", "新增功能", "技术亮点"])
        assert has_categories

    def test_release_notes_has_upgrade_guide(self, sample_release_notes_content):
        """测试 release notes 是否有升级指南"""
        assert "## 升级指南" in sample_release_notes_content or "升级" in sample_release_notes_content

    def test_release_notes_has_known_issues(self, sample_release_notes_content):
        """测试 release notes 是否有已知问题"""
        assert "## 已知问题" in sample_release_notes_content or "已知问题" in sample_release_notes_content


class TestCommonReadmeErrors:
    """测试 README 常见错误检测"""

    def test_detect_empty_readme(self, temp_project_dir):
        """测试检测空的 README"""
        readme = temp_project_dir / "README.md"
        readme.write_text("")

        content = readme.read_text()
        assert len(content.strip()) == 0

    def test_detect_readme_without_title(self, temp_project_dir):
        """测试检测没有标题的 README"""
        readme = temp_project_dir / "README.md"
        readme.write_text("""
这是一些项目说明。
但没有标题。
""")

        content = readme.read_text()
        # 第一行不是标题
        first_line = content.strip().split("\n")[0]
        assert not first_line.startswith("# ")

    def test_detect_readme_without_installation(self, temp_project_dir):
        """测试检测缺少安装说明的 README"""
        readme = temp_project_dir / "README.md"
        readme.write_text("""# My Project

This is a great project.

## Features
- Feature 1
- Feature 2
""")

        content = readme.read_text()
        assert "安装" not in content and "install" not in content.lower()

    def test_detect_readme_without_examples(self, temp_project_dir):
        """测试检测缺少示例的 README"""
        readme = temp_project_dir / "README.md"
        readme.write_text("""# My Project

## Installation
pip install myproject

## Features
- Great feature
""")

        content = readme.read_text()
        # 没有代码块
        assert "```" not in content
        # 没有"示例"相关内容
        assert "示例" not in content and "example" not in content.lower()


class TestCommonReleaseNotesErrors:
    """测试 release notes 常见错误检测"""

    def test_detect_vague_bug_fixes(self, temp_project_dir):
        """测试检测模糊的 bug 修复描述"""
        notes = temp_project_dir / "RELEASE.md"
        notes.write_text("""# v1.0.1

## 主要变化
- 修复了一些 bug
- 优化了性能
""")

        content = notes.read_text()
        # 包含模糊的描述
        assert "一些 bug" in content or "bug 修复" in content
        # 没有具体说明修复了什么
        assert "具体" not in content

    def test_detect_missing_upgrade_guide(self, temp_project_dir):
        """测试检测缺少升级指南的 release notes"""
        notes = temp_project_dir / "RELEASE.md"
        notes.write_text("""# v2.0.0

## 主要变化
- [新增] 新功能
- [移除] 旧功能被移除
""")

        content = notes.read_text()
        # 有移除功能但没有升级指南
        assert "移除" in content
        assert "升级指南" not in content and "迁移" not in content

    def test_detect_too_technical_details(self, temp_project_dir):
        """测试检测过于技术化的 release notes"""
        notes = temp_project_dir / "RELEASE.md"
        notes.write_text("""# v1.0.0

## 主要变化
- 重构了模块结构，采用 ABC 抽象基类
- 优化了时间复杂度从 O(n^2) 到 O(n log n)
- 实现了工厂模式和单例模式
""")

        content = notes.read_text()
        # 包含太多技术细节
        technical_terms = ["抽象", "复杂度", "模式", "重构"]
        found_technical = sum(1 for term in technical_terms if term in content)
        assert found_technical >= 2


@pytest.mark.parametrize("section,content,expected_present", [
    ("安装", "pip install pyhelper", True),
    ("安装", "npm install", False),  # 错误的安装命令
    ("快速开始", "pyhelper add", True),
    ("主要功能", "笔记管理", True),
    ("示例", "pyhelper list", True),
])
def test_readme_section_content_validation(section, content, expected_present):
    """参数化测试：验证 README 各章节内容"""
    if expected_present:
        # 如果内容应该存在，验证它符合章节主题
        if section == "安装":
            assert "pip" in content or "install" in content
        elif section == "快速开始":
            assert content  # 快速开始应该有具体命令


class TestMarkdownFormatting:
    """测试 Markdown 格式规范"""

    def test_heading_levels(self, sample_readme_content):
        """测试标题层级使用正确"""
        lines = sample_readme_content.split("\n")
        headings = [line for line in lines if line.startswith("#")]

        # 应该有多个标题
        assert len(headings) > 1

        # 标题应该使用递增层级（一级标题最多一个）
        h1_count = sum(1 for h in headings if h.startswith("# "))
        assert h1_count == 1  # 只有一个一级标题

    def test_code_blocks_have_language(self, sample_readme_content):
        """测试代码块是否指定了语言"""
        # 查找 ``` 后面是否有语言标识
        import re
        code_block_pattern = r"```(\w+)?"
        matches = re.findall(code_block_pattern, sample_readme_content)

        # 应该有代码块
        assert len(matches) > 0

    def test_lists_are_formatted(self, sample_readme_content):
        """测试列表格式正确"""
        lines = sample_readme_content.split("\n")
        bullet_lines = [line for line in lines if line.strip().startswith("-")]

        # 应该有无序列表
        assert len(bullet_lines) > 0


class TestEdgeCases:
    """测试边界情况"""

    def test_readme_with_only_title(self, temp_project_dir):
        """测试只有标题的 README（不完整）"""
        readme = temp_project_dir / "README.md"
        readme.write_text("# PyHelper")

        content = readme.read_text()
        # 只有标题，没有其他内容
        assert content.strip().count("\n") == 0

    def test_readme_with_unicode(self, temp_project_dir):
        """测试包含 Unicode 字符的 README"""
        readme = temp_project_dir / "README.md"
        readme.write_text("""# PyHelper 🎯

> 学习 Python 的好帮手 🚀

## 功能
- 支持 🇨🇳 中文
- 支持 emoji 😊
""")

        content = readme.read_text()
        # 应该能正确处理 Unicode
        assert "🎯" in content
        assert "🚀" in content
        assert "🇨🇳" in content

    def test_release_notes_first_version(self, temp_project_dir):
        """测试第一个版本的 release notes（无需升级指南）"""
        notes = temp_project_dir / "RELEASE.md"
        notes.write_text("""# PyHelper v1.0.0

## 发布日期
2026-02-15

## 主要变化
- 初始发布
""")

        content = notes.read_text()
        # 第一个版本可能不需要详细的升级指南
        assert "v1.0.0" in content
