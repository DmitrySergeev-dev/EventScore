from dataclasses import dataclass


class Event:
    pass


@dataclass
class NewsScored(Event):
    pk: str
    score_value: int
