"""
测试 Week 04 作业函数

测试文件结构：
- 基础作业测试（40 分）
- 进阶作业测试（30 分）
- 挑战作业测试（30 分）

运行方式：
    python3 -m pytest chapters/week_04/tests/test_assignment.py -q
    python3 -m pytest chapters/week_04/tests/test_assignment.py::test_add_score -v
"""

import pytest
import sys
import os

# 添加 starter_code 到路径，以便导入函数。
# 多周测试会重复使用模块名 solution；导入前清理缓存，避免拿到其他周的 solution.py。
sys.modules.pop("solution", None)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter_code'))
from solution import (
    # 基础作业
    add_score,
    remove_failing_scores,
    get_top_scores,
    get_student_score,
    count_pass_fail,
    find_top_student,
    generate_report,
    # 进阶作业
    analyze_scores,
    group_by_grade,
    # 挑战作业
    add_class,
    get_class_average,
    compare_classes,
    find_top_class,
)


# ========================================
# 基础作业测试（40 分）
# ========================================

# ----------------------------------------------------------------------------
# 1. 成绩列表操作 (15 分)
# ----------------------------------------------------------------------------

def test_add_score():
    """测试：添加成绩到列表末尾"""
    scores = [85, 92]
    result = add_score(scores, 78)
    assert result == [85, 92, 78]
    # 确认是原地修改
    assert scores == [85, 92, 78]


def test_add_score_multiple():
    """测试：连续添加多个成绩"""
    scores = [85]
    add_score(scores, 92)
    add_score(scores, 78)
    assert scores == [85, 92, 78]


def test_remove_failing_scores():
    """测试：删除不及格成绩"""
    scores = [85, 45, 92, 58, 78]
    result = remove_failing_scores(scores)
    assert result == [85, 92, 78]
    # 原列表可能被修改（取决于实现）


def test_remove_failing_all_pass():
    """测试：所有成绩都及格"""
    scores = [85, 92, 78, 90]
    result = remove_failing_scores(scores)
    assert result == [85, 92, 78, 90]


def test_remove_failing_all_fail():
    """测试：所有成绩都不及格"""
    scores = [45, 58, 30]
    result = remove_failing_scores(scores)
    assert result == []


def test_remove_failing_empty():
    """测试：空列表"""
    result = remove_failing_scores([])
    assert result == []


def test_get_top_scores_basic():
    """测试：获取前 3 个最高分"""
    scores = [85, 92, 78, 90, 88]
    result = get_top_scores(scores, 3)
    assert result == [92, 90, 88]


def test_get_top_scores_custom_n():
    """测试：自定义 n 值"""
    scores = [85, 92, 78, 90, 88]
    result = get_top_scores(scores, 2)
    assert result == [92, 90]


def test_get_top_scores_n_larger_than_list():
    """测试：n 大于列表长度"""
    scores = [85, 92, 78]
    result = get_top_scores(scores, 10)
    assert result == [92, 85, 78]  # 返回所有成绩降序


def test_get_top_scores_empty():
    """测试：空列表"""
    result = get_top_scores([], 3)
    assert result == []


def test_get_top_scores_single_element():
    """测试：单元素列表"""
    result = get_top_scores([85], 3)
    assert result == [85]


# ----------------------------------------------------------------------------
# 2. 字典查询与统计 (15 分)
# ----------------------------------------------------------------------------

def test_get_student_score_exists():
    """测试：学生存在"""
    scores = {"小北": 85, "阿码": 92}
    result = get_student_score(scores, "小北")
    assert result == 85


def test_get_student_score_not_exists():
    """测试：学生不存在"""
    scores = {"小北": 85, "阿码": 92}
    result = get_student_score(scores, "小红")
    assert result is None


def test_get_student_score_empty_dict():
    """测试：空字典"""
    result = get_student_score({}, "小北")
    assert result is None


def test_count_pass_fail_basic():
    """测试：统计及格/不及格"""
    scores = {"小北": 85, "阿码": 92, "老潘": 45}
    result = count_pass_fail(scores, 60)
    assert result == {"pass": 2, "fail": 1}


def test_count_pass_fail_custom_passing_score():
    """测试：自定义及格线"""
    scores = {"小北": 85, "阿码": 92, "老潘": 78}
    result = count_pass_fail(scores, 80)
    assert result == {"pass": 2, "fail": 1}


def test_count_pass_fail_all_pass():
    """测试：所有人都及格"""
    scores = {"小北": 85, "阿码": 92, "老潘": 78}
    result = count_pass_fail(scores, 60)
    assert result == {"pass": 3, "fail": 0}


def test_count_pass_fail_all_fail():
    """测试：所有人都不及格"""
    scores = {"小北": 45, "阿码": 58, "老潘": 30}
    result = count_pass_fail(scores, 60)
    assert result == {"pass": 0, "fail": 3}


