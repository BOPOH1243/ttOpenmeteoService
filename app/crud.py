from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def create_request_log(db: Session, sessid: str, city_name: str):
    db_log = models.RequestLog(sessid=sessid, city_name=city_name)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_request_logs(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    sessid: Optional[str] = None,
    city_name: Optional[str] = None,
):
    query = db.query(models.RequestLog)
    if sessid:
        query = query.filter(models.RequestLog.sessid == sessid)
    if city_name:
        query = query.filter(models.RequestLog.city_name == city_name)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return total, items
