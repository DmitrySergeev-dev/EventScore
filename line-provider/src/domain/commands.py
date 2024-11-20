from dataclasses import dataclass


class Command:
    pass


@dataclass
class NotifyAboutCreatedNews(Command):
    pk: str
    deadline: str
    description: str
    status: str


@dataclass
class NotifyAboutDeletedNews(Command):
    pk: str
