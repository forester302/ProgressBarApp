import inspect
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date, datetime
from sqlalchemy.orm import Session

from database import Item, Source, Status, StatusGroup

"""
Get Source Items
Get Status Items
Get Status Group Items
Get Item

Get Statuses for Source
Get Status Groups for Source
"""
def items(app: FastAPI, session: Session):
    class ItemResponse(BaseModel):
        id: int
        source_id: int
        status_id: int
        date_submited: date
        last_updated: datetime
        data: str
    def make_item_response(data: Item) -> ItemResponse:
        return ItemResponse(
            id=data.id,
            source_id=data.source_id,
            status_id=data.status_id,
            date_submited=data.date_submitted,
            last_updated=data.last_updated,
            data=data.data
        )
    class SimpleRequest(BaseModel):
        id: int
    @app.post("/source-items")
    async def get_items_from_source(request: SimpleRequest) -> list[ItemResponse]:
        data = session.query(Source).filter(Source.id == request.id).first()
        if data is None: return []
        l = []
        for item in data.items:
            l.append(make_item_response(item))
    @app.post("/status-items")
    async def get_items_from_status(request: SimpleRequest) -> list[ItemResponse]:
        data = session.query(Status).filter(Status.id == request.id).first()
        if data is None: return []
        l = []
        for item in data.items:
            l.append(make_item_response(item))
    @app.post("/status-group-items")
    async def get_items_from_status_group(request: SimpleRequest) -> list[ItemResponse]:
        data = session.query(StatusGroup).filter(StatusGroup.id == request.id).first()
        if data is None: return []
        l = []
        for status in data.statuses:
            for item in status.items:
                l.append(make_item_response(item))
    @app.post("/item")
    async def get_item(request: SimpleRequest) -> ItemResponse:
        data = session.query(Item).filter(Item.id == request.id).first()
        if data is None: return ItemResponse(id=0, source_id=0, status_id=0, date_submited=0, last_updated=0, data = "")
        return make_item_response(data)
def statuses(app: FastAPI, session: Session):
    class StatusRequest(BaseModel):
        source_id: int
    class StatusResponse(BaseModel):
        id: int
        status_group_id: int
        name: str
    class StatusGroupResponse(BaseModel):
        id: int
        source_id: int
        name: str
        type: str
    @app.post("/statuses")
    async def get_statuses(request: StatusRequest) -> list[StatusResponse]:
        data = session.query(Status)
        if data.first() is None:
            return []
        else:
            l = []
            for status in data.all():
                l.append(StatusResponse(id=status.id, status_group_id=status.status_group_id, name=status.name))
            return l
    @app.post("/status-groups")
    async def get_status_groups(request: StatusRequest) -> list[StatusGroupResponse]:
        data = session.query(StatusGroup)
        if data.first() is None:
            return []
        else:
            l = []
            for group in data.all():
                l.append(StatusGroupResponse(id=group.id, source_id=group.source_id, name=group.name, type=group.type))
            return l

def register(app: FastAPI, session: Session):
    for name, obj in globals().items():
        if inspect.isfunction(obj) and obj.__module__ == __name__ and name not in {"register"}:
            obj(app, session)