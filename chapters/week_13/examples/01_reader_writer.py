#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：最简单的 reader + writer agent 流程

本示例演示：
1. 使用 dataclass 定义 agent 消息格式
2. reader agent：读取并分析笔记文件
3. writer agent：根据笔记信息生成学习计划
4. agent 之间的消息传递（reader 的输出 → writer 的输入）

运行方式：
    python3 chapters/week_13/examples/01_reader_writer.py

预期输出：
    [reader] 读取笔记:函数基础
    [writer] 生成计划:Week 3 - 函数基础
"""

from dataclasses import dataclass
from typing import List
from pathlib import Path


# =====================
# Agent 消息格式（dataclass）
# =====================

@dataclass
class NoteInfo:
    """笔记信息（reader agent 的输出）"""
    title: str
    topics: List[str]
    difficulty: str  # easy/medium/hard


@dataclass
class StudyPlan:
    """学习计划（writer agent 的输出）"""
    week: int
    title: str
    prerequisites: List[str]  # 前置知识
    priority: str  # high/medium/low


# =====================
# Agent 定义
# =====================

class ReaderAgent:
    """reader agent：读取并分析笔记文件"""

    def read_note(self, file_path: Path) -> NoteInfo:
        """读取笔记文件并提取关键信息"""
        content = file_path.read_text()

        # 简化版：模拟提取信息（实际可能用 AI/NLP）
        lines = content.split("\n")
        title = lines[0].strip("# ").strip()

        # 模拟：从内容中提取主题
        topics = []
        if "变量" in content:
            topics.append("变量")
        if "函数" in content:
            topics.append("函数")

        # 如果没找到主题，给一个默认值
        if not topics:
            topics = ["循环"]

        return NoteInfo(
            title=title,
            topics=topics,
            difficulty="medium"
        )


class WriterAgent:
    """writer agent：根据笔记信息生成学习计划"""

    def create_plan(self, note_info: NoteInfo, week: int) -> StudyPlan:
        """根据笔记分析结果生成学习计划"""
        return StudyPlan(
            week=week,
            title=note_info.title,
            prerequisites=[],  # 简化版：暂不分析前置
            priority="high" if note_info.difficulty == "hard" else "medium"
        )


# =====================
# 使用 agent team
# =====================

if __name__ == "__main__":
    # 创建测试笔记文件
    test_note = Path("/tmp/week03_functions.md")
    test_note.write_text(
        "# 函数基础\n\n"
        "函数是 Python 的重要组成部分。\n"
        "本节讲解：变量、函数定义、参数传递。",
        encoding="utf-8"
    )

    # 创建 agent
    reader = ReaderAgent()
    writer = WriterAgent()

    # reader agent 读取笔记
    note_info = reader.read_note(test_note)
    print(f"[reader] 读取笔记:{note_info.title}")
    print(f"  主题:{note_info.topics}")
    print(f"  难度:{note_info.difficulty}")

    # writer agent 生成计划
    plan = writer.create_plan(note_info, week=3)
    print(f"\n[writer] 生成计划:Week {plan.week} - {plan.title}")
    print(f"  前置知识:{plan.prerequisites}")
    print(f"  优先级:{plan.priority}")

    # 清理测试文件
    test_note.unlink()


# =====================
# 总结
# =====================

"""
本示例演示了 agent team 的最基础形式：

核心概念：
  1. dataclass 作为 agent 之间的"消息协议"
     - NoteInfo：reader 的输出，writer 的输入
     - StudyPlan：writer 的输出

  2. 消息传递：reader 的输出 → writer 的输入
     - 类似函数组合：g(f(x))

  3. 职责单一：
     - reader 只负责读取和提取信息
     - writer 只负责生成计划

与之前知识的联系：
  - Week 11 的 dataclass：定义数据结构
  - Week 03 的函数：每个 agent 是一个函数，输入→处理→输出

下一步：
  - 加上 tester agent：测试生成的计划是否合理
  - 加上 reviewer agent：检查代码质量
"""
