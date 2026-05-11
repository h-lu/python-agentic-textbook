from dataclasses import asdict, dataclass, field

@dataclass
class Note:
    date: str
    content: str
    tags: list[str] = field(default_factory=list)
    reviewed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        return cls(
            date=str(data.get("date", "")),
            content=str(data.get("content", "")),
            tags=list(data.get("tags", [])),
            reviewed=bool(data.get("reviewed", False)),
        )

@dataclass
class StudyPlan:
    title: str
    goals: list[str] = field(default_factory=list)
    source_dates: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
