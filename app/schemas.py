from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from enum import Enum

class TimeRangeOption(str, Enum):
    LAST_24H = "1d"
    LAST_7D = "7d"
    LAST_30D = "30d"

class SyncRequest(BaseModel):
    option: Optional[TimeRangeOption] = TimeRangeOption.LAST_24H
    days_start: Optional[int] = None # Custom: Start X days ago
    days_end: Optional[int] = None   # Custom: End Y days ago

class OrderBase(BaseModel):
    id: str
    ref_id: Optional[str] = None
    status: Optional[str] = None
    customer_info: Optional[Any] = None
    line_items: Optional[Any] = None
    full_data: Optional[Any] = None

class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    synced_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
