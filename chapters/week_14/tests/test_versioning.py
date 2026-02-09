"""测试语义化版本规范

这些测试验证学生是否理解：
- 语义化版本格式（MAJOR.MINOR.PATCH）
- 版本号比较
- 版本号递增规则
- Git tag 命令理解
"""

import pytest
import re
from typing import Tuple


class TestSemanticVersionFormat:
    """测试语义化版本格式"""

    @pytest.mark.parametrize("version_string,expected_valid", [
        ("v1.0.0", True),
        ("1.0.0", True),
        ("v2.1.3", True),
        ("10.20.30", True),
        ("0.0.1", True),
        ("v1.0", False),  # 缺少 PATCH
        ("1.0", False),
        ("v1", False),  # 只有 MAJOR
        ("1", False),
        ("v1.0.0.0", False),  # 超过三部分
        ("v1.0.0-beta", False),  # 包含预发布标识（暂不测试）
        ("", False),  # 空字符串
        ("abc", False),  # 非版本号
        ("v1.0.", False),  # 缺少 PATCH
        ("v.1.0.0", False),  # 格式错误
    ])
    def test_semantic_version_format(self, version_string, expected_valid):
        """测试各种版本号格式的有效性"""
        # 语义化版本正则表达式
        pattern = r"^v?(\d+)\.(\d+)\.(\d+)$"
        match = re.match(pattern, version_string)

        is_valid = match is not None
        assert is_valid == expected_valid

    def test_extract_version_components(self):
        """测试提取版本号的三个部分"""
        version = "v1.2.3"
        pattern = r"^v?(\d+)\.(\d+)\.(\d+)$"
        match = re.match(pattern, version)

        assert match is not None
        major, minor, patch = match.groups()
        assert major == "1"
        assert minor == "2"
        assert patch == "3"


class TestVersionComparison:
    """测试版本号比较"""

    @pytest.mark.parametrize("v1,v2,expected", [
        ("1.0.0", "1.0.1", -1),  # PATCH 更大
        ("1.0.0", "1.1.0", -1),  # MINOR 更大
        ("1.0.0", "2.0.0", -1),  # MAJOR 更大
        ("1.2.3", "1.2.3", 0),   # 相同版本
        ("2.0.0", "1.9.9", 1),   # MAJOR 更大
        ("1.5.0", "1.4.9", 1),   # MINOR 更大
        ("1.0.5", "1.0.4", 1),   # PATCH 更大
        ("10.0.0", "9.99.99", 1),  # MAJOR 比较按数字值
    ])
    def test_version_comparison(self, v1, v2, expected):
        """测试版本号大小比较

        Args:
            v1: 第一个版本号
            v2: 第二个版本号
            expected: -1 表示 v1 < v2，0 表示相等，1 表示 v1 > v2
        """
        def parse_version(v: str) -> Tuple[int, int, int]:
            parts = v.lstrip("v").split(".")
            return int(parts[0]), int(parts[1]), int(parts[2])

        v1_parsed = parse_version(v1)
        v2_parsed = parse_version(v2)

        if v1_parsed < v2_parsed:
            result = -1
        elif v1_parsed == v2_parsed:
            result = 0
        else:
            result = 1

        assert result == expected

    def test_version_ordering(self):
        """测试多个版本号的排序"""
        versions = ["1.0.0", "2.0.0", "1.1.0", "1.0.1", "v1.0.0"]

        def parse_version(v: str) -> Tuple[int, int, int]:
            parts = v.lstrip("v").split(".")
            return int(parts[0]), int(parts[1]), int(parts[2])

        # 排序
        sorted_versions = sorted(versions, key=parse_version)

        # 验证排序结果
        assert sorted_versions[0] == "1.0.0" or sorted_versions[0] == "v1.0.0"
        assert sorted_versions[-1] == "2.0.0"


