"""测试 WriterAgent

测试根据笔记信息生成学习计划的功能
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))

try:
    from solution import NoteInfo, StudyPlan, WriterAgent
    SOLUTION_AVAILABLE = True
except ImportError:
    SOLUTION_AVAILABLE = False


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestWriterAgentBasic:
    """测试 WriterAgent 基本功能"""

    def test_writer_agent_instantiation(self):
        """测试 WriterAgent 可以实例化"""
        agent = WriterAgent()
        assert agent is not None
        assert hasattr(agent, 'create_plan')

    def test_create_plan_returns_study_plan(self):
        """测试 create_plan 返回 StudyPlan 对象"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="函数基础",
            topics=["函数"],
            difficulty="easy"
        )

        result = agent.create_plan(note_info, week=3)

        assert isinstance(result, StudyPlan)
        assert hasattr(result, 'week')
        assert hasattr(result, 'title')
        assert hasattr(result, 'prerequisites')
        assert hasattr(result, 'priority')
        assert hasattr(result, 'topics')
        assert hasattr(result, 'estimated_hours')


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestWriterAgentHappyPath:
    """测试 WriterAgent 正常情况（Happy Path）"""

    def test_create_plan_basic(self):
        """测试基本的学习计划生成"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="异常处理",
            topics=["异常处理", "try/except"],
            difficulty="medium"
        )

        plan = agent.create_plan(note_info, week=6)

        assert plan.week == 6
        assert plan.title == "异常处理"
        assert plan.topics == ["异常处理", "try/except"]
        assert isinstance(plan.prerequisites, list)
        assert plan.priority in ["high", "medium", "low"]
        assert isinstance(plan.estimated_hours, int)

    def test_create_plan_with_easy_difficulty(self):
        """测试简单难度的计划生成"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="Python 入门",
            topics=["变量"],
            difficulty="easy"
        )

        plan = agent.create_plan(note_info, week=1)

        # 初次生成使用默认值
        assert plan.priority == "medium"  # 默认 medium 优先级
        assert plan.estimated_hours == 7  # 默认时长
        # 难度信息保存在 note_info 中，初次生成时不直接使用

    def test_create_plan_with_hard_difficulty(self):
        """测试困难难度的计划生成"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="综合实战",
            topics=["函数", "异常处理", "测试", "文件"],
            difficulty="hard"
        )

        plan = agent.create_plan(note_info, week=10)

        # 初次生成使用默认值（不根据难度调整）
        assert plan.priority == "medium"
        assert plan.estimated_hours == 7

    def test_create_plan_preserves_topics(self):
        """测试生成的计划保留原始主题"""
        agent = WriterAgent()
        original_topics = ["函数", "参数", "返回值", "作用域"]
        note_info = NoteInfo(
            title="函数深入",
            topics=original_topics,
            difficulty="hard"
        )

        plan = agent.create_plan(note_info, week=4)

        assert plan.topics == original_topics

    def test_create_plan_preserves_title(self):
        """测试生成的计划保留原始标题"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="Week 08: 单元测试入门",
            topics=["测试"],
            difficulty="medium"
        )

        plan = agent.create_plan(note_info, week=8)

        assert plan.title == "Week 08: 单元测试入门"


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestWriterAgentEdgeCases:
    """测试 WriterAgent 边界情况"""

    def test_create_plan_with_empty_topics(self):
        """测试空主题列表（边界情况）"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="简介",
            topics=[],
            difficulty="easy"
        )

        plan = agent.create_plan(note_info, week=1)

        assert isinstance(plan, StudyPlan)
        assert plan.topics == []

    def test_create_plan_week_zero(self):
        """测试周次为 0（边界情况）"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="导学",
            topics=["介绍"],
            difficulty="easy"
        )

        plan = agent.create_plan(note_info, week=0)

        assert plan.week == 0
        assert isinstance(plan, StudyPlan)

    def test_create_plan_large_week_number(self):
        """测试大周次数字（边界情况）"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="高级主题",
            topics=["高级"],
            difficulty="hard"
        )

        plan = agent.create_plan(note_info, week=14)

        assert plan.week == 14
        assert isinstance(plan, StudyPlan)

    def test_create_plan_with_many_prerequisites(self):
        """测试多个前置知识（边界情况）"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="综合项目",
            topics=["项目"],
            difficulty="hard"
        )

        # 第二次迭代，传入 issues 让它填充前置知识
        plan = agent.create_plan(
            note_info,
            week=14,
            issues=["缺少前置知识"]
        )

        # 应该填充前置知识（虽然具体内容由实现决定）
        assert isinstance(plan.prerequisites, list)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestWriterAgentIteration:
    """测试 WriterAgent 迭代修复功能"""

    def test_create_plan_first_iteration_no_issues(self):
        """测试第一次迭代（没有 issues）"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="函数",
            topics=["函数"],
            difficulty="medium"
        )

        plan = agent.create_plan(note_info, week=3, issues=None)

        # 第一次迭代应该返回基础计划
        assert isinstance(plan, StudyPlan)

    def test_create_plan_with_priority_issue(self):
        """测试修复优先级问题"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="异常处理",
            topics=["异常处理"],
            difficulty="hard"
        )

        # 第一次：默认 medium
        plan1 = agent.create_plan(note_info, week=6, issues=None)
        assert plan1.priority == "medium"

        # 第二次：传入"优先级"问题
        plan2 = agent.create_plan(
            note_info,
            week=6,
            issues=["优先级未设置"]
        )

        # 应该根据难度修复优先级
        assert plan2.priority == "high"  # hard 难度 → high 优先级

    def test_create_plan_with_prerequisite_issue(self):
        """测试修复前置知识问题"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="异常处理",
            topics=["异常处理"],
            difficulty="medium"
        )

        # 第一次：空前置知识
        plan1 = agent.create_plan(note_info, week=6, issues=None)
        assert plan1.prerequisites == []

        # 第二次：传入"缺少前置知识"问题
        plan2 = agent.create_plan(
            note_info,
            week=6,
            issues=["缺少前置知识"]
        )

        # 应该填充前置知识
        assert len(plan2.prerequisites) > 0

    def test_create_plan_with_hours_issue(self):
        """测试修复时长问题"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="函数",
            topics=["函数"],
            difficulty="medium"
        )

        # 第一次：默认时长
        plan1 = agent.create_plan(note_info, week=3, issues=None)
        assert plan1.estimated_hours == 7

        # 第二次：传入"估算时长"问题
        plan2 = agent.create_plan(
            note_info,
            week=3,
            issues=["估算时长不合理"]
        )

        # 应该根据难度调整时长
        assert plan2.estimated_hours in [4, 7, 10]  # 根据难度

    def test_create_plan_multiple_issues(self):
        """测试同时修复多个问题"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="测试",
            topics=["测试"],
            difficulty="hard"
        )

        # 传入多个问题
        plan = agent.create_plan(
            note_info,
            week=8,
            issues=[
                "缺少前置知识",
                "优先级未设置",
                "估算时长不合理"
            ]
        )

        # 应该修复所有问题
        assert len(plan.prerequisites) > 0 or plan.week < 6
        assert plan.priority == "high"
        assert plan.estimated_hours == 10  # hard → 10 小时


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestWriterAgentPrerequisiteInference:
    """测试前置知识推断"""

    def test_infer_prerequisites_week_6(self):
        """测试 Week 06 的前置知识推断"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="异常处理",
            topics=["异常处理"],
            difficulty="medium"
        )

        plan = agent.create_plan(
            note_info,
            week=6,
            issues=["缺少前置知识"]
        )

        # Week 06 应该有函数和文件作为前置
        assert "函数" in plan.prerequisites

    def test_infer_prerequisites_week_8(self):
        """测试 Week 08 的前置知识推断"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="测试",
            topics=["测试"],
            difficulty="medium"
        )

        plan = agent.create_plan(
            note_info,
            week=8,
            issues=["缺少前置知识"]
        )

        # Week 08 应该有异常处理和函数作为前置
        assert len(plan.prerequisites) > 0

    def test_infer_prerequisites_early_weeks(self):
        """测试早期周次没有前置知识"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="入门",
            topics=["变量"],
            difficulty="easy"
        )

        plan = agent.create_plan(
            note_info,
            week=2,
            issues=["缺少前置知识"]
        )

        # 早期周次可能没有前置知识
        assert isinstance(plan.prerequisites, list)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestWriterAgentPriorityMapping:
    """测试优先级映射逻辑"""

    def test_priority_easy_difficulty(self):
        """测试 easy 难度对应 medium 优先级"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="简单",
            topics=[],
            difficulty="easy"
        )

        plan = agent.create_plan(
            note_info,
            week=1,
            issues=["优先级未设置"]
        )

        assert plan.priority == "medium"

    def test_priority_medium_difficulty(self):
        """测试 medium 难度对应 medium 优先级"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="中等",
            topics=["变量"],
            difficulty="medium"
        )

        plan = agent.create_plan(
            note_info,
            week=5,
            issues=["优先级未设置"]
        )

        assert plan.priority == "medium"

    def test_priority_hard_difficulty(self):
        """测试 hard 难度对应 high 优先级"""
        agent = WriterAgent()
        note_info = NoteInfo(
            title="困难",
            topics=["函数", "异常", "测试"],
            difficulty="hard"
        )

        plan = agent.create_plan(
            note_info,
            week=10,
            issues=["优先级未设置"]
        )

        assert plan.priority == "high"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
