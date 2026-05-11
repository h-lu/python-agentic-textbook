from dataclasses import dataclass


@dataclass
class StudyPlan:
    goal: str
    topics: list[str]
    estimated_hours: float


class PlannerAgent:
    def generate(self, goal: str, notes: list[str]) -> StudyPlan:
        topics = [note.split()[0] for note in notes if note.strip()]
        return StudyPlan(goal=goal, topics=topics or [goal], estimated_hours=max(1.0, len(topics) * 0.5))


class ReviewerAgent:
    def review(self, plan: StudyPlan) -> list[str]:
        issues = []
        if not plan.topics:
            issues.append("缺少学习主题")
        if plan.estimated_hours <= 0:
            issues.append("预计时间必须大于 0")
        if len(plan.goal) < 4:
            issues.append("目标太短，需要更具体")
        return issues