def test_count_pass_fail_empty():
    """测试：空字典"""
    result = count_pass_fail({}, 60)
    assert result == {"pass": 0, "fail": 0}


def test_find_top_student_basic():
    """测试：找出最高分学生"""
    scores = {"小北": 85, "阿码": 92, "老潘": 78}
    result = find_top_student(scores)
    assert result == "阿码"


def test_find_top_student_tie():
    """测试：多人并列第一（返回任意一个）"""
    scores = {"小北": 92, "阿码": 92, "老潘": 78}
    result = find_top_student(scores)
    assert result in ["小北", "阿码"]


def test_find_top_student_empty():
    """测试：空字典"""
    result = find_top_student({})
    assert result is None


def test_find_top_student_single():
    """测试：单元素字典"""
    scores = {"小北": 85}
    result = find_top_student(scores)
    assert result == "小北"


# ----------------------------------------------------------------------------
# 3. 成绩单生成 (10 分)
# ----------------------------------------------------------------------------

def test_generate_report_basic():
    """测试：生成基本成绩单"""
    scores = {"小北": 85, "阿码": 92, "老潘": 78}
    result = generate_report(scores)

    assert "=== 成绩单 ===" in result
    assert "小北: 85 (良好)" in result
    assert "阿码: 92 (优秀)" in result
    assert "老潘: 78 (及格)" in result


def test_generate_report_with_failing():
    """测试：包含不及格成绩"""
    scores = {"小北": 85, "小红": 58}
    result = generate_report(scores)

    assert "小北: 85 (良好)" in result
    assert "小红: 58 (不及格)" in result


def test_generate_report_grade_boundaries():
    """测试：等级边界值"""
    scores = {
        "优秀95": 95,
        "优秀90": 90,
        "良好89": 89,
        "良好80": 80,
        "及格79": 79,
        "及格60": 60,
        "不及格59": 59
    }
    result = generate_report(scores)

    assert "(优秀)" in result
    assert "(良好)" in result
    assert "(及格)" in result
    assert "(不及格)" in result


def test_generate_report_empty():
    """测试：空字典"""
    result = generate_report({})
    assert "=== 成绩单 ===" in result


# ========================================
# 进阶作业测试（30 分）
# ========================================

# ----------------------------------------------------------------------------
# 4. 成绩分析器 (30 分)
# ----------------------------------------------------------------------------

def test_analyze_scores_basic():
    """测试：基本统计分析"""
    scores = [85, 92, 78, 45, 88]
    result = analyze_scores(scores)

    assert result["count"] == 5
    assert abs(result["average"] - 77.6) < 0.1
    assert result["max"] == 92
    assert result["min"] == 45
    assert result["pass_rate"] == 0.8  # 4/5 = 0.8


def test_analyze_scores_empty():
    """测试：空列表"""
    result = analyze_scores([])

    assert result["count"] == 0
    # 其他统计值应该是 0 或 None（取决于实现）
    assert result["average"] == 0 or result["average"] is None
    assert result["max"] == 0 or result["max"] is None
    assert result["min"] == 0 or result["min"] is None


def test_analyze_scores_single():
    """测试：单元素列表"""
    result = analyze_scores([85])

    assert result["count"] == 1
    assert result["average"] == 85.0
    assert result["max"] == 85
    assert result["min"] == 85
    assert result["pass_rate"] == 1.0


def test_analyze_scores_all_failing():
    """测试：所有人都不及格"""
    result = analyze_scores([45, 58, 30])

    assert result["count"] == 3
    assert result["pass_rate"] == 0.0


def test_analyze_scores_rounding():
    """测试：平均分保留1位小数"""
    result = analyze_scores([85, 86])

    # 平均分应该是 85.5，不是 85 或 86
    assert abs(result["average"] - 85.5) < 0.1


def test_group_by_grade_basic():
    """测试：按等级分组"""
    scores = {"小北": 85, "阿码": 92, "老潘": 78, "小红": 58}
    result = group_by_grade(scores)

    assert result["优秀"] == ["阿码"]
    assert result["良好"] == ["小北"]
    assert result["及格"] == ["老潘"]
    assert result["不及格"] == ["小红"]


def test_group_by_grade_multiple_per_level():
    """测试：每个等级多个人"""
    scores = {
        "学生1": 95,
        "学生2": 91,
        "学生3": 85,
        "学生4": 82,
        "学生5": 65,
        "学生6": 55
    }
    result = group_by_grade(scores)

    assert len(result["优秀"]) == 2
    assert len(result["良好"]) == 2
    assert len(result["及格"]) == 1
    assert len(result["不及格"]) == 1


def test_group_by_grade_empty():
    """测试：空字典"""
    result = group_by_grade({})

    assert result["优秀"] == []
    assert result["良好"] == []
    assert result["及格"] == []
    assert result["不及格"] == []