class TestVersionIncrementRules:
    """测试版本号递增规则"""

    @pytest.mark.parametrize("current_version,increment_type,expected_next", [
        ("1.0.0", "patch", "1.0.1"),    # 修复 bug
        ("1.0.0", "minor", "1.1.0"),    # 新功能
        ("1.0.0", "major", "2.0.0"),    # 不兼容变更
        ("1.5.3", "patch", "1.5.4"),
        ("1.5.3", "minor", "1.6.0"),
        ("1.5.3", "major", "2.0.0"),
        ("2.9.9", "patch", "2.9.10"),
        ("2.9.9", "minor", "2.10.0"),
        ("2.9.9", "major", "3.0.0"),
    ])
    def test_version_increment(self, current_version, increment_type, expected_next):
        """测试根据变更类型递增版本号

        Args:
            current_version: 当前版本号
            increment_type: 变更类型（patch/minor/major）
            expected_next: 期望的下一个版本号
        """
        def increment_version(version: str, increment_type: str) -> str:
            parts = version.lstrip("v").split(".")
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

            if increment_type == "patch":
                patch += 1
            elif increment_type == "minor":
                minor += 1
                patch = 0
            elif increment_type == "major":
                major += 1
                minor = 0
                patch = 0
            else:
                raise ValueError(f"Invalid increment type: {increment_type}")

            return f"{major}.{minor}.{patch}"

        result = increment_version(current_version, increment_type)
        assert result == expected_next

    @pytest.mark.parametrize("scenario,increment_type", [
        ("添加了导出为 PDF 的功能", "minor"),
        ("优化了性能，提升 20%", "minor"),
        ("新增了数据分析功能", "minor"),
        ("数据格式变更，旧版本无法读取", "major"),
        ("移除了旧版 API", "major"),
        ("不兼容的数据库迁移", "major"),
        ("修复了搜索功能的崩溃问题", "patch"),
        ("修复了中文显示乱码问题", "patch"),
        ("修复了拼写错误", "patch"),
    ])
    def test_determine_increment_type(self, scenario, increment_type):
        """测试根据变更描述确定递增类型"""
        # 这些是基于语义化版本规范的规则
        # 按优先级检查：先 major（不兼容/移除），再 patch（修复），最后 minor（新增/优化）
        # 注意：patch 要在 minor 之前检查，因为"修复了XX功能"可能包含"功能"关键词
        major_keywords = ["不兼容", "移除", "breaking", "remove"]
        patch_keywords = ["修复", "fix", "bug", "问题"]
        minor_keywords = ["添加", "新增", "优化", "提升", "add", "feature"]

        scenario_lower = scenario.lower()

        # 按优先级检查
        if any(keyword in scenario_lower for keyword in major_keywords):
            assert increment_type == "major"
        elif any(keyword in scenario_lower for keyword in patch_keywords):
            assert increment_type == "patch"
        elif any(keyword in scenario_lower for keyword in minor_keywords):
            assert increment_type == "minor"


class TestGitTagCommands:
    """测试 Git tag 命令理解"""

    def test_create_annotated_tag_command(self):
        """测试创建带注释的 tag 命令"""
        command = "git tag -a v1.0.0 -m 'PyHelper v1.0.0 发布'"

        # 应该包含 tag 命令
        assert "git tag" in command
        # 应该有 -a 参数（带注释）
        assert "-a" in command
        # 应该指定版本号
        assert "v1.0.0" in command
        # 应该有 -m 参数（消息）
        assert "-m" in command

    def test_list_tags_command(self):
        """测试列出所有 tag 命令"""
        command = "git tag"

        assert "git tag" in command

    def test_show_tag_details_command(self):
        """测试查看 tag 详情命令"""
        command = "git show v1.0.0"

        assert "git show" in command
        assert "v1.0.0" in command

    def test_push_specific_tag_command(self):
        """测试推送指定 tag 命令"""
        command = "git push origin v1.0.0"

        assert "git push" in command
        assert "origin" in command
        assert "v1.0.0" in command

    def test_push_all_tags_command(self):
        """测试推送所有 tag 命令"""
        command = "git push origin --tags"

        assert "git push" in command
        assert "--tags" in command

    def test_checkout_tag_command(self):
        """测试切换到指定 tag 命令"""
        command = "git checkout v1.0.0"

        assert "git checkout" in command
        assert "v1.0.0" in command


