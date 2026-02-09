#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：review checklist - 检测边界情况处理

本示例演示：
1. 检查代码是否处理了边界情况
2. 检查项：文件存在性、空输入、异常处理
3. 对比"坏代码"和"好代码"的审查结果

运行方式：
    python3 chapters/week_13/examples/02_checklist_edge_cases.py

预期输出：
    审查 bad 代码:
      通过:False, 问题:['未检查文件是否存在', '未检查空输入', '缺少异常处理']

    审查 good 代码:
      通过:True, 问题:[]
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
    """reviewer agent：检查边界情况处理"""

    def review_edge_cases(self, code: str) -> ReviewResult:
        """检查代码是否处理了边界情况"""
        issues = []

        # 检查 1：是否检查文件是否存在
        if "Path(" in code or "path" in code.lower():
            if "exists" not in code:
                issues.append("未检查文件是否存在(用 path.exists())")

        # 检查 2：是否检查空输入
        if "if not" not in code and "if len(" not in code:
            issues.append("未检查空输入(用 `if not content`)")

        # 检查 3：是否有 try/except
        if "try:" not in code:
            issues.append("缺少异常处理(try/except)")

        # 检查 4：是否处理除零（简化版检查）
        # 只在代码中有除法且没有检查分母时才提示
        has_division = "/" in code
        has_check = ("if len(" in code or "if not" in code or
                     "ZeroDivisionError" in code or "//" in code)
        if has_division and not has_check:
            # 但如果有 len(words) 这样的检查，认为已处理
            if "len(" not in code:
                issues.append("可能存在除零风险(未检查分母)")

        return ReviewResult(
            passed=len(issues) == 0,
            issues=issues
        )


# =====================
# 使用 reviewer agent
# =====================

if __name__ == "__main__":
    reviewer = ReviewerAgent()

    # AI 生成的代码（缺少边界检查）
    ai_code_bad = """
def summarize(file_path):
    content = open(file_path).read()
    words = content.split()
    return len(words) / len(words)
"""

    # 修复后的代码（有边界检查）
    ai_code_good = """
def summarize(file_path):
    # 检查文件是否存在
    if not Path(file_path).exists():
        raise FileNotFoundError(f"文件不存在:{file_path}")

    # 读取文件
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception as e:
        logger.error(f"读取失败:{e}")
        raise

    # 检查空文件
    if not content.strip():
        return 0

    # 计算平均词长
    words = content.split()
    if not words:
        return 0

    # 安全的除法（已检查 words 非空）
    return sum(len(w) for w in words) / len(words)
"""

    print("=" * 70)
    print("审查 bad 代码（缺少边界检查）:")
    print("=" * 70)
    result = reviewer.review_edge_cases(ai_code_bad)
    print(f"  通过:{result.passed}")
    print(f"  问题:{result.issues}")
    if result.issues:
        print("\n  问题说明:")
        for issue in result.issues:
            print(f"    ✗ {issue}")

    print("\n" + "=" * 70)
    print("审查 good 代码（有边界检查）:")
    print("=" * 70)
    result = reviewer.review_edge_cases(ai_code_good)
    print(f"  通过:{result.passed}")
    print(f"  问题:{result.issues if result.issues else '无'}")

    # 演示：手动检查边界情况的例子
    print("\n" + "=" * 70)
    print("边界情况示例:")
    print("=" * 70)

    test_cases = [
        ("空文件", ""),
        ("正常文件", "Hello world"),
        ("超大文件", "word " * 1000000),
    ]

    for name, content in test_cases[:2]:  # 只演示前两个
        print(f"\n  测试:{name}")
        print(f"    内容长度:{len(content)} 字符")
        print(f"    词数:{len(content.split()) if content else 0}")


# =====================
# 总结
# =====================

"""
本示例演示了如何检查边界情况处理：

核心概念：
  1. 边界情况（Edge Case）：
     - 空输入：空文件、空字符串、空列表
     - 文件不存在：路径错误、权限问题
     - 异常情况：除零、网络超时、格式错误

  2. 检查方法：
     - 文件存在性：Path.exists()
     - 空输入检查：if not content
     - 异常处理：try/except

  3. 常见边界情况：
     - 空文件/空字符串/空列表
     - 文件不存在/权限不足
     - 除零/负数/超大值
     - 网络超时/格式错误

AI 代码为什么容易忽略边界情况？
  - AI 训练数据里的代码也不是完美的
  - 大多数示例代码只演示"正常情况"
  - AI 不知道你的具体使用场景

与之前知识的联系：
  - Week 06 的异常处理：try/except FileNotFoundError
  - Week 05 的文件操作：Path.exists()
  - Week 02 的条件判断：if not content

实践建议：
  - 每次审查 AI 代码时，先问自己"什么情况下会崩溃？"
  - 用测试覆盖边界情况（就像 Week 08 学的 pytest）
  - 保留一份 checklist，逐项检查
"""
