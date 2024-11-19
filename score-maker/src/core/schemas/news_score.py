from pydantic import BaseModel


class NewsScoreIn(BaseModel):
    news_id: str
    score: int | None = None


class NewsScoreOut(BaseModel):
    news_id: str
    score: int
    editable: bool


