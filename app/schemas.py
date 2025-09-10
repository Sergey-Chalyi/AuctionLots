from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LotCreate(BaseModel):
    title: str
    description: Optional[str] = None
    starting_price: float
    duration_minutes: int = 60


class LotResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    starting_price: float
    current_price: float
    status: str
    created_at: datetime
    end_time: Optional[datetime]

    class Config:
        from_attributes = True


class BidCreate(BaseModel):
    bidder: str
    amount: float


class BidResponse(BaseModel):
    id: int
    lot_id: int
    bidder: str
    amount: float
    placed_at: datetime

    class Config:
        from_attributes = True


class WebSocketMessage(BaseModel):
    type: str
    lot_id: int
    bidder: str
    amount: float
