from typing import Any

from pydantic import BaseModel


class CategoryStatistic(BaseModel):
    letter: str
    items: int


class CategoryOverview(BaseModel):
    types: list[Any]
    alpha: list[CategoryStatistic]