class TestTagNamingConventions:
    """测试 tag 命名规范"""

    @pytest.mark.parametrize("tag_name,is_valid", [
        ("v1.0.0", True),
        ("1.0.0", True),
        ("v2.1.3", True),
        ("final", False),  # 不规范
        ("release", False),  # 不规范
        ("v1.0", False),  # 缺少 PATCH
        ("version1.0.0", False),  # 前缀不规范
    ])
    def test_tag_naming_convention(self, tag_name, is_valid):
        """测试 tag 命名是否符合规范"""
        # 应该使用语义化版本
        pattern = r"^v?\d+\.\d+\.\d+$"
        matches = bool(re.match(pattern, tag_name))

        assert matches == is_valid


class TestVersionInDifferentContexts:
    """测试版本号在不同上下文中的使用"""

    def test_version_in_pyproject_toml(self):
        """测试 pyproject.toml 中的版本号格式"""
        content = """
[project]
name = "pyhelper"
version = "1.0.0"
"""
        # 应该包含版本号
        assert 'version = "1.0.0"' in content or "version = '1.0.0'" in content

    def test_version_in_init_py(self):
        """测试 __init__.py 中的版本号定义"""
        content = '''
__version__ = "1.0.0"
'''
        assert "__version__" in content
        assert "1.0.0" in content

    def test_version_in_changelog(self):
        """测试 CHANGELOG.md 中的版本号"""
        content = """
# Changelog

## [1.0.0] - 2026-02-15

### Added
- Initial release
"""
        # 应该有版本号
        assert "1.0.0" in content
        # 应该有日期
        assert "2026-02-15" in content


class TestEdgeCases:
    """测试边界情况"""

    def test_version_zero_zero_zero(self):
        """测试 0.0.0 版本（初始开发阶段）"""
        version = "0.0.0"
        pattern = r"^v?\d+\.\d+\.\d+$"
        assert re.match(pattern, version) is not None

    def test_version_with_leading_zeros(self):
        """测试前导零的版本号（不推荐但合法）"""
        version = "1.01.003"
        pattern = r"^v?\d+\.\d+\.\d+$"
        # 格式合法，但语义化版本规范不建议使用前导零
        assert re.match(pattern, version) is not None

    def test_very_large_version_numbers(self):
        """测试非常大的版本号"""
        version = "999.999.999"
        pattern = r"^v?\d+\.\d+\.\d+$"
        assert re.match(pattern, version) is not None

        # 解析测试
        parts = version.split(".")
        assert int(parts[0]) == 999
        assert int(parts[1]) == 999
        assert int(parts[2]) == 999

    def test_case_sensitivity(self):
        """测试版本号大小写敏感性"""
        # 版本号是大小写敏感的
        version1 = "v1.0.0"
        version2 = "V1.0.0"

        # 'v' 前缀应该是小写
        assert version1.lower() == "v1.0.0"
        # 大写 V 不符合常见规范（虽然技术上可行）


@pytest.mark.parametrize("changes,expected_bump", [
    (["修复了 bug A"], "patch"),
    (["修复了 bug A", "修复了 bug B"], "patch"),
    (["添加了新功能 X"], "minor"),
    (["优化了性能"], "minor"),
    (["修复了 bug", "添加了新功能"], "minor"),  # 有新功能就是 minor
    (["不兼容的 API 变更"], "major"),
    (["移除了旧功能"], "major"),
    (["修复了 bug", "不兼容的变更"], "major"),  # 有不兼容变更就是 major
])
def test_determine_version_bump_from_changes(changes, expected_bump):
    """测试根据变更列表确定版本号递增类型"""
    major_keywords = ["不兼容", "移除", "breaking"]
    minor_keywords = ["添加", "新增", "优化", "功能"]
    patch_keywords = ["修复", "fix"]

    changes_text = " ".join(changes).lower()

    # 检查是否包含 major 关键词
    if any(keyword in changes_text for keyword in major_keywords):
        assert expected_bump == "major"
    # 检查是否包含 minor 关键词
    elif any(keyword in changes_text for keyword in minor_keywords):
        assert expected_bump == "minor"
    # 检查是否只包含 patch 关键词
    elif any(keyword in changes_text for keyword in patch_keywords):
        assert expected_bump == "patch"
