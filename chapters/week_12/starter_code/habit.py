#!/usr/bin/env python3
"""学生提交入口：habit-cli。

solution.py 保存完整参考实现；本文件让作业中的 `python habit.py ...`
和 `habit ...` 约定有一个真实入口。
"""

import sys

try:
    import solution as _solution
except ImportError:  # pragma: no cover - package import fallback
    from . import solution as _solution


if __name__ == "__main__":
    sys.exit(_solution.main())
else:
    sys.modules[__name__] = _solution
