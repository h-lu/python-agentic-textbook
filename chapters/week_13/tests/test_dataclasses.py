"""测试 Dataclass 消息格式

测试 agent 之间传递消息用的 dataclass 结构
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))

try:
    from solution import (
        NoteInfo,
        StudyPlan,
        ReviewResult,
        create_note_info,
        create_study_plan,
        create_review_result
    )
    SOLUTION_AVAILABLE = True
except ImportError:
    SOLUTION_AVAILABLE = False


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestNoteInfo:
    """测试 NoteInfo dataclass"""

    def test_create_note_info_with_all_fields(self):
        """测试创建 NoteInfo 包含所有字段"""
        note_info = NoteInfo(
            title="Python 函数",
            topics=["函数", "参数", "返回值"],
            difficulty="medium"
        )

        assert note_info.title == "Python 函数"
        assert note_info.topics == ["函数", "参数", "返回值"]
        assert note_info.difficulty == "medium"

    def test_create_note_info_with_empty_topics(self):
        """测试创建 NoteInfo 包含空主题列表（边界情况）"""
        note_info = NoteInfo(
            title="简单介绍",
            topics=[],
            difficulty="easy"
        )

        assert note_info.title == "简单介绍"
        assert note_info.topics == []
        assert note_info.difficulty == "easy"

    def test_note_info_equality(self):
        """测试 NoteInfo 相等性比较"""
        note1 = NoteInfo(title="测试", topics=["A"], difficulty="easy")
        note2 = NoteInfo(title="测试", topics=["A"], difficulty="easy")
        note3 = NoteInfo(title="测试", topics=["B"], difficulty="easy")

        # dataclass 自动生成 __eq__
        assert note1 == note2
        assert note1 != note3

    def test_create_note_info_helper_function(self):
        """测试便捷函数 create_note_info"""
        note_info = create_note_info(
            title="异常处理",
            topics=["异常处理", "try", "except"],
            difficulty="hard"
        )

        assert isinstance(note_info, NoteInfo)
        assert note_info.title == "异常处理"
        assert note_info.topics == ["异常处理", "try", "except"]
        assert note_info.difficulty == "hard"

    def test_create_note_info_default_difficulty(self):
        """测试便捷函数的默认难度参数"""
        note_info = create_note_info(
            title="基础概念",
            topics=["变量"]
        )

        assert note_info.difficulty == "medium"


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestStudyPlan:
    """测试 StudyPlan dataclass"""

    def test_create_study_plan_with_all_fields(self):
        """测试创建 StudyPlan 包含所有字段"""
        plan = StudyPlan(
            week=6,
            title="异常处理",
            prerequisites=["函数", "文件"],
            priority="high",
            topics=["异常处理", "try/except"],
            estimated_hours=10
        )

        assert plan.week == 6
        assert plan.title == "异常处理"
        assert plan.prerequisites == ["函数", "文件"]
        assert plan.priority == "high"
        assert plan.topics == ["异常处理", "try/except"]
        assert plan.estimated_hours == 10

    def test_create_study_plan_with_empty_prerequisites(self):
        """测试创建 StudyPlan 包含空前置知识列表（边界情况）"""
        plan = StudyPlan(
            week=1,
            title="Python 入门",
            prerequisites=[],
            priority="medium",
            topics=["变量", "输出"],
            estimated_hours=4
        )

        assert plan.prerequisites == []

    def test_study_plan_equality(self):
        """测试 StudyPlan 相等性比较"""
        plan1 = StudyPlan(
            week=1, title="测试", prerequisites=[],
            priority="low", topics=[], estimated_hours=4
        )
        plan2 = StudyPlan(
            week=1, title="测试", prerequisites=[],
            priority="low", topics=[], estimated_hours=4
        )
        plan3 = StudyPlan(
            week=2, title="测试", prerequisites=[],
            priority="low", topics=[], estimated_hours=4
        )

        assert plan1 == plan2
        assert plan1 != plan3

    def test_create_study_plan_helper_function(self):
        """测试便捷函数 create_study_plan"""
        plan = create_study_plan(
            week=8,
            title="单元测试",
            prerequisites=["异常处理", "函数"],
            priority="high",
            topics=["pytest", "断言"],
            estimated_hours=8
        )

        assert isinstance(plan, StudyPlan)
        assert plan.week == 8
        assert plan.title == "单元测试"
        assert plan.prerequisites == ["异常处理", "函数"]
        assert plan.priority == "high"
        assert plan.topics == ["pytest", "断言"]
        assert plan.estimated_hours == 8

    def test_create_study_plan_default_parameters(self):
        """测试便捷函数的默认参数"""
        plan = create_study_plan(
            week=5,
            title="数据结构"
        )

        assert plan.prerequisites == []
        assert plan.priority == "medium"
        assert plan.topics == []
        assert plan.estimated_hours == 7


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestReviewResult:
    """测试 ReviewResult dataclass"""

    def test_create_review_result_passed(self):
        """测试创建通过的审查结果"""
        result = ReviewResult(
            passed=True,
            issues=[]
        )

        assert result.passed is True
        assert result.issues == []

    def test_create_review_result_failed(self):
        """测试创建失败的审查结果"""
        result = ReviewResult(
            passed=False,
            issues=["缺少错误处理", "未检查空输入"]
        )

        assert result.passed is False
        assert result.issues == ["缺少错误处理", "未检查空输入"]

    def test_review_result_passed_evaluation(self):
        """测试通过审查结果的评估逻辑"""
        # 通过 = 没有问题
        result_pass = ReviewResult(passed=True, issues=[])
        assert result_pass.passed is True
        assert len(result_pass.issues) == 0

        # 失败 = 有问题
        result_fail = ReviewResult(passed=False, issues=["有问题"])
        assert result_fail.passed is False
        assert len(result_fail.issues) > 0

    def test_create_review_result_helper_function(self):
        """测试便捷函数 create_review_result"""
        result = create_review_result(
            passed=False,
            issues=["优先级未设置", "时长不合理"]
        )

        assert isinstance(result, ReviewResult)
        assert result.passed is False
        assert result.issues == ["优先级未设置", "时长不合理"]


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestDataclassIntegration:
    """测试 dataclass 在 agent 之间的传递"""

    def test_note_info_to_study_plan_flow(self):
        """测试 NoteInfo → StudyPlan 的消息流"""
        # Reader agent 输出
        note_info = NoteInfo(
            title="文件操作",
            topics=["文件", "读写", "上下文管理器"],
            difficulty="medium"
        )

        # Writer agent 输入 = Reader agent 输出
        plan = StudyPlan(
            week=5,
            title=note_info.title,
            prerequisites=["变量"],
            priority="high" if note_info.difficulty == "hard" else "medium",
            topics=note_info.topics,
            estimated_hours=7
        )

        assert plan.title == note_info.title
        assert plan.topics == note_info.topics

    def test_study_plan_to_review_result_flow(self):
        """测试 StudyPlan → ReviewResult 的消息流"""
        # Writer agent 输出
        plan = StudyPlan(
            week=6,
            title="异常处理",
            prerequisites=["函数"],
            priority="high",
            topics=["try/except"],
            estimated_hours=10
        )

        # Reviewer agent 输入 = Writer agent 输出
        # 模拟审查逻辑
        issues = []
        if not plan.prerequisites:
            issues.append("缺少前置知识")
        if not plan.priority:
            issues.append("优先级未设置")

        result = ReviewResult(
            passed=len(issues) == 0,
            issues=issues
        )

        assert result.passed is True  # 前置知识不为空，优先级不为空
        assert len(result.issues) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
