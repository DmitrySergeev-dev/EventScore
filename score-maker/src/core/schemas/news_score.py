from typing import Literal

from pydantic import BaseModel, Field, conint


class NewsScoreIn(BaseModel):
    news_id: str
    score: conint(ge=1, le=5) | None = None


class NewsScoreOut(BaseModel):
    news_id: str
    score: conint(ge=1, le=5) | None
    editable: bool


class NewsScorePatch(BaseModel):
    score: conint(ge=1, le=5)


class ScoresFilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100, title="sasas")
    offset: int = Field(0, ge=0)
    order_by: Literal["news_id", "score"] = "news_id"
