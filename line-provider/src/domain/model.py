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
        self._status = NewsStatus.NOT_SCORED
        self.events: list[Event] = []  # todo для SAGA

    def to_dict(self):
        return dict(
            description=self.description,
            deadline=self.deadline_as_str,
            status=self.status
        )

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        expected_values = (s.value for s in NewsStatus)
        if value not in expected_values:
            raise ValueError
        self._status = value

    @property
    def deadline_as_str(self):
        return self.deadline.strftime(self.DATETIME_PATTERN)

    @staticmethod
    def define_status_by_score(score_value: int) -> str:
        if score_value >= 3:
            return NewsStatus.SCORED_GOOD
        return NewsStatus.SCORED_BAD
