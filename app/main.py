from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas, crud, dependencies
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/notify_backend", response_model=schemas.RequestLogSchema)
def notify_backend(
    request_data: schemas.NotifyRequest,
    request: Request,
    response: Response,
    db: Session = Depends(dependencies.get_db),
    sessid: str = Depends(dependencies.get_or_create_session_id),
):
    return crud.create_request_log(db, sessid, request_data.city_name)

@app.get("/analytics", response_model=schemas.PaginatedResponse)
def analytics(
    request: Request,
    response: Response,
    db: Session = Depends(dependencies.get_db),
    sessid: Optional[str] = None,
    city_name: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
):
    total, items = crud.get_request_logs(db, skip, limit, sessid, city_name)
    return {"total": total, "items": items}
