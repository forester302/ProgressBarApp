from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Status, StatusGroup
import database as db

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
    
    @app.post(f"/{PREFIX}/filtered")
    async def get_statuses(request: list[SimpleRequest]) -> list[StatusResponse]:
        l = []
        for req in request:
            status = session.query(Status).filter(Status.id == req.id).first()
            if status is None: continue
            l.append(StatusResponse(id=status.id, status_group_id=status.status_group_id, name=status.name))
        return l
    
    class CreateStatusRequest(BaseModel):
        status_group_id: int
        name: str

    @app.post(f"/{PREFIX}/create")
    async def create_status(request: CreateStatusRequest) -> SimpleResponse:
        status = Status()
        status.status_group_id = request.status_group_id
        status.name = request.name
        session.add(status)
        db.try_commit(session, HTTPException(500, "Database Error"))
        return SimpleResponse(id=status.id)

    class UpdateStatusRequest(BaseModel):
        id: int
        name: str

    @app.post(f"/{PREFIX}/update")
    async def update_status(request: UpdateStatusRequest):
        status = session.query(Status).filter(Status.id == request.id).first()
        if status is None: raise HTTPException(404, "Group not found")
        status.name = request.name
        db.try_commit(session, HTTPException(500, "Database Error"))

    @app.post(f"/{PREFIX}/delete")
    async def delete_status(request: SimpleRequest):
        status = session.query(Status).filter(Status.id == request.id).first()
        if status is None: return
        session.delete(status)
        db.try_commit(session, HTTPException(500, "Database Error"))

    @app.post(f"/status-group/statuses")
    async def get_statuses_from_status_groups(request: list[SimpleRequest]) -> list[StatusResponse]:
        l = []
        for g in request:
            group = session.query(StatusGroup).filter(StatusGroup.id == g.id).first()
            if group is None: continue
            for status in group.statuses:
                l.append(StatusResponse(id=status.id, status_group_id=status.status_group_id, name = status.name))
        return l