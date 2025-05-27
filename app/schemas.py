from pydantic import BaseModel
from datetime import datetime
from typing import List

class NotifyRequest(BaseModel):
    city_name: str

class RequestLogSchema(BaseModel):
    id: int
    sessid: str
    city_name: str
    timestamp: datetime

    class Config:
        orm_mode = True

class PaginatedResponse(BaseModel):
    total: int
    items: List[RequestLogSchema]
