#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：PyHelper 集成 agent team - 为学习计划功能协作开发

本示例演示：
1. reader agent：读取并分析 PyHelper 学习笔记
2. writer agent：根据笔记分析生成学习计划
3. reviewer agent：检查学习计划质量
4. 失败驱动迭代：最多 3 次
5. CLI 集成：pyhelper plan generate 命令

运行方式：
    # 测试 reader agent
    python3 chapters/week_13/examples/13_pyhelper_agent_team.py

    # 作为模块导入
    from chapters.week_13.examples.pyhelper_agent_team import agent_team_pipeline

预期输出：
    [INFO] 读取笔记:/tmp/test_week06.md
    [INFO] 分析结果:Week 6 - 异常处理
    [INFO] 主题:['异常处理']
    [INFO] 难度:medium
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path
import re
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


# =====================
# 数据模型（dataclass）
# =====================

@dataclass
class NoteAnalysis:
    """笔记分析结果（reader agent 的输出）"""
    week: int
    title: str
    topics: List[str]
    difficulty: str  # easy/medium/hard


@dataclass
class StudyPlan:
    """学习计划（writer agent 的输出）"""
    week: int
    title: str
    prerequisites: List[str]
    priority: str  # high/medium/low
    topics: List[str]
    estimated_hours: int

    def to_dict(self) -> dict:
        """转换为字典（用于 JSON 序列化）"""
        return asdict(self)


# =====================
# Agent 定义
# =====================

class ReaderAgent:
    """reader agent：读取并分析笔记文件"""

    def read_note(self, file_path: Path) -> NoteAnalysis:
        """读取笔记文件并提取关键信息"""
        logger.info(f"读取笔记:{file_path}")

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"读取失败:{e}")
            raise

        # 提取周次（从文件名）
        week_match = re.search(r'week(\d+)', file_path.name, re.IGNORECASE)
        week = int(week_match.group(1)) if week_match else 0

        # 提取标题（第一个 # 标题）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem

        # 简化版：提取主题（实际可用 NLP/AI）
        topics = []
        if "异常" in content or "Exception" in content:
            topics.append("异常处理")
        if "测试" in content or "test" in content.lower():
            topics.append("测试")
        if "函数" in content or "def " in content:
            topics.append("函数")
        if "文件" in content or "file" in content.lower():
            topics.append("文件")
        if "JSON" in content or "json" in content.lower():
            topics.append("JSON")
        if "dataclass" in content:
            topics.append("dataclass")
        if "argparse" in content:
            topics.append("argparse")

        # 根据主题数量推断难度
        difficulty = "hard" if len(topics) >= 3 else "medium" if len(topics) >= 1 else "easy"

        analysis = NoteAnalysis(
            week=week,
            title=title,
            topics=topics,
            difficulty=difficulty
        )

        logger.info(f"分析结果:{analysis.title}")
        logger.info(f"  主题:{analysis.topics}")
        logger.info(f"  难度:{analysis.difficulty}")

        return analysis


class WriterAgent:
    """writer agent：根据笔记分析生成学习计划"""

    def create_plan(self, analysis: NoteAnalysis, all_topics: List[str],
                    issues: Optional[List[str]] = None) -> StudyPlan:
        """根据笔记分析生成学习计划（支持迭代修复）"""
        logger.info(f"生成学习计划:Week {analysis.week} - {analysis.title}")

        # 推断前置知识（简化版：根据周次推断）
        if issues is None or not any("前置知识" in issue for issue in issues):
            prerequisites = []
        else:
            prerequisites = self._infer_prerequisites(analysis.week, all_topics)

        # 推断优先级（根据难度）
        priority = "high" if analysis.difficulty == "hard" else "medium"

        # 估算学习时长（根据难度）
        hours_map = {"easy": 4, "medium": 7, "hard": 10}
        estimated_hours = hours_map.get(analysis.difficulty, 7)

        return StudyPlan(
            week=analysis.week,
            title=analysis.title,
            prerequisites=prerequisites,
            priority=priority,
            topics=analysis.topics,
            estimated_hours=estimated_hours
        )

    def _infer_prerequisites(self, week: int, all_topics: List[str]) -> List[str]:
        """推断前置知识（简化版）"""
        # 实际项目中可以用 AI 分析依赖关系
        prereq_map = {
            1: [],
            2: ["变量"],
            3: ["变量", "if/else"],
            4: ["变量", "循环"],
            5: ["变量", "文件"],
            6: ["函数", "文件"],
            7: ["异常处理"],
            8: ["异常处理", "函数"],
            9: ["测试"],
            10: ["JSON", "文件"],
            11: ["dataclass", "类型提示"],
            12: ["argparse", "logging"],
            13: ["agent team", "review checklist"],
            14: ["所有前置知识"],
        }
        return [p for p in prereq_map.get(week, []) if p in all_topics]


