# Week 07 测试设计总结

## 概述

为 Week 07（模块化与项目结构）设计了完整的测试套件，共 120 个测试用例，覆盖所有核心知识点。

## 核心知识点覆盖

### 1. import 语句的三种写法
- **import module**: 导入整个模块
- **from module import name**: 导入特定名称
- **import module as alias**: 给模块起别名

### 2. 模块搜索路径
- sys.path 的理解
- 当前目录搜索
- 模块缓存（sys.modules）

### 3. __name__ 守卫
- 直接运行 vs 被导入的区别
- 守卫的作用
- 既能导入也能运行的双用途模块

### 4. 包结构
- __init__.py 的作用
- 包 vs 模块的区别
- 嵌套包

### 5. 导入方式
- 绝对导入
- 相对导入（from . import, from .. import）
- 相对导入的限制（只能在包内使用）

## 测试文件结构

```
chapters/week_07/tests/
├── test_smoke.py                    # 冒烟测试 (35 个)
├── test_assignment_contract.py      # 作业契约 (5 个)
├── test_import_basics.py            # import 基础 (40 个)
├── test_modules_and_name_guard.py   # 模块与 __name__ 守卫 (19 个)
├── test_packages_and_imports.py     # 包与导入 (21 个)
└── README.md                        # 测试文档
```

## 测试用例分布

| 文件 | 测试数 | 主要内容 |
|------|--------|---------|
| test_smoke.py | 35 | Python 基础功能验证 |
| test_import_basics.py | 40 | import 语句、搜索路径、标准库 |
| test_modules_and_name_guard.py | 19 | 模块概念、__name__ 守卫 |
| test_packages_and_imports.py | 21 | 包结构、相对/绝对导入 |
| test_assignment_contract.py | 5 | 作业入口契约 |
| **总计** | **120** | **Week 07 所有核心概念** |

## 测试特点

### 1. 正例（Happy Path）
- 正常导入和使用模块
- 正确使用 `__name__` 守卫
- 正确的包结构
- 绝对导入和相对导入的正确用法

### 2. 边界测试
- 重复导入同一模块
- 模块别名
- 空 `__init__.py`
- 嵌套包结构
- 模块级代码执行时机

### 3. 反例（错误用法）
- 导入不存在的模块
- 命名冲突
- 函数定义在守卫内（错误示例）
- 相对导入在包外使用

## 技术亮点

### 1. subprocess 测试
使用 subprocess 创建临时脚本，验证 `__name__` 的实际值：

```python
def test_main_script_has_main_name(self):
    script_content = """
print(f"__name__ = {__name__}")
"""
    result = subprocess.run([sys.executable, script_path], ...)
    assert "__name__ = __main__" in result.stdout
```

### 2. 临时文件和目录
使用 tempfile 和 tmp_path fixture 创建隔离的测试环境：

```python
def test_directory_with_init_py_is_package(self, tmp_path):
    pkg_dir = tmp_path / "mypackage"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text(...)
```

### 3. monkeypatch
使用 monkeypatch 模拟用户输入（为后续测试做准备）：

```python
def test_get_positive_integer_with_retry(self, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: "10")
    result = get_positive_integer_with_retry(...)
    assert result == 10
```

## 测试命名规范

遵循清晰的命名约定：`test_<功能>_<场景>_<预期结果>`

- `test_import_math_module`: 测试导入 math 模块
- `test_name_guard_executes_when_run_as_script`: 测试直接运行时守卫执行
- `test_relative_import_sibling_module`: 测试相对导入同级模块
- `test_functions_defined_inside_guard_are_not_importable`: 测试守卫内定义的函数不可导入

## 测试覆盖矩阵

| 知识点 | 正例 | 边界 | 反例 | 总计 |
|--------|-----|------|-----|------|
| import module | 6 | 3 | 1 | 10 |
| from import | 6 | 3 | 2 | 11 |
| import as | 4 | 2 | 0 | 6 |
| 搜索路径 | 3 | 3 | 1 | 7 |
| 标准库 | 4 | 0 | 0 | 4 |
| 模块概念 | 4 | 2 | 0 | 6 |
| __name__ 变量 | 2 | 2 | 0 | 4 |
| __name__ 守卫 | 6 | 3 | 1 | 10 |
| 包结构 | 3 | 3 | 0 | 6 |
| 绝对导入 | 2 | 1 | 0 | 3 |
| 相对导入 | 4 | 2 | 1 | 7 |
| 项目结构 | 2 | 2 | 0 | 4 |
| **总计** | **46** | **26** | **6** | **78** |

注：该矩阵按概念归类，不是 pytest 采集数量的完整拆分；`test_smoke.py` 和 `test_assignment_contract.py` 主要做基础/契约验证，未计入此矩阵。

## 运行结果

```bash
$ python3 -m pytest chapters/week_07/tests -q
............................................................................
...........................................
120 passed
```

所有 120 个测试全部通过，验证了测试用例的正确性和完整性。

## 教育价值

这些测试不仅验证功能正确性，还具有教育价值：

1. **测试即文档**：测试代码展示了正确的用法
2. **错误示例**：反例测试说明错误用法的后果
3. **最佳实践**：测试中体现了 Python 社区的最佳实践
4. **渐进式学习**：从简单到复杂，从基础到进阶

## 后续工作建议

1. 当 starter_code/solution.py 创建后，可以添加更多针对作业的测试
2. 可以添加性能测试（如大型项目的导入时间）
3. 可以添加代码覆盖率测试，确保测试覆盖所有代码路径
4. 可以添加集成测试，测试完整的模块化项目流程
