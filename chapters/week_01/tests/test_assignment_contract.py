"""Week 01 assignment contract: the submitted card generator runs end-to-end."""

import subprocess
import sys
from pathlib import Path


def test_business_card_generator_runs_with_user_input():
    script = Path(__file__).resolve().parents[1] / "starter_code" / "solution.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        input="小北\n20\n学生\n",
        text=True,
        capture_output=True,
        timeout=5,
    )

    assert result.returncode == 0, result.stderr
    assert "个人名片" in result.stdout
    assert "姓名：小北" in result.stdout
    assert "年龄：20 岁" in result.stdout
    assert "职业：学生" in result.stdout
    assert "名片生成成功" in result.stdout
