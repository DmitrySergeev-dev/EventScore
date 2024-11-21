from dataclasses import dataclass


class Command:
    pass


@dataclass
class NotifyAboutScoredNews(Command):
    pk: str
    score_value: int

