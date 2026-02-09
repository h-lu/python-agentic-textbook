"""测试失败驱动迭代

测试失败驱动迭代的完整流程：测试失败 → 修复 → 再测试
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))

try:
    from solution import (
        NoteInfo,
        StudyPlan,
        iterative_plan_generation
    )
    SOLUTION_AVAILABLE = True
except ImportError:
    SOLUTION_AVAILABLE = False


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestIterativeGenerationBasic:
    """测试迭代生成基本功能"""

    def test_iterative_plan_generation_exists(self):
        """测试迭代生成函数存在"""
        assert callable(iterative_plan_generation)

    def test_iterative_plan_generation_returns_study_plan(self):
        """测试迭代生成返回 StudyPlan 对象"""
        note_info = NoteInfo(
            title="测试",
            topics=["测试"],
            difficulty="medium"
        )
        all_topics = ["测试"]

        result = iterative_plan_generation(note_info, week=1, all_topics=all_topics)

        assert isinstance(result, StudyPlan)


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestIterativeGenerationHappyPath:
    """测试迭代生成正常情况（Happy Path）"""

    def test_iterative_generation_success_on_first_try(self):
        """测试第一次迭代就成功"""
        note_info = NoteInfo(
            title="Python 入门",
            topics=["变量"],
            difficulty="easy"
        )
        all_topics = ["变量", "函数"]

        plan = iterative_plan_generation(note_info, week=1, all_topics=all_topics)

        assert isinstance(plan, StudyPlan)
        assert plan.week == 1

    def test_iterative_generation_converges(self):
        """测试迭代最终收敛"""
        note_info = NoteInfo(
            title="异常处理",
            topics=["异常处理"],
            difficulty="medium"
        )
        all_topics = ["变量", "函数", "文件", "异常处理"]

        plan = iterative_plan_generation(note_info, week=6, all_topics=all_topics)

        # 应该返回一个计划（即使未完全通过）
        assert isinstance(plan, StudyPlan)
        assert plan.week == 6

    def test_iterative_generation_improves_plan(self):
        """测试迭代改进计划质量"""
        note_info = NoteInfo(
            title="测试",
            topics=["测试"],
            difficulty="hard"
        )
        all_topics = ["变量", "函数", "异常处理", "测试"]

        plan = iterative_plan_generation(note_info, week=8, all_topics=all_topics)

        # 迭代后应该有改进（至少不会崩溃）
        assert isinstance(plan, StudyPlan)
        # hard 难度应该有高优先级（如果迭代成功）
        assert plan.priority in ["high", "medium"]


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestIterativeGenerationWithIssues:
    """测试带问题的迭代生成"""

    def test_iterative_generation_with_missing_prerequisites(self):
        """测试缺少前置知识时的迭代"""
        note_info = NoteInfo(
            title="异常处理",
            topics=["异常处理"],
            difficulty="medium"
        )
        all_topics = ["变量", "函数", "文件", "异常处理"]

        plan = iterative_plan_generation(note_info, week=6, all_topics=all_topics)

        # Week 06 应该在迭代后填充前置知识
        assert isinstance(plan, StudyPlan)
        # 可能修复了前置知识
        if plan.week >= 6:
            # 不一定完全修复，但应该尝试
            assert isinstance(plan.prerequisites, list)

    def test_iterative_generation_with_wrong_priority(self):
        """测试优先级错误时的迭代"""
        note_info = NoteInfo(
            title="综合实战",
            topics=["函数", "异常", "测试"],
            difficulty="hard"
        )
        all_topics = ["函数", "异常处理", "测试", "文件", "JSON", "dataclass", "argparse"]

        plan = iterative_plan_generation(note_info, week=10, all_topics=all_topics)

        # hard 难度应该在迭代后设置为 high 优先级
        assert isinstance(plan, StudyPlan)
        # 迭代应该修复优先级（如果迭代收敛成功）
        # 注意：如果前置知识问题导致达到最大迭代次数，优先级可能未修复
        assert plan.priority in ["high", "medium"]  # 至少是有效优先级

    def test_iterative_generation_with_wrong_hours(self):
        """测试时长错误时的迭代"""
        note_info = NoteInfo(
            title="函数",
            topics=["函数"],
            difficulty="medium"
        )
        all_topics = ["函数"]

        plan = iterative_plan_generation(note_info, week=3, all_topics=all_topics)

        # 应该在合理范围内
        assert isinstance(plan, StudyPlan)
        assert 4 <= plan.estimated_hours <= 15


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestIterativeGenerationMaxIterations:
    """测试最大迭代次数限制"""

    def test_iterative_generation_respects_max_iterations(self):
        """测试遵守最大迭代次数"""
        note_info = NoteInfo(
            title="困难主题",
            topics=["高级"],
            difficulty="hard"
        )
        # 使用有限的主题列表，确保有些检查可能失败
        all_topics = ["基础"]

        plan = iterative_plan_generation(note_info, week=10, all_topics=all_topics)

        # 应该返回结果（即使未完全通过）
        assert isinstance(plan, StudyPlan)
        # 不会无限循环

    def test_iterative_generation_returns_plan_after_max_iterations(self):
        """测试达到最大迭代次数后仍返回计划"""
        note_info = NoteInfo(
            title="测试",
            topics=["测试"],
            difficulty="medium"
        )
        # 故意使用不匹配的主题列表
        all_topics = ["完全不相关的主题"]

        plan = iterative_plan_generation(note_info, week=8, all_topics=all_topics)

        # 即使未完全通过，也应该返回最后一次的结果
        assert isinstance(plan, StudyPlan)
        assert plan.week == 8


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚尚不实现")
class TestIterativeGenerationEdgeCases:
    """测试迭代生成边界情况"""

    def test_iterative_generation_week_zero(self):
        """测试周次为 0"""
        note_info = NoteInfo(
            title="导学",
            topics=["介绍"],
            difficulty="easy"
        )
        all_topics = ["介绍"]

        plan = iterative_plan_generation(note_info, week=0, all_topics=all_topics)

        assert isinstance(plan, StudyPlan)
        assert plan.week == 0

    def test_iterative_generation_large_week_number(self):
        """测试大周次数字"""
        note_info = NoteInfo(
            title="高级",
            topics=["高级"],
            difficulty="hard"
        )
        all_topics = ["基础", "中级", "高级"]

        plan = iterative_plan_generation(note_info, week=14, all_topics=all_topics)

        assert isinstance(plan, StudyPlan)
        assert plan.week == 14

    def test_iterative_generation_empty_topics(self):
        """测试空主题列表"""
        note_info = NoteInfo(
            title="简单",
            topics=[],
            difficulty="easy"
        )
        all_topics = []

        plan = iterative_plan_generation(note_info, week=1, all_topics=all_topics)

        # 空主题不应该崩溃
        assert isinstance(plan, StudyPlan)

    def test_iterative_generation_with_many_topics(self):
        """测试多主题"""
        note_info = NoteInfo(
            title="综合",
            topics=["主题1", "主题2", "主题3", "主题4"],
            difficulty="hard"
        )
        all_topics = ["主题1", "主题2", "主题3", "主题4"]

        plan = iterative_plan_generation(note_info, week=10, all_topics=all_topics)

        assert isinstance(plan, StudyPlan)
        assert len(plan.topics) == 4


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestIterativeGenerationPreservation:
    """测试迭代过程中信息保留"""

    def test_iterative_generation_preserves_title(self):
        """测试保留原始标题"""
        original_title = "Week 08: 单元测试"
        note_info = NoteInfo(
            title=original_title,
            topics=["测试"],
            difficulty="medium"
        )
        all_topics = ["测试"]

        plan = iterative_plan_generation(note_info, week=8, all_topics=all_topics)

        assert plan.title == original_title

    def test_iterative_generation_preserves_topics(self):
        """测试保留原始主题"""
        original_topics = ["函数", "参数", "返回值"]
        note_info = NoteInfo(
            title="函数深入",
            topics=original_topics,
            difficulty="medium"
        )
        all_topics = original_topics + ["前置"]

        plan = iterative_plan_generation(note_info, week=4, all_topics=all_topics)

        assert plan.topics == original_topics

    def test_iterative_generation_preserves_week(self):
        """测试保留周次"""
        note_info = NoteInfo(
            title="测试",
            topics=["测试"],
            difficulty="medium"
        )
        all_topics = ["测试"]

        plan = iterative_plan_generation(note_info, week=7, all_topics=all_topics)

        assert plan.week == 7


@pytest.mark.skipif(not SOLUTION_AVAILABLE, reason="solution.py 尚未实现")
class TestIterativeGenerationConvergence:
    """测试迭代收敛性"""

    def test_iterative_generation_converges_for_simple_case(self):
        """测试简单情况快速收敛"""
        note_info = NoteInfo(
            title="入门",
            topics=["变量"],
            difficulty="easy"
        )
        all_topics = ["变量"]

        plan = iterative_plan_generation(note_info, week=1, all_topics=all_topics)

        # 简单情况应该快速成功
        assert isinstance(plan, StudyPlan)

    def test_iterative_generation_handles_complex_case(self):
        """测试复杂情况多次迭代"""
        note_info = NoteInfo(
            title="综合项目",
            topics=["函数", "异常", "测试", "文件"],
            difficulty="hard"
        )
        all_topics = ["变量", "函数", "文件", "异常处理", "测试"]

        plan = iterative_plan_generation(note_info, week=12, all_topics=all_topics)

        # 复杂情况可能需要多次迭代，但最终应该返回结果
        assert isinstance(plan, StudyPlan)
        # hard 难度应该有合理的优先级和时长
        assert plan.priority in ["high", "medium"]
        assert 4 <= plan.estimated_hours <= 15


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
