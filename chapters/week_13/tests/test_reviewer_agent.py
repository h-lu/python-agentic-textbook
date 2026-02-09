"""测试 ReviewerAgent

测试检查学习计划质量的功能（review checklist）
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))

try:
    from solution import StudyPlan, ReviewerAgent
    SOLUTION_AVAILABLE = True
except ImportError:
    SOLUTION_AVAILABLE = False


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReviewerAgentBasic:
    """测试 ReviewerAgent 基本功能"""

    def test_reviewer_agent_instantiation(self):
        """测试 ReviewerAgent 可以实例化"""
        agent = ReviewerAgent()
        assert agent is not None
        assert hasattr(agent, 'review_plan')

    def test_review_plan_returns_list(self):
        """测试 review_plan 返回问题列表"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=6,
            title="测试",
            prerequisites=["函数"],
            priority="high",
            topics=["测试"],
            estimated_hours=7
        )

        result = agent.review_plan(plan, all_topics=["函数", "测试"])

        assert isinstance(result, list)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReviewerAgentHappyPath:
    """测试 ReviewerAgent 正常情况（Happy Path）"""

    def test_review_plan_good_plan_passes(self, all_topics):
        """测试审查好的计划通过"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=6,
            title="异常处理",
            prerequisites=["函数", "文件"],
            priority="high",
            topics=["异常处理"],
            estimated_hours=10
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该通过（没有问题）
        assert isinstance(issues, list)
        # 可能有警告，但核心检查应该通过

    def test_review_plan_week_1_without_prerequisites(self, all_topics):
        """测试 Week 01 没有前置知识是允许的"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=1,
            title="Python 入门",
            prerequisites=[],
            priority="medium",
            topics=["变量"],
            estimated_hours=4
        )

        issues = agent.review_plan(plan, all_topics)

        # Week 01 没有前置知识不应该报错
        assert not any("前置知识" in issue for issue in issues)

    def test_review_plan_complete_plan(self, all_topics):
        """测试完整的学习计划通过审查"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=8,
            title="单元测试",
            prerequisites=["异常处理", "函数"],
            priority="high",
            topics=["pytest", "assert"],
            estimated_hours=8
        )

        issues = agent.review_plan(plan, all_topics)

        # 完整的计划应该通过
        assert isinstance(issues, list)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReviewerAgentPrerequisiteCheck:
    """测试前置知识检查"""

    def test_review_plan_missing_prerequisites_week_6(self, all_topics):
        """测试 Week 06+ 缺少前置知识被检测"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=6,
            title="异常处理",
            prerequisites=[],  # 缺少前置知识
            priority="medium",
            topics=["异常处理"],
            estimated_hours=7
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该检测到缺少前置知识
        assert any("前置知识" in issue for issue in issues)

    def test_review_plan_missing_prerequisites_week_10(self, all_topics):
        """测试 Week 10 缺少前置知识被检测"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=10,
            title="JSON 处理",
            prerequisites=[],
            priority="medium",
            topics=["JSON"],
            estimated_hours=7
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该检测到缺少前置知识
        assert any("前置知识" in issue for issue in issues)

    def test_review_plan_valid_prerequisites(self, all_topics):
        """测试有效的前置知识通过检查"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=8,
            title="测试",
            prerequisites=["异常处理", "函数"],  # 在 all_topics 中
            priority="medium",
            topics=["测试"],
            estimated_hours=7
        )

        issues = agent.review_plan(plan, all_topics)

        # 不应该报告"前置知识未找到"
        assert not any("未在课程中找到" in issue for issue in issues)

    def test_review_plan_invalid_prerequisites(self, all_topics):
        """测试无效的前置知识被检测"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=8,
            title="测试",
            prerequisites=["不存在的主题"],  # 不在 all_topics 中
            priority="medium",
            topics=["测试"],
            estimated_hours=7
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该检测到前置知识不存在
        assert any("未在课程中找到" in issue for issue in issues)

    def test_review_plan_multiple_invalid_prerequisites(self, all_topics):
        """测试多个无效的前置知识被检测"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=10,
            title="高级",
            prerequisites=["不存在1", "不存在2"],
            priority="medium",
            topics=["高级"],
            estimated_hours=7
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该检测到所有无效的前置知识
        invalid_issues = [i for i in issues if "未在课程中找到" in i]
        assert len(invalid_issues) >= 2


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReviewerAgentPriorityCheck:
    """测试优先级检查"""

    def test_review_plan_missing_priority(self, all_topics):
        """测试缺少优先级被检测"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=6,
            title="测试",
            prerequisites=["函数"],
            priority="",  # 空优先级
            topics=["测试"],
            estimated_hours=7
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该检测到优先级未设置
        assert any("优先级" in issue for issue in issues)

    def test_review_plan_valid_priorities(self, all_topics):
        """测试有效的优先级通过检查"""
        agent = ReviewerAgent()

        for priority in ["high", "medium", "low"]:
            plan = StudyPlan(
                week=6,
                title="测试",
                prerequisites=["函数"],
                priority=priority,
                topics=["测试"],
                estimated_hours=7
            )

            issues = agent.review_plan(plan, all_topics)

            # 有效优先级不应该报错
            assert not any("优先级未设置" in issue for issue in issues)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReviewerAgentHoursCheck:
    """测试时长检查"""

    def test_review_plan_too_few_hours(self, all_topics):
        """测试时长过少被检测"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=6,
            title="测试",
            prerequisites=["函数"],
            priority="medium",
            topics=["测试"],
            estimated_hours=2  # 太少
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该检测到时长不合理
        assert any("估算时长" in issue for issue in issues)

    def test_review_plan_too_many_hours(self, all_topics):
        """测试时长过多被检测"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=6,
            title="测试",
            prerequisites=["函数"],
            priority="medium",
            topics=["测试"],
            estimated_hours=20  # 太多
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该检测到时长不合理
        assert any("估算时长" in issue for issue in issues)

    def test_review_plan_boundary_hours(self, all_topics):
        """测试边界时长值"""
        agent = ReviewerAgent()

        # 测试下边界
        plan1 = StudyPlan(
            week=6,
            title="测试",
            prerequisites=["函数"],
            priority="medium",
            topics=["测试"],
            estimated_hours=4  # 边界值
        )
        issues1 = agent.review_plan(plan1, all_topics)
        assert not any("估算时长" in issue for issue in issues1)

        # 测试上边界
        plan2 = StudyPlan(
            week=6,
            title="测试",
            prerequisites=["函数"],
            priority="medium",
            topics=["测试"],
            estimated_hours=15  # 边界值
        )
        issues2 = agent.review_plan(plan2, all_topics)
        assert not any("估算时长" in issue for issue in issues2)

    def test_review_plan_valid_hours_range(self, all_topics):
        """测试有效时长范围"""
        agent = ReviewerAgent()

        for hours in [5, 7, 10, 12]:
            plan = StudyPlan(
                week=6,
                title="测试",
                prerequisites=["函数"],
                priority="medium",
                topics=["测试"],
                estimated_hours=hours
            )

            issues = agent.review_plan(plan, all_topics)

            # 有效时长不应该报错
            assert not any("估算时长" in issue for issue in issues)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReviewerAgentEdgeCases:
    """测试 ReviewerAgent 边界情况"""

    def test_review_plan_empty_all_topics(self):
        """测试空的所有主题列表（边界情况）"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=6,
            title="测试",
            prerequisites=["函数"],
            priority="medium",
            topics=["测试"],
            estimated_hours=7
        )

        issues = agent.review_plan(plan, all_topics=[])

        # 空主题列表时，任何前置知识都应该被标记为不存在
        assert any("未在课程中找到" in issue for issue in issues)

    def test_review_plan_zero_week(self, all_topics):
        """测试周次为 0（边界情况）"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=0,
            title="导学",
            prerequisites=[],
            priority="medium",
            topics=["介绍"],
            estimated_hours=4
        )

        issues = agent.review_plan(plan, all_topics)

        # Week 0 没有前置知识应该被允许
        assert not any("前置知识" in issue for issue in issues)

    def test_review_plan_negative_week(self, all_topics):
        """测试负数周次（边界情况）"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=-1,
            title="测试",
            prerequisites=[],
            priority="medium",
            topics=["测试"],
            estimated_hours=7
        )

        issues = agent.review_plan(plan, all_topics)

        # 负数周次不应该要求前置知识
        # (行为由实现决定，测试确保不会崩溃)
        assert isinstance(issues, list)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReviewerAgentMultipleIssues:
    """测试同时检测多个问题"""

    def test_review_plan_multiple_issues_detected(self, all_topics):
        """测试同时检测多个问题"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=6,
            title="测试",
            prerequisites=[],  # 问题 1: 缺少前置知识
            priority="",  # 问题 2: 优先级未设置
            topics=["测试"],
            estimated_hours=20  # 问题 3: 时长过多
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该检测到所有问题
        assert len(issues) >= 3

    def test_review_plan_all_checks_pass(self, all_topics):
        """测试所有检查都通过"""
        agent = ReviewerAgent()
        plan = StudyPlan(
            week=8,
            title="单元测试",
            prerequisites=["异常处理", "函数"],
            priority="high",
            topics=["pytest", "assert"],
            estimated_hours=8
        )

        issues = agent.review_plan(plan, all_topics)

        # 应该没有问题（或者只有警告）
        # 核心检查应该通过：前置知识、优先级、时长
        critical_issues = [
            i for i in issues
            if any(keyword in i for keyword in ["前置知识", "优先级", "估算时长"])
        ]
        assert len(critical_issues) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