class ReviewerAgent:
    """reviewer agent：检查学习计划质量"""

    def review_plan(self, plan: StudyPlan, all_topics: List[str]) -> List[str]:
        """检查学习计划，返回问题列表"""
        logger.info(f"审查学习计划:Week {plan.week}")

        issues = []

        # 检查 1：前置知识不能为空（Week 06+）
        if plan.week >= 6 and not plan.prerequisites:
            issues.append("缺少前置知识")

        # 检查 2：前置知识必须在所有主题中
        for prereq in plan.prerequisites:
            if prereq not in all_topics:
                issues.append(f"前置知识'{prereq}'未在课程中找到")

        # 检查 3：优先级不能为空
        if not plan.priority:
            issues.append("优先级未设置")

        # 检查 4：估算时长必须合理（4-15 小时）
        if plan.estimated_hours < 4 or plan.estimated_hours > 15:
            issues.append(f"估算时长不合理:{plan.estimated_hours} 小时")

        # 检查 5：优先级必须是合法值
        if plan.priority not in ["high", "medium", "low"]:
            issues.append(f"优先级值无效:{plan.priority}")

        return issues


# =====================
# 失败驱动迭代
# =====================

def iterative_plan_generation(analysis: NoteAnalysis,
                             all_topics: List[str]) -> StudyPlan:
    """失败驱动迭代：生成学习计划"""
    writer = WriterAgent()
    reviewer = ReviewerAgent()

    for iteration in range(3):
        logger.info(f"迭代 {iteration + 1}/3")

        # 第 1 次：初次生成，之后：根据 issues 修复
        issues = None if iteration == 0 else last_issues
        plan = writer.create_plan(analysis, all_topics, issues)

        # 检查
        plan_issues = reviewer.review_plan(plan, all_topics)

        if not plan_issues:
            logger.info("审查通过!")
            return plan
        else:
            logger.warning(f"审查失败:{plan_issues}")
            last_issues = plan_issues

    logger.warning("达到最大迭代次数")
    return plan


# =====================
# Agent Team 流水线
# =====================

def agent_team_pipeline(note_file: Path, all_topics: List[str]) -> StudyPlan:
    """完整的 agent team 流程：reader → writer → reviewer"""
    # 创建 agent
    reader = ReaderAgent()

    # reader agent 读取笔记
    analysis = reader.read_note(note_file)

    # writer + reviewer 迭代生成计划
    plan = iterative_plan_generation(analysis, all_topics)

    return plan


