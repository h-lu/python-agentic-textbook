#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：失败驱动迭代 - 从测试失败到修复

本示例演示：
1. writer agent：根据反馈修复学习计划
2. reviewer agent：检查计划质量
3. 迭代循环：最多 3 次，失败后修复再检查

运行方式：
    python3 chapters/week_13/examples/03_failure_driven_iteration.py

预期输出：
    === 迭代 1 ===
    [reviewer] 审查失败:['缺少前置知识']

    === 迭代 2 ===
    [reviewer] 审查通过!

    最终计划:Week 6 - 异常处理
      前置知识:['函数', '文件']
      优先级:medium
"""

from dataclasses import dataclass
from typing import List, Optional


# =====================
# 数据模型
# =====================

@dataclass
class StudyPlan:
    """学习计划"""
    week: int
    title: str
    prerequisites: List[str]  # 前置知识
    priority: str  # high/medium/low


# =====================
# Agent 定义
# =====================

class WriterAgent:
    """writer agent：生成学习计划（支持迭代修复）"""

    def create_plan(self, note_info: dict, week: int,
                    issues: Optional[List[str]] = None) -> StudyPlan:
        """根据笔记信息和反馈生成学习计划"""
        # 初次生成
        if issues is None:
            return StudyPlan(
                week=week,
                title=note_info["title"],
                prerequisites=[],  # 初次可能为空
                priority="medium"   # 默认值
            )

        # 根据 issues 修复
        plan = StudyPlan(
            week=week,
            title=note_info["title"],
            prerequisites=[],  # 待填充
            priority="medium"
        )

        # 修复 1：如果 reviewer 说"缺少前置知识"，添加前置
        if any("前置知识" in issue for issue in issues):
            plan.prerequisites = self._infer_prerequisites(week)

        # 修复 2：如果 reviewer 说"优先级未设置"，根据难度推断
        if any("优先级" in issue for issue in issues):
            plan.priority = "high" if note_info.get("difficulty") == "hard" else "medium"

        return plan

    def _infer_prerequisites(self, week: int) -> List[str]:
        """推断前置知识（简化版）"""
        # 实际项目中可以用 AI 分析
        prereq_map = {
            3: ["变量"],
            4: ["变量", "if/else"],
            5: ["变量", "文件"],
            6: ["函数", "文件"],
            7: ["异常处理"],
            8: ["异常处理", "函数"],
            9: ["测试"],
            10: ["JSON", "文件"],
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

        return issues


# =====================
# 失败驱动迭代
# =====================

def iterative_generation(note_info: dict, week: int,
                        all_topics: List[str]) -> StudyPlan:
    """失败驱动迭代：生成学习计划"""
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    for iteration in range(3):
        print(f"\n=== 迭代 {iteration + 1} ===")

        # 第 1 次是初次生成，之后是修复
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

    # 3 次迭代后仍未通过，返回最后一次的结果（警告）
    print("[warning] 达到最大迭代次数，返回最后一次结果")
    return plan


# =====================
# 使用
# =====================

if __name__ == "__main__":
    # 模拟笔记信息
    note_info = {
        "title": "异常处理",
        "difficulty": "medium"
    }
    all_topics = ["变量", "函数", "文件", "异常处理", "测试", "JSON", "dataclass", "argparse"]

    # 失败驱动迭代
    plan = iterative_generation(note_info, week=6, all_topics=all_topics)

    # 输出最终结果
    print(f"\n最终计划:Week {plan.week} - {plan.title}")
    print(f"  前置知识:{plan.prerequisites}")
    print(f"  优先级:{plan.priority}")


# =====================
# 总结
# =====================

"""
本示例演示了失败驱动迭代的核心概念：

核心概念：
  1. 反馈循环：
     - tester/reviewer 发现问题
     - writer 根据反馈修复
     - 再次测试
     - 重复直到通过或达到上限

  2. 最大迭代次数：
     - 不能无限迭代（可能永远修不好）
     - 设置上限（如 3 次）
     - 超过上限后返回最后一次结果并警告

  3. 基于反馈的修复：
     - 初次生成：issues=None
     - 修复生成：issues=[问题列表]
     - writer 根据 issues 选择修复策略

与 TDD 的相似性：
  - Week 08 的 TDD 循环：红（测试失败）→ 绿（写代码通过）→ 重构
  - 本周的迭代循环：失败（reviewer 发现问题）→ 修复（writer 改进）→ 验证

与之前知识的联系：
  - Week 02 的 while 循环：需要终止条件
  - Week 08 的 pytest：定义"什么算通过"
  - Week 06 的异常处理：try/except 捕获失败

实践建议：
  - 设置合理的最大迭代次数（3-5 次）
  - 保留最后一次结果，即使未完全通过
  - 人类要审查最终结果，不要盲目信任 AI

下一步：
  - 完整的 agent team：reader → writer → reviewer
  - 集成到 PyHelper：添加学习计划功能
"""
