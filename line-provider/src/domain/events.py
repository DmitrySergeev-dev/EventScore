from dataclasses import dataclass


class Event:
    pass


@dataclass
class NewsScored(Event):
    news_hash: str
    score_value: int
