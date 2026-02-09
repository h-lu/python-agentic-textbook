# Week 11 测试覆盖说明

## 测试文件概览

| 文件 | 测试数量 | 覆盖范围 |
|------|---------|---------|
| `test_smoke.py` | 6 | 基础功能验证 |
| `test_dataclass.py` | 21 | dataclass 创建、比较、字段默认值、边界情况 |
| `test_state.py` | 23 | 状态转换、状态验证、枚举 |
| `test_json_conversion.py` | 24 | JSON 序列化、字典转换、文件操作 |
| `test_type_hints.py` | 20 | 类型提示函数、复杂类型场景 |
| **总计** | **88** | **全部通过** |

---

## 测试矩阵

### 1. dataclass 基础 (test_dataclass.py)

| 测试类别 | 测试场景 | 测试方法 | 预期结果 |
|---------|---------|---------|---------|
| **创建** | 提供所有必需字段 | `test_create_with_all_required_fields` | 成功创建 |
| **创建** | 使用默认值 | `test_create_with_default_value` | completed=False |
| **创建** | 显式覆盖默认值 | `test_create_explicitly_override_default` | completed=True |
| **创建** | 缺少必需字段 | `test_create_missing_required_field` | TypeError |
| **比较** | 相同字段值的实例 | `test_equal_objects` | 相等 |
| **比较** | 不同字段值的实例 | `test_unequal_objects` | 不相等 |
| **字段可变性** | 修改字段值 | `test_fields_are_mutable` | 可以修改 |
| **字符串表示** | __repr__ 方法 | `test_repr_contains_field_info` | 包含字段信息 |
| **默认值** | 不可变类型默认值 | `test_immutability_default` | 正常工作 |
| **默认值** | 可变类型默认值 | `test_mutable_default_with_factory` | 每个实例独立 |
| **默认值** | 创建时指定可变字段 | `test_custom_tags_on_creation` | 正确设置 |
| **方法** | dataclass 可以有方法 | `test_dataclass_can_have_methods` | 方法正常工作 |
| **边界** | 空字符串字段 | `test_empty_string_fields` | 正常处理 |
| **边界** | Unicode 字段 | `test_unicode_fields` | 正确存储 |
| **边界** | 超长字符串 | `test_long_string_fields` | 正确处理 |
| **边界** | 特殊字符 | `test_special_characters_in_fields` | 正确存储 |

### 2. 状态管理 (test_state.py)

| 测试类别 | 测试场景 | 测试方法 | 预期结果 |
|---------|---------|---------|---------|
| **初始状态** | 默认状态 | `test_initial_state_is_todo` | TODO |
| **状态转换** | TODO → IN_PROGRESS | `test_todo_to_in_progress` | 成功 |
| **状态转换** | IN_PROGRESS → DONE | `test_in_progress_to_done` | 成功 |
| **状态转换** | TODO → DONE 直接 | `test_todo_to_done_directly` | 成功 |
| **状态转换** | DONE → TODO | `test_cannot_restart_done_task` | ValueError |
| **状态验证** | TODO → IN_PROGRESS | `test_validate_todo_to_in_progress` | True |
| **状态验证** | IN_PROGRESS → DONE | `test_validate_in_progress_to_done` | True |
| **状态验证** | TODO → DONE | `test_validate_todo_to_done` | True |
| **状态验证** | DONE → TODO | `test_validate_done_to_todo_is_invalid` | False |
| **状态验证** | DONE → IN_PROGRESS | `test_validate_done_to_in_progress_is_invalid` | False |
| **状态查询** | TODO 状态可重启 | `test_can_restart_when_todo` | True |
| **状态查询** | IN_PROGRESS 可重启 | `test_can_restart_when_in_progress` | True |
| **状态查询** | DONE 不可重启 | `test_cannot_restart_when_done` | False |
| **枚举** | 枚举值 | `test_enum_values` | 正确的中文值 |
| **枚举** | 枚举比较 | `test_enum_comparison` | 同值相等 |
| **枚举** | 枚举同一性 | `test_enum_identity` | 同一对象 |
| **边界** | 多次前向转换 | `test_multiple_transitions_forward` | 正常 |
| **边界** | 快速状态变化 | `test_rapid_state_changes` | 保持最终状态 |
| **边界** | 创建时覆盖状态 | `test_state_with_default_overridden` | 使用指定状态 |
| **边界** | 所有状态 | `test_all_possible_states` | 全部可用 |

### 3. JSON 转换 (test_json_conversion.py)

