#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：reader → writer → tester agent 流程

本示例演示：
1. 在 reader + writer 基础上添加 tester agent
2. tester agent：测试学习计划是否合理
3. agent 消息链：reader → writer → tester

运行方式：
    python3 chapters/week_13/examples/01_reader_writer_tester.py

预期输出：
    [reader] 读取笔记:函数基础
    [writer] 生成计划:Week 3 - 函数基础
    [tester] 测试通过:函数基础
"""

from dataclasses import dataclass
from typing import List
from pathlib import Path


# =====================
# Agent 消息格式
# =====================

@dataclass
class NoteInfo:
    """笔记信息（reader agent 的输出）"""
    title: str
    topics: List[str]
    difficulty: str


@dataclass
class StudyPlan:
    """学习计划（writer agent 的输出）"""
    week: int
    title: str
    prerequisites: List[str]
    priority: str


@dataclass
class TestResult:
    """测试结果（tester agent 的输出）"""
    passed: bool
    issues: List[str]


# =====================
# Agent 定义
# =====================

class ReaderAgent:
    """reader agent：读取并分析笔记文件"""

    def read_note(self, file_path: Path) -> NoteInfo:
        content = file_path.read_text()
        lines = content.split("\n")
        title = lines[0].strip("# ").strip()

        topics = []
        if "变量" in content:
            topics.append("变量")
        if "函数" in content:
            topics.append("函数")
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
        return StudyPlan(
            week=week,
            title=note_info.title,
            prerequisites=[],
            priority="high" if note_info.difficulty == "hard" else "medium"
        )


class TesterAgent:
    """tester agent：测试学习计划是否合理"""

    def test_plan(self, plan: StudyPlan, all_topics: List[str]) -> TestResult:
        """测试学习计划的质量"""
        issues = []

        # 检查 1：前置知识是否在所有主题中
        for prereq in plan.prerequisites:
            if prereq not in all_topics:
                issues.append(f"前置知识'{prereq}'未在课程中找到")

        # 检查 2：优先级不能为空
        if not plan.priority:
            issues.append("优先级未设置")

        # 检查 3：周次必须大于 0
        if plan.week <= 0:
            issues.append(f"周次无效:{plan.week}")

        return TestResult(
            passed=len(issues) == 0,
            issues=issues
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

    # 定义所有课程主题
    all_topics = ["变量", "函数", "循环", "文件", "异常处理", "测试"]

    # 创建 agent
    reader = ReaderAgent()
    writer = WriterAgent()
    tester = TesterAgent()

    # reader agent 读取笔记
    note_info = reader.read_note(test_note)
    print(f"[reader] 读取笔记:{note_info.title}")

    # writer agent 生成计划
    plan = writer.create_plan(note_info, week=3)
    print(f"[writer] 生成计划:Week {plan.week} - {plan.title}")

    # tester agent 测试计划
    test_result = tester.test_plan(plan, all_topics)

    if test_result.passed:
        print(f"[tester] 测试通过:{plan.title}")
    else:
        print(f"[tester] 测试失败:{test_result.issues}")
        for issue in test_result.issues:
            print(f"  - {issue}")

    # 清理测试文件
    test_note.unlink()


# =====================
# 总结
# =====================

"""
本示例在 reader + writer 基础上添加了 tester agent：

核心概念：
  1. 测试断言：定义"什么算通过"
     - 前置知识必须在课程中
     - 优先级不能为空
     - 周次必须有效

  2. 消息链：reader → writer → tester
     - reader.read() → NoteInfo
     - writer.create(NoteInfo) → StudyPlan
     - tester.test(StudyPlan) → TestResult

  3. 职责分离：
     - reader：读取和提取
     - writer：生成计划
     - tester：验证质量

与之前知识的联系：
  - Week 08 的 pytest：测试驱动开发
  - Week 01-05 的条件判断：if/else 检查

下一步：
  - 加上 reviewer agent：检查代码质量
  - 实现失败驱动迭代：测试失败 → 修复 → 再测试
"""
