from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Status

from .items import ItemResponse, make_item_response
from . import SimpleRequest, SimpleResponse

PREFIX = "status"
def register(app: FastAPI, session: Session):
    @app.post(f"/{PREFIX}/items")
    async def get_items_from_status(request: SimpleRequest) -> list[ItemResponse]:
        data = session.query(Status).filter(Status.id == request.id).first()
        if data is None: return []
        l = []
        for item in data.items:
            l.append(make_item_response(item))
        return l

    class StatusResponse(BaseModel):
        id: int
        status_group_id: int
        name: str
        
    @app.post(f"/{PREFIX}/all")
    async def get_statuses() -> list[StatusResponse]:
        data = session.query(Status)
        if data.first() is None: return []
        l = []
        for status in data.all():
            l.append(StatusResponse(id=status.id, status_group_id=status.status_group_id, name=status.name))
        return l
    
    @app.post(f"{PREFIX}/create")
    async def create_status() -> SimpleResponse:
        pass

    @app.post(f"{PREFIX}/update")
    async def update_status():
        pass