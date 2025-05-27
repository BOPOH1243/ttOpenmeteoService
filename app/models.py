from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    sessid = Column(String, index=True)
    city_name = Column(String(128))
    timestamp = Column(DateTime, default=datetime.utcnow)