| 测试类别 | 测试场景 | 测试方法 | 预期结果 |
|---------|---------|---------|---------|
| **字典转换** | to_dict | `test_to_dict` | 正确转换 |
| **字典转换** | from_dict | `test_from_dict` | 正确恢复 |
| **字典转换** | 缺少字段 | `test_from_dict_with_missing_fields` | 使用默认值 |
| **字典转换** | 往返转换 | `test_round_trip_conversion` | 数据一致 |
| **文件操作** | to_json | `test_to_json` | 正确保存 |
| **文件操作** | from_json | `test_from_json` | 正确加载 |
| **文件操作** | 文件往返 | `test_json_file_round_trip` | 数据一致 |
| **Enum 处理** | to_dict 带 Enum | `test_note_to_dict_with_enum` | 转为字符串 |
| **Enum 处理** | from_dict 带 Enum | `test_note_from_dict_with_enum` | 恢复为 Enum |
| **Enum 处理** | Enum 往返 | `test_note_enum_round_trip` | 状态一致 |
| **笔记状态** | 发布草稿 | `test_publish_draft_note` | PUBLISHED |
| **笔记状态** | 归档笔记 | `test_archive_note` | ARCHIVED |
| **笔记状态** | 发布已归档 | `test_cannot_publish_archived_note` | ValueError |
| **asdict** | 基本功能 | `test_asdict_basic` | 正确转换 |
| **asdict** | 嵌套结构 | `test_asdict_with_nested_structures` | 递归转换 |
| **边界** | 空字符串 | `test_empty_strings` | 正确处理 |
| **边界** | Unicode | `test_unicode_characters` | 正确存储 |
| **边界** | 特殊字符 | `test_special_characters` | 正确处理 |
| **边界** | 超长字符串 | `test_very_long_strings` | 正确处理 |
| **边界** | 多标签 | `test_tags_with_multiple_items` | 全部保留 |
| **边界** | 所有状态序列化 | `test_all_note_statuses_serialize` | 全部支持 |

### 4. 类型提示 (test_type_hints.py)

| 测试类别 | 测试场景 | 测试方法 | 预期结果 |
|---------|---------|---------|---------|
| **函数** | 筛选高优先级 | `test_get_high_priority_tasks_returns_list` | 返回列表 |
| **函数** | 空输入 | `test_get_high_priority_tasks_empty_input` | 空列表 |
| **函数** | 无匹配 | `test_get_high_priority_tasks_no_matches` | 空列表 |
| **函数** | 按状态筛选 | `test_get_tasks_by_status` | 正确筛选 |
| **函数** | 按标题查找（找到） | `test_find_task_by_title_found` | 返回任务 |
| **函数** | 按标题查找（未找到） | `test_find_task_by_title_not_found` | 返回 None |
| **类型行为** | Python 不强制检查 | `test_python_does_not_enforce_types` | 运行时不报错 |
| **类型行为** | 类型提示作为文档 | `test_type_hints_are_documentation` | 可通过 __annotations__ 访问 |
| **类型行为** | Optional 类型 | `test_optional_type` | 支持 None |
| **列表类型** | List[Task] | `test_list_of_tasks_type` | 正确类型 |
| **复杂场景** | 多参数函数 | `test_function_with_multiple_parameters` | 正确处理 |
| **复杂场景** | 嵌套调用 | `test_nested_function_calls` | 正确组合 |
| **复杂场景** | 链式操作 | `test_chained_operations` | 正确工作 |
| **边界** | None for Optional | `test_none_for_optional_types` | 正确处理 |
| **边界** | 空集合 | `test_empty_collections` | 正确处理 |
| **边界** | 默认参数 | `test_function_with_default_parameters` | 使用默认值 |
| **边界** | Union 类型 | `test_union_types` | 支持多种类型 |

---

## 运行测试

```bash
# 运行所有测试
python3 -m pytest chapters/week_11/tests -v

# 运行特定文件
python3 -m pytest chapters/week_11/tests/test_dataclass.py -v
python3 -m pytest chapters/week_11/tests/test_state.py -v
python3 -m pytest chapters/week_11/tests/test_json_conversion.py -v
python3 -m pytest chapters/week_11/tests/test_type_hints.py -v

# 运行单个测试
python3 -m pytest chapters/week_11/tests/test_state.py::TestStateTransitions::test_cannot_restart_done_task -v

# 查看测试覆盖率（需要安装 pytest-cov）
python3 -m pytest chapters/week_11/tests --cov=starter_code/solution --cov-report=term-missing
```

---

## 测试覆盖的核心概念

1. **dataclass** (21 tests)
   - @dataclass 装饰器的使用
   - 字段定义和类型提示
   - 默认值（不可变和可变）
   - 自动生成的方法（__init__, __repr__, __eq__）

2. **字段默认值** (3 tests)
   - 简单类型默认值（int, str, bool）
   - 可变类型默认值（field(default_factory=...)）
   - 避免可变默认值陷阱

3. **类型提示** (20 tests)
   - 函数参数和返回值类型标注
   - Optional, List, Union 等类型
   - Python 不强制检查类型

4. **状态管理** (23 tests)
   - Enum 定义状态
   - 状态转换规则
   - 非法状态转换的拒绝
   - 状态查询方法

5. **JSON 序列化** (24 tests)
   - dataclass 与 dict 转换
   - JSON 文件读写
   - Enum 的序列化处理
   - 往返转换的一致性

---

## 设计原则

1. **正例优先**：先测试正常使用场景
2. **边界覆盖**：空值、超长、特殊字符
3. **错误处理**：非法输入应有明确错误
4. **测试独立性**：每个测试不依赖其他测试
5. **清晰的命名**：`test_<功能>_<场景>_<预期结果>`
