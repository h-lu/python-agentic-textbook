try:
    from .models import StudyPlan
except ImportError:
    from models import StudyPlan

class ReaderAgent:
    def summarize(self, records: list[dict]) -> dict:
        keywords = []
        for item in records:
            keywords.extend(item.get("tags", []))
        return {"count": len(records), "dates": [item["date"] for item in records], "keywords": sorted(set(keywords))}

class PlannerAgent:
    def create_plan(self, summary: dict) -> StudyPlan:
        goals = ["复盘最近 3 条学习记录", "把卡住的问题拆成 15 分钟小任务"]
        if summary.get("keywords"):
            goals.append("围绕标签 " + ", ".join(summary["keywords"][:3]) + " 做一次主题练习")
        return StudyPlan(title="PyHelper 自动学习计划", goals=goals, source_dates=summary.get("dates", []))

class ReviewerAgent:
    def review(self, plan: StudyPlan) -> str:
        if len(plan.goals) < 2:
            return "需要补充更具体的目标。"
        return "计划可执行：目标清晰，来源记录明确。"

def build_study_plan(records: list[dict]) -> StudyPlan:
    return PlannerAgent().create_plan(ReaderAgent().summarize(records))

def review_plan(plan: StudyPlan) -> str:
    return ReviewerAgent().review(plan)
