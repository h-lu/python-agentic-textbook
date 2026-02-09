#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Week 13 作业参考实现

本文件是作业的参考实现，当你在作业中遇到困难时可以查看。
请注意：
1. 这只是基础要求的实现，进阶部分需要你自己完成
2. 不要直接复制，理解后用自己的方式实现
3. 可以在此基础上添加你自己的改进

作业要求：
1. 用 dataclass 定义 agent 之间的消息格式（NoteInfo, StudyPlan, ReviewResult）
2. 实现 ReaderAgent：读取并分析笔记文件
3. 实现 WriterAgent：根据笔记信息生成学习计划
4. 实现 ReviewerAgent：检查生成的代码/计划质量
5. 实现失败驱动迭代：最多迭代 3 次，每次基于上一次的反馈修复

进阶挑战：
1. 实现 TesterAgent：自动生成 pytest 测试
2. 实现完整的 agent team pipeline
3. 加上 CLI 调用（pyhelper plan generate）
4. 用 logging 记录 agent 协作过程
"""

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


# =====================
# 数据模型（Agent 消息格式）
# =====================

@dataclass
class NoteInfo:
    """笔记信息（Reader agent 的输出）"""
    title: str
    topics: List[str]
    difficulty: str  # easy/medium/hard


@dataclass
class StudyPlan:
    """学习计划（Writer agent 的输出）"""
    week: int
    title: str
    prerequisites: List[str]  # 前置知识
    priority: str  # high/medium/low
    topics: List[str]
    estimated_hours: int


@dataclass
class ReviewResult:
    """审查结果（Reviewer agent 的输出）"""
    passed: bool
    issues: List[str]


# =====================
# 日志配置
# =====================

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


# =====================
# Agent 实现
# =====================

class ReaderAgent:
    """Reader Agent: 读取并分析笔记文件"""

    def read_note(self, file_path: Path) -> NoteInfo:
        """
        读取并分析笔记文件

        Args:
            file_path: 笔记文件路径

        Returns:
            NoteInfo: 分析结果（标题、主题、难度）

        Raises:
            FileNotFoundError: 文件不存在
            Exception: 其他读取错误
        """
        logger.info(f"读取笔记: {file_path}")

        try:
            content = file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            logger.error(f"文件不存在: {file_path}")
            raise
        except Exception as e:
            logger.error(f"读取失败: {e}")
            raise

        # 提取标题（第一个 # 标题）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem

        # 简化版：提取主题（实际可用 NLP/AI）
        topics = []
        if "异常" in content or "exception" in content.lower():
            topics.append("异常处理")
        if "测试" in content or "test" in content.lower():
            topics.append("测试")
        if "函数" in content or "function" in content.lower():
            topics.append("函数")
        if "变量" in content or "variable" in content.lower():
            topics.append("变量")

        # 简化版：根据主题数量推断难度
        difficulty = "hard" if len(topics) >= 3 else ("medium" if len(topics) >= 1 else "easy")

        return NoteInfo(
            title=title,
            topics=topics,
            difficulty=difficulty
        )


class WriterAgent:
    """Writer Agent: 根据笔记信息生成学习计划"""

    def create_plan(self, note_info: NoteInfo, week: int,
                   issues: Optional[List[str]] = None) -> StudyPlan:
        """
        生成学习计划（支持迭代修复）

        Args:
            note_info: 笔记信息
            week: 周次
            issues: 上一轮审查发现的问题（用于迭代修复）

        Returns:
            StudyPlan: 生成的学习计划
        """
        logger.info(f"生成学习计划: Week {week} - {note_info.title}")

        # 初次生成（使用默认值）
        if issues is None:
            return StudyPlan(
                week=week,
                title=note_info.title,
                prerequisites=[],  # 初次可能为空
                priority="medium",  # 默认值
                topics=note_info.topics,
                estimated_hours=7  # 默认值
            )

        # 根据 issues 修复
        plan = StudyPlan(
            week=week,
            title=note_info.title,
            prerequisites=[],
            priority="medium",  # 默认值，后续可能调整
            topics=note_info.topics,
            estimated_hours=7  # 默认值，后续可能调整
        )

        # 修复 1: 如果 reviewer 说"缺少前置知识"，添加前置
        if any("前置知识" in issue for issue in issues):
            plan.prerequisites = self._infer_prerequisites(week)

        # 修复 2: 如果 reviewer 说"优先级未设置"，根据难度推断
        if any("优先级" in issue for issue in issues):
            plan.priority = "high" if note_info.difficulty == "hard" else "medium"

        # 修复 3: 如果 reviewer 说"估算时长不合理"，根据难度调整
        if any("估算时长" in issue for issue in issues):
            hours_map = {"easy": 4, "medium": 7, "hard": 10}
            plan.estimated_hours = hours_map.get(note_info.difficulty, 7)

        return plan

    def _infer_prerequisites(self, week: int) -> List[str]:
        """推断前置知识（简化版）"""
        if week == 6:
            return ["函数", "文件"]
        elif week == 8:
            return ["异常处理", "函数"]
        elif week == 10:
            return ["文件", "JSON"]
        elif week == 11:
            return ["JSON", "类"]
        elif week == 12:
            return ["dataclass", "argparse"]
        else:
            return []


class ReviewerAgent:
    """Reviewer Agent: 检查学习计划质量"""

    def review_plan(self, plan: StudyPlan, all_topics: List[str]) -> List[str]:
        """
        审查学习计划质量

        Args:
            plan: 学习计划
            all_topics: 所有主题列表（用于检查前置知识是否存在）

        Returns:
            List[str]: 发现的问题列表（空列表表示通过）
        """
        logger.info(f"审查学习计划: Week {plan.week}")

        issues = []

        # 检查 1: 前置知识不能为空（Week 06+）
        if plan.week >= 6 and not plan.prerequisites:
            issues.append("缺少前置知识")

        # 检查 2: 前置知识必须在所有主题中
        for prereq in plan.prerequisites:
            if prereq not in all_topics:
                issues.append(f"前置知识'{prereq}'未在课程中找到")

        # 检查 3: 优先级不能为空
        if not plan.priority:
            issues.append("优先级未设置")

        # 检查 4: 估算时长必须合理（4-15 小时）
        if plan.estimated_hours < 4 or plan.estimated_hours > 15:
            issues.append(f"估算时长不合理: {plan.estimated_hours} 小时")

        return issues


# =====================
# 失败驱动迭代
# =====================

def iterative_plan_generation(note_info: NoteInfo, week: int,
                            all_topics: List[str]) -> StudyPlan:
    """
    失败驱动迭代：生成学习计划

    Args:
        note_info: 笔记信息
        week: 周次
        all_topics: 所有主题列表

    Returns:
        StudyPlan: 最终生成的学习计划（可能未完全通过审查）
    """
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    for iteration in range(3):
        logger.info(f"迭代 {iteration + 1}/3")

        # 第 1 次是初次生成，之后是修复
        issues = None if iteration == 0 else last_issues
        plan = writer.create_plan(note_info, week, issues)

        # 检查
        plan_issues = reviewer.review_plan(plan, all_topics)

        if not plan_issues:
            logger.info("审查通过!")
            return plan
        else:
            logger.warning(f"审查失败: {plan_issues}")
            last_issues = plan_issues

    logger.warning("达到最大迭代次数")
    return plan


# =====================
# 辅助函数
# =====================

def create_note_info(title: str, topics: List[str],
                    difficulty: str = "medium") -> NoteInfo:
    """创建 NoteInfo 的便捷函数"""
    return NoteInfo(title=title, topics=topics, difficulty=difficulty)


def create_study_plan(week: int, title: str, prerequisites: List[str] = None,
                     priority: str = "medium", topics: List[str] = None,
                     estimated_hours: int = 7) -> StudyPlan:
    """创建 StudyPlan 的便捷函数"""
    if topics is None:
        topics = []
    if prerequisites is None:
        prerequisites = []
    return StudyPlan(
        week=week,
        title=title,
        prerequisites=prerequisites,
        priority=priority,
        topics=topics,
        estimated_hours=estimated_hours
    )


def create_review_result(passed: bool, issues: List[str]) -> ReviewResult:
    """创建 ReviewResult 的便捷函数"""
    return ReviewResult(passed=passed, issues=issues)


if __name__ == "__main__":
    # 简单测试
    print("Week 13 - Agent Team 模式")
    print("=" * 50)

    # 测试 dataclass
    note_info = create_note_info(
        title="异常处理",
        topics=["异常处理", "函数"],
        difficulty="medium"
    )
    print(f"NoteInfo: {note_info}")

    plan = create_study_plan(
        week=6,
        title="异常处理",
        prerequisites=["函数", "文件"],
        priority="high",
        topics=["异常处理"],
        estimated_hours=7
    )
    print(f"StudyPlan: {plan}")

    result = create_review_result(
        passed=True,
        issues=[]
    )
    print(f"ReviewResult: {result}")

    print("\n所有 dataclass 创建成功!")
