from datetime import datetime
from enum import Enum

from .events import Event


class NewsStatus(str, Enum):
    SCORED_GOOD: str = "оценено высокой оценкой, ( >= 3 )"
    SCORED_BAD: str = "оценено низкой оценкой ( < 3 )"
    NOT_SCORED: str = "в обработке"


class News:
    def __init__(self,
                 description: str,
                 deadline: datetime,
                 status: NewsStatus = NewsStatus.NOT_SCORED):
        self.description = description
        self.deadline = deadline
        self.status = status
        self.events: list[Event] = []
