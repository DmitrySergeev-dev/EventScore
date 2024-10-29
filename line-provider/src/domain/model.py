from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .events import Event


class NewsStatus(str, Enum):
    SCORED_GOOD: str = "оценено высокой оценкой, ( >= 3 )"
    SCORED_BAD: str = "оценено низкой оценкой ( < 3 )"
    NOT_SCORED: str = "в обработке"


@dataclass
class NewsData:
    description: str
    deadline: str
    status: str


class News:
    DATETIME_PATTERN = "%Y-%m-%d %H:%M:%S"

    def __init__(self,
                 description: str,
                 deadline: datetime):
        self.description = description
        self.deadline = deadline
        self.status = NewsStatus.NOT_SCORED
        self.events: list[Event] = []

    def to_dict(self):
        return dict(
            description=self.description,
            deadline=self.deadline_as_str,
            status=self.status
        )

    @property
    def deadline_as_str(self):
        return self.deadline.strftime(self.DATETIME_PATTERN)
