from dataclasses import dataclass


class Event:
    pass


@dataclass
class Created(Event):
    news_id: str
    deadline: str
    description: str
    status: str


@dataclass
class Deleted(Event):
    news_id: str


@dataclass
class Updated(Event):
    news_id: str