def test_group_by_grade_all_same_level():
    """测试：所有人同等级"""
    scores = {"小北": 95, "阿码": 92, "老潘": 98}
    result = group_by_grade(scores)

    assert len(result["优秀"]) == 3
    assert result["良好"] == []
    assert result["及格"] == []
    assert result["不及格"] == []


# ========================================
# 挑战作业测试（30 分）
# ========================================

# ----------------------------------------------------------------------------
# 5. 多班级成绩管理系统 (30 分)
# ----------------------------------------------------------------------------

def test_add_class_basic():
    """测试：添加班级"""
    school = {}
    add_class(school, "一班", {"小北": 85, "阿码": 92})

    assert "一班" in school
    assert school["一班"]["小北"] == 85
    assert school["一班"]["阿码"] == 92


def test_add_class_multiple():
    """测试：添加多个班级"""
    school = {}
    add_class(school, "一班", {"小北": 85})
    add_class(school, "二班", {"老潘": 78})

    assert len(school) == 2
    assert school["一班"]["小北"] == 85
    assert school["二班"]["老潘"] == 78


def test_add_class_override():
    """测试：覆盖已存在的班级"""
    school = {"一班": {"小北": 85}}
    add_class(school, "一班", {"阿码": 92})

    # 班级被覆盖
    assert school["一班"]["阿码"] == 92
    assert "小北" not in school["一班"]


def test_get_class_average_basic():
    """测试：获取班级平均分"""
    school = {"一班": {"小北": 85, "阿码": 92}, "二班": {"老潘": 78}}
    result = get_class_average(school, "一班")

    assert abs(result - 88.5) < 0.1  # (85 + 92) / 2 = 88.5


def test_get_class_average_not_exists():
    """测试：班级不存在"""
    school = {"一班": {"小北": 85}}
    result = get_class_average(school, "二班")

    assert result is None


def test_get_class_average_empty_school():
    """测试：空学校"""
    result = get_class_average({}, "一班")
    assert result is None


def test_compare_classes_first_higher():
    """测试：第一个班级更高"""
    school = {"一班": {"小北": 85}, "二班": {"老潘": 78}}
    result = compare_classes(school, "一班", "二班")

    assert "一班 比 二班 高 7.0 分" == result


def test_compare_classes_second_higher():
    """测试：第二个班级更高"""
    school = {"一班": {"小北": 78}, "二班": {"老潘": 85}}
    result = compare_classes(school, "一班", "二班")

    assert "二班 比 一班 高 7.0 分" == result


def test_compare_classes_equal():
    """测试：两个班级平均分相同"""
    school = {"一班": {"小北": 85}, "二班": {"老潘": 85}}
    result = compare_classes(school, "一班", "二班")

    assert "一班 和 二班 平均分相同" == result


def test_compare_classes_not_exists():
    """测试：班级不存在"""
    school = {"一班": {"小北": 85}}
    result = compare_classes(school, "一班", "二班")

    assert "二班 班级不存在" in result or "二班" in result


def test_find_top_class_basic():
    """测试：找出最高班级"""
    school = {
        "一班": {"小北": 85, "阿码": 70},  # 平均 77.5
        "二班": {"老潘": 78}                 # 平均 78
    }
    result = find_top_class(school)

    assert result == "二班"


def test_find_top_class_empty():
    """测试：空学校"""
    result = find_top_class({})
    assert result is None


def test_find_top_class_single():
    """测试：单班级"""
    school = {"一班": {"小北": 85}}
    result = find_top_class(school)
    assert result == "一班"


def test_find_top_class_tie():
    """测试：多个班级并列第一（返回任意一个）"""
    school = {
        "一班": {"小北": 85},
        "二班": {"老潘": 85},
        "三班": {"阿码": 70}
    }
    result = find_top_class(school)

    assert result in ["一班", "二班"]


# ========================================
# 集成测试
# ========================================

def test_complete_workflow():
    """测试：完整的工作流"""
    # 1. 创建学校
    school = {}

    # 2. 添加班级
    add_class(school, "一班", {"小北": 85, "阿码": 92, "老潘": 78})
    add_class(school, "二班", {"小红": 90, "小明": 88, "小李": 95})

    # 3. 验证班级添加
    assert len(school) == 2

    # 4. 获取平均分
    avg1 = get_class_average(school, "一班")
    avg2 = get_class_average(school, "二班")
    assert abs(avg1 - 85.0) < 0.1  # (85+92+78)/3
    assert abs(avg2 - 91.0) < 0.1  # (90+88+95)/3

    # 5. 比较班级
    comparison = compare_classes(school, "一班", "二班")
    assert "二班" in comparison and "高" in comparison

    # 6. 找出最高班级
    top = find_top_class(school)
    assert top == "二班"

    # 7. 生成二班成绩单
    report = generate_report(school["二班"])
    assert "=== 成绩单 ===" in report
    assert "小红" in report
