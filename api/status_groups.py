import database as db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import StatusGroup

from . import SimpleRequest, SimpleResponse

from .items import ItemResponse, make_item_response

PREFIX = "status-group"

def register(app: FastAPI, session: Session):
    @app.post(f"/{PREFIX}/items")
    async def get_items_from_status_group(request: SimpleRequest) -> list[ItemResponse]:
        data = session.query(StatusGroup).filter(
            StatusGroup.id == request.id).first()
        if data is None:
            return []
        l = []
        for status in data.statuses:
            for item in status.items:
                l.append(make_item_response(item))
        return l

    class StatusGroupResponse(BaseModel):
        id: int
        source_id: int
        name: str
        type: str

    @app.post(f"/{PREFIX}/all")
    async def get_status_groups() -> list[StatusGroupResponse]:
        data = session.query(StatusGroup)
        if data.first() is None:
            return []
        else:
            l = []
            for group in data.all():
                l.append(StatusGroupResponse(
                    id=group.id, source_id=group.source_id, name=group.name, type=group.type))
            return l

    class CreateStatusGroupRequest(BaseModel):
        source_id: int
        name: str
        type: StatusGroup.StatusTypeEnum

    @app.post(f"/{PREFIX}/create", status_code=201)
    async def create_status_group(request: CreateStatusGroupRequest) -> SimpleResponse:
        group = StatusGroup()
        group.source_id = request.source_id
        group.name = request.name
        group.type = request.type
        session.add(group)
        db.try_commit(session, HTTPException(500, "Database Error"))
        return SimpleResponse(id=group.id)
    
    class UpdateStatusGroupRequest(BaseModel):
        id: int
        source_id: int
        name: str
        type: StatusGroup.StatusTypeEnum

    @app.post(f"/{PREFIX}/update")
    async def create_status_group(request: UpdateStatusGroupRequest) -> SimpleResponse:
        group = session.query(StatusGroup).filter(StatusGroup.id == request.id).first()
        if group is None: raise HTTPException(404, "Group not found")
        group.source_id = request.source_id
        group.name = request.name
        group.type = request.type
        db.try_commit(session, HTTPException(500, "Database Error"))

    @app.post(f"/{PREFIX}")
    async def get_status_group(request: SimpleRequest) -> StatusGroupResponse:
        group = session.query(StatusGroup).filter(StatusGroup.id == request.id).first()
        if group is None: raise HTTPException(404, "Group not found")
        return StatusGroupResponse(id=group.id, source_id=group.source_id, name = group.name, type=group.type)