from pydantic import BaseModel, HttpUrl


class TradeHistory(BaseModel):
    trend: str
    price: str | int


class Item(BaseModel):
    icon: HttpUrl
    icon_large: HttpUrl
    id: int
    type: str
    typeIcon: HttpUrl
    name: str
    description: str
    current: TradeHistory
    today: TradeHistory
    members: bool


class Items(BaseModel):
    total: int
    items: list[Item]
