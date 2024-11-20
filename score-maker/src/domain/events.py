from dataclasses import dataclass


class Event:
    pass


@dataclass
class NewsCreated(Event):
    pk: str
    deadline: str
    description: str
    status: str


@dataclass
class NewsDeleted(Event):
    pk: str
