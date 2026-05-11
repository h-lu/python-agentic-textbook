"""Week 02 PyHelper: mood-based study advice."""

import sys


def advice_for_mood(mood: str) -> str:
    mood = mood.strip().lower()
    if mood in {"累", "tired", "困", "exhausted"}:
        return "先休息 10 分钟，再完成一个 15 分钟的小任务。"
    if mood in {"焦虑", "anxious", "stressed"}:
        return "把任务写成三步：先做最小一步，不要一口吞完整项目。"
    if mood in {"开心", "good", "happy"}:
        return "状态不错！挑战一个稍难的小练习，并记录学到的东西。"
    return "今天也可以从一个很小的练习开始。"


def main() -> None:
    mood = sys.argv[1] if len(sys.argv) > 1 else "tired"
    print("欢迎使用 PyHelper！")
    print(f"你的状态：{mood}")
    print("学习建议：" + advice_for_mood(mood))


if __name__ == "__main__":
    main()
