#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：完整的 agent team 流程 - reader → writer → reviewer

本示例演示：
1. reader agent：读取并分析笔记文件
2. writer agent：生成学习计划（支持迭代）
3. reviewer agent：检查计划质量
4. 完整的 agent team 流水线

运行方式：
    python3 chapters/week_13/examples/03_full_agent_team.py

预期输出：
    [reader] 读取笔记:Week 06 - 异常处理

    === 迭代 1 ===
    [reviewer] 审查失败:['缺少前置知识']

    === 迭代 2 ===
    [reviewer] 审查通过!

    最终计划:Week 6 - 异常处理
      前置知识:['函数', '文件']
      优先级:medium
"""

from pathlib import Path
from typing import List, Optional


# =====================
# 数据模型（复用之前的定义）
# =====================

class StudyPlan:
    """学习计划（简化版，不用 dataclass）"""

    def __init__(self, week: int, title: str,
                 prerequisites: List[str], priority: str):
        self.week = week
        self.title = title
        self.prerequisites = prerequisites
        self.priority = priority

    def __repr__(self):
        return f"StudyPlan(week={self.week}, title='{self.title}')"


# =====================
# Agent 定义
# =====================

class ReaderAgent:
    """reader agent：读取并分析笔记文件"""

    def read_note(self, file_path: Path) -> dict:
        """读取笔记文件并提取关键信息"""
        content = file_path.read_text(encoding="utf-8")

        # 提取标题（第一个 # 标题）
        lines = content.split("\n")
        title = lines[0].strip("# ").strip()

        # 简化版：提取主题（实际可用 NLP/AI）
        topics = []
        if "异常" in content:
            topics.append("异常处理")
        if "测试" in content:
            topics.append("测试")
        if "函数" in content:
            topics.append("函数")

        # 根据主题数量推断难度
        difficulty = "hard" if len(topics) >= 3 else "medium" if len(topics) >= 1 else "easy"

        return {
            "title": title,
            "topics": topics,
            "difficulty": difficulty
        }


class WriterAgent:
    """writer agent：生成学习计划（支持迭代）"""

    def create_plan(self, note_info: dict, week: int,
                    issues: Optional[List[str]] = None) -> StudyPlan:
        """根据笔记信息和反馈生成学习计划"""
        # 初次生成
        if issues is None:
            return StudyPlan(
                week=week,
                title=note_info["title"],
                prerequisites=[],
                priority="medium"
            )

        # 根据 issues 修复
        plan = StudyPlan(
            week=week,
            title=note_info["title"],
            prerequisites=[],
            priority="medium"
        )

        # 修复 1：添加前置知识
        if any("前置知识" in issue for issue in issues):
            plan.prerequisites = self._infer_prerequisites(week)

        # 修复 2：设置优先级
        if any("优先级" in issue for issue in issues):
            plan.priority = "high" if note_info.get("difficulty") == "hard" else "medium"

        return plan

    def _infer_prerequisites(self, week: int) -> List[str]:
        """推断前置知识（简化版）"""
        prereq_map = {
            3: ["变量"],
            4: ["变量", "if/else"],
            5: ["变量", "文件"],
            6: ["函数", "文件"],
            7: ["异常处理"],
            8: ["异常处理", "函数"],
            9: ["测试"],
            10: ["JSON", "file"],
            11: ["dataclass"],
            12: ["argparse"],
        }
        return prereq_map.get(week, [])


class ReviewerAgent:
    """reviewer agent：检查学习计划质量"""

    def review_plan(self, plan: StudyPlan, all_topics: List[str]) -> List[str]:
        """检查学习计划，返回问题列表"""
        issues = []

        # 检查 1：前置知识不能为空（Week 06+）
        if plan.week >= 6 and not plan.prerequisites:
            issues.append("缺少前置知识")

        # 检查 2：优先级不能为空
        if not plan.priority:
            issues.append("优先级未设置")

        # 检查 3：前置知识必须在所有主题中
        for prereq in plan.prerequisites:
            if prereq not in all_topics:
                issues.append(f"前置知识'{prereq}'未在课程中找到")

        # 检查 4：优先级必须是合法值
        if plan.priority not in ["high", "medium", "low"]:
            issues.append(f"优先级值无效:{plan.priority}")

        return issues


# =====================
# 完整的 agent team 流程
# =====================

def agent_team_pipeline(note_file: Path, week: int,
                       all_topics: List[str]) -> StudyPlan:
    """完整的 agent team 流程"""
    # 创建 agent
    reader = ReaderAgent()
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    # 1. reader agent 读取笔记
    note_info = reader.read_note(note_file)
    print(f"[reader] 读取笔记:{note_info['title']}")
    print(f"  主题:{note_info['topics']}")
    print(f"  难度:{note_info['difficulty']}")

    # 2. writer → reviewer 迭代（最多 3 次）
    for iteration in range(3):
        print(f"\n=== 迭代 {iteration + 1} ===")

        # 第 1 次：初次生成，之后：根据 issues 修复
        issues = None if iteration == 0 else last_issues
        plan = writer.create_plan(note_info, week, issues)

        # 检查
        plan_issues = reviewer.review_plan(plan, all_topics)

        if not plan_issues:
            print("[reviewer] 审查通过!")
            return plan
        else:
            print(f"[reviewer] 审查失败:{plan_issues}")
            last_issues = plan_issues

    print("[warning] 达到最大迭代次数，返回最后一次结果")
    return plan


# =====================
# 使用
# =====================

if __name__ == "__main__":
    # 创建测试笔记文件
    test_note = Path("/tmp/week06_exceptions.md")
    test_note.write_text(
        "# Week 06: 异常处理\n\n"
        "本节讲解：\n"
        "- try/except\n"
        "- 常见异常类型\n"
        "- 异常处理最佳实践\n\n"
        "前置知识：函数、文件操作",
        encoding="utf-8"
    )

    # 定义所有课程主题
    all_topics = ["变量", "函数", "文件", "异常处理", "测试",
                  "JSON", "dataclass", "argparse"]

    # 运行 agent team
    plan = agent_team_pipeline(test_note, week=6, all_topics=all_topics)

    # 输出最终结果
    print(f"\n最终计划:Week {plan.week} - {plan.title}")
    print(f"  前置知识:{plan.prerequisites}")
    print(f"  优先级:{plan.priority}")

    # 清理测试文件
    test_note.unlink()


# =====================
# 总结
# =====================

"""
本示例演示了完整的 agent team 流程：

核心概念：
  1. 流水线（Pipeline）：
     - reader → writer → reviewer
     - 每个 agent 的输出是下一个的输入
     - 类似 Unix 管道：cat file | grep pattern | sort

  2. 职责分离：
     - reader：读取和提取信息
     - writer：生成计划（支持迭代修复）
     - reviewer：检查质量（定义标准）

  3. 失败驱动迭代：
     - writer 和 reviewer 之间形成循环
     - 最多 3 次迭代
     - 每次基于上次的反馈

Agent team 的价值：
  - 可组合：可以随意添加/删除 agent
  - 可测试：每个 agent 可以独立测试
  - 可扩展：新功能 = 新 agent

与之前知识的联系：
  - Week 03 的函数分解：一个函数只做一件事
  - Week 08 的 TDD：红-绿-重构循环
  - Week 11 的 dataclass：数据结构定义
  - Week 12 的 argparse：CLI 工具

与实际工程的对应：
  - reader = 开发者写代码
  - reviewer = code review
  - 迭代循环 = PR 流程：提出 PR → review → 修改 → 再次 review

下一步：
  - 集成到 PyHelper：添加学习计划功能
  - 加上 tester agent：自动生成测试
  - 加上文档 agent：自动生成 README
"""
