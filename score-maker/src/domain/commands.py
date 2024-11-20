from dataclasses import dataclass


class Command:
    pass


@dataclass
class NotifyAboutScoredNews(Command):
    news_hash: str
    score_value: int


@dataclass
class NotifyAboutDeletedNews(Command):
    news_id: str
