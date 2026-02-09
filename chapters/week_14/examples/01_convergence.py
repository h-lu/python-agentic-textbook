#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：代码收敛 - 整理项目结构

本示例演示如何将"能跑"的代码收敛成"专业"的项目：
1. 删除冗余代码（提取公共函数）
2. 统一代码风格（snake_case 命名、类型提示、docstring）
3. 优化导入结构（标准库 → 第三方 → 本地）

运行方式：
    python3 chapters/week_14/examples/01_convergence.py

预期输出：
    展示收敛前后的代码对比，说明改进点

本示例是代码质量对比展示，不产生实际功能输出
"""

# =====================
# ❌ 收敛前：冗余代码、风格不统一
# =====================

def before_add_note(data, content):
    """添加笔记（收敛前）"""
    # 冗余：重复的校验逻辑
    if not content or not content.strip():
        raise ValueError("笔记内容不能为空")

    note_id = "20250209-001"
    data[note_id] = {
        "content": content,
        "created_at": "2025-02-09"
    }
    return note_id


def before_update_note(data, note_id, new_content):
    """更新笔记（收敛前）"""
    # 冗余：同样的校验逻辑
    if not new_content or not new_content.strip():
        raise ValueError("笔记内容不能为空")

    if note_id in data:
        data[note_id]["content"] = new_content
        return True
    return False


def before_getUserNotes(userId):  # ❌ camelCase 命名
    """获取用户笔记（收敛前）"""
    # ❌ 没有 docstring，没有类型提示
    return data.get(userId, [])


# 导入顺序混乱（示例代码，注释掉避免报错）
# import sys
# from .storage import save_data
# from pathlib import Path
# import json
# from .models import Note


# =====================
# ✅ 收敛后：公共函数提取、风格统一
# =====================

def validate_content(content: str) -> None:
    """校验笔记内容（提取的公共函数）

    Args:
        content: 笔记内容

    Raises:
        ValueError: 内容为空或只有空白字符
    """
    if not content or not content.strip():
        raise ValueError("笔记内容不能为空")


def add_note(data: dict, content: str) -> str:
    """添加学习笔记

    Args:
        data: 数据字典
        content: 笔记内容

    Returns:
        笔记 ID

    Raises:
        ValueError: 内容为空
    """
    validate_content(content)  # 复用公共校验

    from datetime import datetime
    note_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    data[note_id] = {
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    return note_id


def update_note(data: dict, note_id: str, new_content: str) -> bool:
    """更新学习笔记

    Args:
        data: 数据字典
        note_id: 笔记 ID
        new_content: 新内容

    Returns:
        是否更新成功

    Raises:
        ValueError: 内容为空
    """
    validate_content(new_content)  # 复用公共校验

    if note_id in data:
        data[note_id]["content"] = new_content
        return True
    return False


def get_user_notes(user_id: str) -> list:  # ✅ snake_case 命名
    """获取用户的所有笔记

    Args:
        user_id: 用户 ID

    Returns:
        笔记列表
    """
    return data.get(user_id, [])


# ✅ 优化导入顺序（PEP 8 推荐：标准库 → 第三方 → 本地）
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 第三方库（如果有的话）
# import requests
# import click

# 本地模块
# from .models import Note
# from .storage import save_data


# =====================
# 对比演示
# =====================

if __name__ == "__main__":
    print("=" * 70)
    print("代码收敛示例")
    print("=" * 70)

    print("\n【收敛前的问题】")
    print("1. ❌ 冗余代码：validate_content 逻辑在两个函数中重复")
    print("2. ❌ 风格不统一：camelCase vs snake_case")
    print("3. ❌ 缺少类型提示：无法静态检查")
    print("4. ❌ 缺少 docstring：不知道函数做什么")
    print("5. ❌ 导入顺序混乱：难定位模块来源")

    print("\n【收敛后的改进】")
    print("1. ✅ 提取公共函数：validate_content()")
    print("2. ✅ 统一命名规范：全部使用 snake_case")
    print("3. ✅ 添加类型提示：content: str -> str")
    print("4. ✅ 补充 docstring：Args/Returns/Raises")
    print("5. ✅ 优化导入顺序：标准库 → 第三方 → 本地")

    # 测试收敛后的代码
    print("\n【测试收敛后的代码】")
    print("-" * 70)

    data = {}

    # 测试添加笔记
    note_id = add_note(data, "今天学了代码收敛")
    print(f"✓ 添加笔记：{note_id}")

    # 测试更新笔记
    success = update_note(data, note_id, "今天学了代码收敛和代码风格")
    print(f"✓ 更新笔记：{'成功' if success else '失败'}")

    # 测试校验功能
    print("\n测试校验功能：")
    try:
        add_note(data, "")  # 空内容
    except ValueError as e:
        print(f"✓ 正确捕获错误：{e}")

    print("\n" + "=" * 70)
    print("收敛的价值：")
    print("- 代码更易读（统一的风格和清晰的文档）")
    print("- 更易维护（公共函数只需改一处）")
    print("- 更易测试（每个函数职责单一）")
    print("=" * 70)
