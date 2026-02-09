#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：review checklist - 检查 AI 生成代码的基本质量

本示例演示：
1. reviewer agent：检查 AI 生成的代码质量
2. checklist：定义检查项（错误处理、日志、文档）
3. 可定制的检查项配置

运行方式：
    python3 chapters/week_13/examples/02_review_checklist.py

预期输出：
    [reviewer] 审查失败:['缺少错误处理(try/except)', '缺少日志记录(logging)', '函数缺少 docstring']
"""

from dataclasses import dataclass
from typing import List


# =====================
# 审查结果
# =====================

@dataclass
class ReviewResult:
    """审查结果"""
    passed: bool
    issues: List[str]


# =====================
# Reviewer Agent
# =====================

class ReviewerAgent:
    """reviewer agent：检查 AI 生成的代码质量"""

    def review_code(self, code: str, checklist: dict) -> ReviewResult:
        """根据 checklist 检查代码质量"""
        issues = []

        # 检查项 1：是否有 try/except
        if checklist["check_error_handling"]:
            if "try:" not in code and "except" not in code:
                issues.append("缺少错误处理(try/except)")

        # 检查项 2：是否有日志
        if checklist["check_logging"]:
            if "logging." not in code and "logger." not in code:
                issues.append("缺少日志记录(logging)")

        # 检查项 3：函数是否有 docstring
        if checklist["check_docstring"]:
            if '"""' not in code and "'''" not in code:
                issues.append("函数缺少 docstring")

        # 检查项 4：是否有类型提示
        if checklist.get("check_type_hints", False):
            if "->" not in code and ":" not in code:
                issues.append("缺少类型提示(type hints)")

        return ReviewResult(
            passed=len(issues) == 0,
            issues=issues
        )


# =====================
# 使用 reviewer agent
# =====================

if __name__ == "__main__":
    reviewer = ReviewerAgent()

    # AI 生成的代码（节选，缺少错误处理、日志、文档）
    ai_code_bad = """
def summarize(file_path):
    content = open(file_path).read()
    # ... 摘要逻辑
    return summary
"""

    # 修复后的代码（有错误处理、日志、文档）
    ai_code_good = """
def summarize(file_path: str) -> str:
    \"\"\"生成文件摘要\"\"\"
    logger.info(f"正在读取文件:{file_path}")

    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception as e:
        logger.error(f"读取失败:{e}")
        raise

    # ... 摘要逻辑
    return summary
"""

    # 定义 checklist（可以定制）
    checklist = {
        "check_error_handling": True,  # 检查错误处理
        "check_logging": True,          # 检查日志
        "check_docstring": True,        # 检查文档字符串
        "check_type_hints": False,      # 不检查类型提示（可选）
    }

    print("=" * 60)
    print("审查 bad 代码（缺少错误处理、日志、文档）:")
    print("=" * 60)
    result = reviewer.review_code(ai_code_bad, checklist)
    if result.passed:
        print("[reviewer] 审查通过")
    else:
        print(f"[reviewer] 审查失败:")
        for issue in result.issues:
            print(f"  ✗ {issue}")

    print("\n" + "=" * 60)
    print("审查 good 代码（有错误处理、日志、文档）:")
    print("=" * 60)
    result = reviewer.review_code(ai_code_good, checklist)
    if result.passed:
        print("[reviewer] 审查通过 ✓")
    else:
        print(f"[reviewer] 审查失败:")
        for issue in result.issues:
            print(f"  ✗ {issue}")


# =====================
# 总结
# =====================

"""
本示例演示了 review checklist 的基本概念：

核心概念：
  1. checklist：定义"什么算好代码"
     - 错误处理：有 try/except
     - 日志：有 logging
     - 文档：有 docstring

  2. 可定制：根据需要开关检查项
     - check_type_hints：可选检查

  3. 检查方法：简单的字符串匹配
     - 实际项目可以用 AST（抽象语法树）

AI 代码的常见问题：
  - 缺少错误处理：文件不存在、权限不足时崩溃
  - 忽略边界情况：空输入、负数、超大值
  - 过度工程化：用复杂的库解决简单问题
  - 命名不一致：变量名、函数名混乱
  - 缺少日志：出问题后无法追溯

与之前知识的联系：
  - Week 06 的异常处理：try/except
  - Week 12 的 logging：日志记录
  - Week 11 的类型提示：type hints

下一步：
  - 更复杂的 checklist：检测边界情况
  - 用 AST 做更精确的代码分析
"""
