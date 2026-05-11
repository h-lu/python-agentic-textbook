from dataclasses import asdict, dataclass, field
from enum import Enum


class NoteStatus(Enum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    ARCHIVED = "archived"


@dataclass
class Note:
    date: str
    content: str
    tags: list[str] = field(default_factory=list)
    status: NoteStatus = NoteStatus.DRAFT

    def to_dict(self) -> dict:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass
class StudyPlan:
    goal: str
    topics: list[str]
    estimated_hours: float

    def summary(self) -> str:
        return f"{self.goal}: {len(self.topics)} 个主题，约 {self.estimated_hours} 小时"
