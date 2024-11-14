from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from src.domain.model import NewsStatus


class NewsSchema(BaseModel):
    description: str
    deadline: datetime


class NewsSchemaEdit(NewsSchema):
    status: NewsStatus | None = None


class NewsSchemaOut(NewsSchema):
    pk: str
    status: NewsStatus


class NewsFilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100, title="sasas")
    offset: int = Field(0, ge=0)
    order_by: Literal["deadline", "status", "description"] = "deadline"