def generate_study_plans(notes_dir: Path, output_file: Path) -> int:
    """为所有笔记生成学习计划（CLI 入口）"""
    logger.info("开始生成学习计划")

    # 1. 收集所有笔记文件
    note_files = sorted(notes_dir.glob("week*.md"))

    if not note_files:
        logger.error(f"未找到笔记文件:{notes_dir}")
        return 1

    # 2. 提取所有主题（用于前置知识检查）
    all_topics = [
        "变量", "if/else", "循环", "函数", "文件",
        "异常处理", "测试", "JSON", "dataclass", "类型提示",
        "argparse", "logging", "agent team", "review checklist"
    ]

    # 3. 为每个笔记生成计划
    plans = []

    for note_file in note_files:
        try:
            plan = agent_team_pipeline(note_file, all_topics)
            plans.append(plan)
        except Exception as e:
            logger.error(f"处理 {note_file.name} 失败:{e}")
            continue

    # 4. 导出为 JSON
    plans_dict = [plan.to_dict() for plan in plans]
    output_file.write_text(
        json.dumps(plans_dict, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    logger.info(f"✓ 学习计划已生成:{output_file}")
    logger.info(f"  共 {len(plans)} 周")
    total_hours = sum(p.estimated_hours for p in plans)
    logger.info(f"  总时长:{total_hours} 小时")

    return 0


# =====================
# 测试代码
# =====================

if __name__ == "__main__":
    # 测试 reader agent
    print("=" * 70)
    print("测试 ReaderAgent")
    print("=" * 70)

    # 创建测试笔记文件
    test_note = Path("/tmp/test_week06.md")
    test_note.write_text(
        "# Week 06: 异常处理\n\n"
        "本节讲解：\n"
        "- try/except 语句\n"
        "- 常见异常类型\n"
        "- 异常处理最佳实践\n\n"
        "前置知识：函数、文件操作",
        encoding="utf-8"
    )

    reader = ReaderAgent()
    analysis = reader.read_note(test_note)

    print(f"\n分析结果:")
    print(f"  周次:{analysis.week}")
    print(f"  标题:{analysis.title}")
    print(f"  主题:{analysis.topics}")
    print(f"  难度:{analysis.difficulty}")

    # 清理测试文件
    test_note.unlink()

    # 测试完整的 agent team
    print("\n" + "=" * 70)
    print("测试完整 Agent Team")
    print("=" * 70)

    # 创建多个测试笔记
    test_notes_dir = Path("/tmp/test_pyhelper_notes")
    test_notes_dir.mkdir(exist_ok=True)

    (test_notes_dir / "week01.md").write_text(
        "# Week 01: Python 入门\n\n变量、print、输入输出。", encoding="utf-8")
    (test_notes_dir / "week06.md").write_text(
        "# Week 06: 异常处理\n\ntry/except、异常类型。", encoding="utf-8")
    (test_notes_dir / "week08.md").write_text(
        "# Week 08: 测试\n\npytest、TDD。", encoding="utf-8")

    # 生成学习计划
    output_file = Path("/tmp/test_study_plan.json")
    all_topics = [
        "变量", "if/else", "循环", "函数", "文件",
        "异常处理", "测试", "JSON", "dataclass", "类型提示",
        "argparse", "logging"
    ]

    plans = []
    for note_file in sorted(test_notes_dir.glob("week*.md")):
        try:
            plan = agent_team_pipeline(note_file, all_topics)
            plans.append(plan)
        except Exception as e:
            logger.error(f"处理 {note_file.name} 失败:{e}")

    # 输出结果
    print("\n生成的学习计划:")
    for plan in plans:
        print(f"\nWeek {plan.week}: {plan.title}")
        print(f"  前置知识:{plan.prerequisites}")
        print(f"  优先级:{plan.priority}")
        print(f"  预估时长:{plan.estimated_hours} 小时")

    # 清理测试文件
    for f in test_notes_dir.glob("*"):
        f.unlink()
    test_notes_dir.rmdir()


# =====================
# 总结
# =====================

"""
本示例演示了如何将 agent team 集成到 PyHelper 中：

核心概念：
  1. dataclass 消息格式：
     - NoteAnalysis：reader 的输出
     - StudyPlan：writer 的输出
     - 用 asdict() 序列化为 JSON

  2. Agent 职责：
     - ReaderAgent：读取笔记，提取周次/标题/主题/难度
     - WriterAgent：生成计划，推断前置知识/优先级/时长
     - ReviewerAgent：检查质量，验证前置知识/优先级/时长

  3. 失败驱动迭代：
     - 最多 3 次
     - 根据 reviewer 反馈修复
     - 保留最后一次结果

与之前知识的联系：
  - Week 11 的 dataclass：数据模型定义
  - Week 10 的 JSON：序列化/导出
  - Week 12 的 logging：日志记录
  - Week 06 的异常处理：try/except

CLI 集成（在其他文件中）：
  ```python
  import argparse
  from pyhelper_agent_team import generate_study_plans

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  # plan generate 子命令
  plan_parser = subparsers.add_parser("plan", help="学习计划管理")
  generate_parser = plan_parser.add_subparsers()

  gen_parser = generate_parser.add_parser("generate", help="生成学习计划")
  gen_parser.add_argument("--notes-dir", "-n", default="notes")
  gen_parser.add_argument("--output", "-o", default="study_plan.json")
  gen_parser.set_defaults(func=generate_study_plans)
  ```

使用方式：
  ```bash
  pyhelper plan generate --notes-dir notes --output study_plan.json
  pyhelper plan show --week 6
  pyhelper plan export --format csv
  ```

Agent team 的价值：
  - 清晰的职责分离
  - 可测试、可扩展
  - 模拟真实工程流程（开发 → review → 修复）
  - 人类是技术负责人，AI 是团队成员
"""
