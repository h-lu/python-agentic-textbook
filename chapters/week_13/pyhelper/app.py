"""Week 13 PyHelper: agent-assisted planning."""

try:
    from .agents import PlannerAgent, ReviewerAgent
except ImportError:
    from agents import PlannerAgent, ReviewerAgent


def main() -> None:
    notes = ["argparse 子命令", "pytest 测试", "json 存储"]
    plan = PlannerAgent().generate("发布 PyHelper v1", notes)
    issues = ReviewerAgent().review(plan)
    print(plan)
    print("审查问题：", issues or "无")


if __name__ == "__main__":
    main()
