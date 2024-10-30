from dataclasses import dataclass
from typing import Optional


class Command:
    pass


@dataclass
class CreateNews(Command):
    news_id: str
    deadline: str
    description: str
    status: str


@dataclass
class DeleteNews(Command):
    news_id: str


@dataclass
class UpdateNews(Command):
    news_id: str
    deadline: Optional[str]
    description: Optional[str]
    status: Optional[str]
