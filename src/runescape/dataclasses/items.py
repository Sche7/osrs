from pydantic import BaseModel, HttpUrl


class TradeHistory(BaseModel):
    trend: str
    price: str | int


class TradeTrend(BaseModel):
    trend: str
    change: str


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


class Details(BaseModel):
    icon: HttpUrl
    icon_large: HttpUrl
    typeIcon: HttpUrl
    type: str
    name: str
    description: str
    members: bool
    current: TradeHistory
    today: TradeHistory
    day30: TradeTrend
    day90: TradeTrend
    day180: TradeTrend


class ItemDetails(BaseModel):
    item: Details
