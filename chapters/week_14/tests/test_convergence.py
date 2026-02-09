"""测试代码收敛相关功能

这些测试验证学生是否理解：
- 项目结构验证
- 模块导入检查
- 冗余代码识别
- 代码风格验证
"""

import pytest
import ast
import sys
from pathlib import Path


class TestProjectStructureValidation:
    """测试项目结构验证"""

    def test_has_source_package_directory(self, valid_project_structure):
        """测试项目是否有源代码包目录"""
        pyhelper_dir = valid_project_structure / "pyhelper"
        assert pyhelper_dir.exists()
        assert pyhelper_dir.is_dir()

    def test_has_init_py(self, valid_project_structure):
        """测试包目录是否有 __init__.py"""
        init_file = valid_project_structure / "pyhelper" / "__init__.py"
        assert init_file.exists()
        assert init_file.is_file()

    def test_has_tests_directory(self, valid_project_structure):
        """测试项目是否有独立的 tests 目录"""
        tests_dir = valid_project_structure / "tests"
        assert tests_dir.exists()
        assert tests_dir.is_dir()

    def test_has_readme(self, valid_project_structure):
        """测试项目是否有 README.md"""
        readme = valid_project_structure / "README.md"
        assert readme.exists()
        assert readme.is_file()

    def test_has_changelog(self, valid_project_structure):
        """测试项目是否有 CHANGELOG.md"""
        changelog = valid_project_structure / "CHANGELOG.md"
        assert changelog.exists()
        assert changelog.is_file()

    def test_has_pyproject_toml(self, valid_project_structure):
        """测试项目是否有 pyproject.toml 配置文件"""
        pyproject = valid_project_structure / "pyproject.toml"
        assert pyproject.exists()
        assert pyproject.is_file()


class TestModuleImportValidation:
    """测试模块导入检查"""

    def test_import_main_module(self, valid_project_structure, monkeypatch):
        """测试能否导入主模块"""
        # 将临时目录添加到 Python 路径
        monkeypatch.syspath_prepend(str(valid_project_structure))

        # 尝试导入包
        import pyhelper
        assert pyhelper is not None

    def test_import_submodules(self, valid_project_structure, monkeypatch):
        """测试能否导入子模块"""
        monkeypatch.syspath_prepend(str(valid_project_structure))

        # 导入包应该成功
        import pyhelper
        assert pyhelper is not None

        # 检查子模块文件是否存在
        assert (valid_project_structure / "pyhelper" / "cli.py").exists()
        assert (valid_project_structure / "pyhelper" / "models.py").exists()
        assert (valid_project_structure / "pyhelper" / "storage.py").exists()

    def test_import_nonexistent_module_fails(self, valid_project_structure, monkeypatch):
        """测试导入不存在的模块应该失败"""
        monkeypatch.syspath_prepend(str(valid_project_structure))

        with pytest.raises(ImportError):
            from pyhelper import nonexistent_module


class TestCodeConvergence:
    """测试代码收敛识别"""

    def test_detect_duplicate_functions(self, temp_project_dir):
        """测试检测重复的函数定义"""
        # 创建包含重复代码的文件
        code_file = temp_project_dir / "duplicate.py"
        code_file.write_text("""
def validate_content(content):
    if not content or not content.strip():
        raise ValueError("内容不能为空")

def add_note(data, content):
    if not content or not content.strip():
        raise ValueError("内容不能为空")
    # 添加逻辑

def update_note(data, note_id, new_content):
    if not new_content or not new_content.strip():
        raise ValueError("内容不能为空")
    # 更新逻辑
""")

        # 解析代码
        tree = ast.parse(code_file.read_text())

        # 查找所有的函数定义
        function_defs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_defs.append(node.name)

        # 应该有多个函数
        assert len(function_defs) >= 3
        assert "validate_content" in function_defs
        assert "add_note" in function_defs
        assert "update_note" in function_defs

    def test_snake_case_naming(self, temp_project_dir):
        """测试检测 snake_case 命名规范"""
        # 创建符合规范的代码
        good_code = temp_project_dir / "good_style.py"
        good_code.write_text("""
def get_user_notes(user_id: str) -> list:
    return []

def save_notes(note_data: dict) -> None:
    pass
""")

        tree = ast.parse(good_code.read_text())

        # 检查所有函数名都是 snake_case
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                assert node.name.islower() or "_" in node.name

    def test_detect_camel_case_naming(self, temp_project_dir):
        """测试检测 camelCase 命名（不符合 Python 规范）"""
        # 创建不符合规范的代码
        bad_code = temp_project_dir / "bad_style.py"
        bad_code.write_text("""
def getUserNotes(userId):
    return []

def SaveNotes(noteData):
    pass
""")

        tree = ast.parse(bad_code.read_text())

        # 检查是否有 camelCase 命名（首字母小写，包含大写字母）
        camel_case_functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                name = node.name
                if name and name[0].islower() and any(c.isupper() for c in name):
                    camel_case_functions.append(name)

        # 应该找到 camelCase 命名的函数
        assert len(camel_case_functions) > 0


class TestImportOrderValidation:
    """测试导入顺序验证（PEP 8）"""

    def test_import_order_standard_first(self, temp_project_dir):
        """测试标准库导入应该在最前面"""
        code_file = temp_project_dir / "ordered_imports.py"
        code_file.write_text("""
import sys
from pathlib import Path
import json

from .models import Note
from .storage import save_data
""")

        tree = ast.parse(code_file.read_text())
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom):
                    if node.module and not node.module.startswith("."):
                        imports.append(("stdlib", node.module))
                    else:
                        imports.append(("local", node.module))
                else:
                    imports.append(("stdlib", [alias.name for alias in node.names][0]))

        # 标准库导入应该在本地导入之前
        stdlib_indices = [i for i, (t, _) in enumerate(imports) if t == "stdlib"]
        local_indices = [i for i, (t, _) in enumerate(imports) if t == "local"]

        if stdlib_indices and local_indices:
            assert max(stdlib_indices) < min(local_indices)


class TestEdgeCases:
    """测试边界情况"""

    def test_empty_project_directory(self, temp_project_dir):
        """测试空项目目录"""
        # 空目录应该没有关键文件
        assert not (temp_project_dir / "README.md").exists()
        assert not (temp_project_dir / "pyproject.toml").exists()

    def test_missing_init_py(self, temp_project_dir):
        """测试缺少 __init__.py 的包"""
        (temp_project_dir / "mypackage").mkdir()
        # 没有 __init__.py

        # Python 应该能将其视为 namespace package
        # 但传统包需要 __init__.py
        assert not (temp_project_dir / "mypackage" / "__init__.py").exists()

    def test_deeply_nested_structure(self, temp_project_dir):
        """测试深层嵌套的项目结构"""
        nested = temp_project_dir / "deep" / "nested" / "package"
        nested.mkdir(parents=True)
        (nested / "__init__.py").write_text("")

        # 即使嵌套很深，也应该能找到
        assert nested.exists()
        assert (nested / "__init__.py").exists()
