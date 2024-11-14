from typing import NamedTuple

from src.domain import model


class NewsObject(NamedTuple):
    pk: str
    data: model.NewsData
