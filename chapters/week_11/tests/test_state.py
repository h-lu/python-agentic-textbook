"""Week 11 状态管理测试

测试状态转换规则、状态验证等。
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "starter_code"))

from solution import TaskWithStatus, TaskStatus, validate_state_transition


class TestStateTransitions:
    """测试状态转换"""

    def test_initial_state_is_todo(self):
        """测试初始状态为 TODO"""
        task = TaskWithStatus(title="作业", priority="high")
        assert task.status == TaskStatus.TODO

    def test_todo_to_in_progress(self):
        """测试 TODO -> IN_PROGRESS 转换"""
        task = TaskWithStatus(title="作业", priority="high")
        assert task.status == TaskStatus.TODO

        task.mark_in_progress()
        assert task.status == TaskStatus.IN_PROGRESS

    def test_in_progress_to_done(self):
        """测试 IN_PROGRESS -> DONE 转换"""
        task = TaskWithStatus(title="作业", priority="high")
        task.mark_in_progress()
        assert task.status == TaskStatus.IN_PROGRESS

        task.mark_done()
        assert task.status == TaskStatus.DONE

    def test_todo_to_done_directly(self):
        """测试 TODO -> DONE 直接转换"""
        task = TaskWithStatus(title="作业", priority="high")

        # TaskWithStatus 的 mark_done 可以从任何状态调用
        task.mark_done()
        assert task.status == TaskStatus.DONE

    def test_cannot_restart_done_task(self):
        """测试已完成的任务不能重新开始"""
        task = TaskWithStatus(title="作业", priority="high")
        task.mark_in_progress()
        task.mark_done()

        with pytest.raises(ValueError, match="已完成的任务不能重新开始"):
            task.mark_in_progress()


class TestStateValidation:
    """测试状态验证函数"""

    def test_validate_todo_to_in_progress(self):
        """测试 TODO -> IN_PROGRESS 是合法的"""
        assert validate_state_transition(TaskStatus.TODO, TaskStatus.IN_PROGRESS) is True

    def test_validate_in_progress_to_done(self):
        """测试 IN_PROGRESS -> DONE 是合法的"""
        assert validate_state_transition(TaskStatus.IN_PROGRESS, TaskStatus.DONE) is True

    def test_validate_todo_to_done(self):
        """测试 TODO -> DONE 是合法的"""
        assert validate_state_transition(TaskStatus.TODO, TaskStatus.DONE) is True

    def test_validate_done_to_todo_is_invalid(self):
        """测试 DONE -> TODO 是非法的"""
        assert validate_state_transition(TaskStatus.DONE, TaskStatus.TODO) is False

    def test_validate_done_to_in_progress_is_invalid(self):
        """测试 DONE -> IN_PROGRESS 是非法的"""
        assert validate_state_transition(TaskStatus.DONE, TaskStatus.IN_PROGRESS) is False

    def test_validate_same_state(self):
        """测试保持相同状态应该是合法的"""
        # validate_state_transition 当前实现允许相同状态
        assert validate_state_transition(TaskStatus.TODO, TaskStatus.TODO) is True


class TestStateQueryMethods:
    """测试状态查询方法"""

    def test_can_restart_when_todo(self):
        """测试 TODO 状态下可以重新开始"""
        task = TaskWithStatus(title="作业", priority="high")
        assert task.can_restart() is True

    def test_can_restart_when_in_progress(self):
        """测试 IN_PROGRESS 状态下可以重新开始"""
        task = TaskWithStatus(title="作业", priority="high")
        task.mark_in_progress()
        assert task.can_restart() is True

    def test_cannot_restart_when_done(self):
        """测试 DONE 状态下不能重新开始"""
        task = TaskWithStatus(title="作业", priority="high")
        task.mark_done()
        assert task.can_restart() is False


class TestStateEnum:
    """测试状态枚举"""

    def test_enum_values(self):
        """测试枚举值"""
        assert TaskStatus.TODO.value == "待办"
        assert TaskStatus.IN_PROGRESS.value == "进行中"
        assert TaskStatus.DONE.value == "已完成"

    def test_enum_comparison(self):
        """测试枚举比较"""
        status1 = TaskStatus.TODO
        status2 = TaskStatus.TODO
        status3 = TaskStatus.DONE

        assert status1 == status2
        assert status1 != status3

    def test_enum_identity(self):
        """测试枚举同一性"""
        # 相同枚举值应该是同一个对象
        status1 = TaskStatus.TODO
        status2 = TaskStatus.TODO
        assert status1 is status2


class TestStateTransitionEdgeCases:
    """测试状态转换边界情况"""

    def test_multiple_transitions_forward(self):
        """测试多次前向转换"""
        task = TaskWithStatus(title="作业", priority="high")

        # TODO -> IN_PROGRESS -> DONE
        task.mark_in_progress()
        assert task.status == TaskStatus.IN_PROGRESS

        task.mark_done()
        assert task.status == TaskStatus.DONE

    def test_rapid_state_changes(self):
        """测试快速状态变化"""
        task = TaskWithStatus(title="作业", priority="high")

        # 多次调用 mark_done 应该保持 DONE 状态
        task.mark_done()
        task.mark_done()
        task.mark_done()
        assert task.status == TaskStatus.DONE

    def test_state_with_default_overridden(self):
        """测试创建时覆盖默认状态"""
        task = TaskWithStatus(
            title="作业",
            priority="high",
            status=TaskStatus.IN_PROGRESS
        )
        assert task.status == TaskStatus.IN_PROGRESS

    def test_all_possible_states(self):
        """测试所有可能的状态"""
        tasks = [
            TaskWithStatus(title="T1", priority="high", status=TaskStatus.TODO),
            TaskWithStatus(title="T2", priority="high", status=TaskStatus.IN_PROGRESS),
            TaskWithStatus(title="T3", priority="high", status=TaskStatus.DONE),
        ]

        assert tasks[0].status == TaskStatus.TODO
        assert tasks[1].status == TaskStatus.IN_PROGRESS
        assert tasks[2].status == TaskStatus.DONE


class TestStateWithDescription:
    """测试带描述的状态转换"""

    def test_state_with_description_field(self):
        """测试状态和描述字段的配合"""
        task = TaskWithStatus(
            title="作业",
            priority="high",
            description="初始描述"
        )

        assert task.description == "初始描述"
        assert task.status == TaskStatus.TODO

        task.mark_in_progress()
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.description == "初始描述"  # 描述不应该改变
