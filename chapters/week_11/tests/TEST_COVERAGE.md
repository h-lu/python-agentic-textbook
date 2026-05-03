# Week 11 测试覆盖说明

## 测试文件概览

| 文件 | 测试数量 | 覆盖范围 |
|------|---------|---------|
| `test_week11.py` | 7 | dataclass 默认值、类型提示函数、Enum 状态转换、JSON 转换、图书重构、图书馆修复版 |

## 测试矩阵

| 测试函数 | 覆盖内容 |
|---------|---------|
| `test_student_dataclass_defaults_and_repr` | `Student` dataclass 默认字段和 `__repr__` |
| `test_type_hint_practice_functions` | `calculate_average`、`find_student`、`filter_by_major`、`count_by_major`、`get_top_student` |
| `test_enrollment_status_transitions` | `EnrollmentStatus` 以及审核、完成、非法重复审核 |
| `test_enrollment_reject_path` | 拒绝路径、拒绝原因、拒绝后不能完成 |
| `test_task_json_conversion` | `Task.to_dict()`、`from_dict()`、`to_json()`、`from_json()` |
| `test_book_refactor_contract` | `Book` dataclass、库存更新、总价值、JSON 保存加载 |
| `test_library_system_fixed_contract` | `LibraryBook` 借还状态、借阅人、到期日、缺失 ISBN |

## 运行测试

```bash
# 运行所有 Week 11 测试
python3 -m pytest chapters/week_11/tests -q

# 运行单个契约测试
python3 -m pytest chapters/week_11/tests/test_week11.py::test_task_json_conversion -q
```

当前期望结果：

```text
7 passed
```

## 测试覆盖的核心概念

1. **dataclass**
   - 字段定义和类型提示
   - 默认值和 `field(default_factory=...)`
   - 自动生成的 `__repr__`

2. **类型提示**
   - `List`、`Dict`、`Optional`
   - 空列表、未找到学生、最高 GPA 等边界返回

3. **状态管理**
   - `Enum` 定义有限状态
   - 合法转换和非法转换的 `ValueError`

4. **JSON 序列化**
   - dataclass 与 dict 的双向转换
   - JSON 文件读写往返

5. **重构与修复**
   - 图书字典模型重构为 dataclass
   - 图书馆借还逻辑的状态一致性
