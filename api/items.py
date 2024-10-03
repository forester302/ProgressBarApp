import inspect
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, datetime
from sqlalchemy.orm import Session

from database import Item
import database as db

from . import SimpleRequest

PREFIX = "item"

class SimpleItemResponse(BaseModel):
    id: int
    last_updated: datetime
class ItemResponse(SimpleItemResponse):
        source_id: int
        status_id: int
        name: str
        date_submitted: date
        data: str
def make_item_response(data: Item) -> ItemResponse:
    return ItemResponse(
        id=data.id,
        source_id=data.source_id,
        status_id=data.status_id,
        date_submitted=data.date_submitted,
        last_updated=data.last_updated,
        data=data.data,
        name=data.name
    )

def register(app: FastAPI, session: Session):
    @app.post(f"/{PREFIX}")
    async def get_item(request: SimpleRequest) -> ItemResponse:
        data = session.query(Item).filter(Item.id == request.id).first()
        if data is None: raise HTTPException(404, "Item not found")
        return make_item_response(data)
    
    class CreateItemRequest(BaseModel):
        source_id: int
        status_id: int
        name: str
        date_submitted: date
        data: str

    @app.post(f"/{PREFIX}/create")
    async def get_item(request: CreateItemRequest) -> SimpleItemResponse:
        item = Item()
        item.source_id = request.source_id
        item.name = request.name
        item.date_submitted = request.date_submitted
        item.status_id = request.status_id
        item.data = request.data
        session.add(item)
        db.try_commit(session, HTTPException(500, "Database Error"))
        return SimpleItemResponse(id=item.id, last_updated=item.last_updated)
    
    class UpdateItemRequest(BaseModel):
        id: int
        name: str
        status_id: int
        date_submitted: date
        data: str

    @app.post(f"/{PREFIX}/update")
    async def get_item(request: UpdateItemRequest):
        item = session.query(Item).filter(Item.id == request.id).first()
        if item is None: raise HTTPException(404, "Item not found")
        item.name = request.name
        item.date_submitted = request.date_submitted
        item.status_id = request.status_id
        item.data = request.data
        db.try_commit(session, HTTPException(500, "Database Error"))
        return SimpleItemResponse(id=item.id, last_updated=item.last_updated)
    
    class ItemUpdateDataRequest(BaseModel):
        id: int
        data: str

    @app.post(f"/{PREFIX}/update/data")
    async def update_data(request: ItemUpdateDataRequest):
        item = session.query(Item).filter(Item.id == request.id).first()
        if item is None: raise HTTPException(404, "Item not found")
        item.data = request.data
        db.try_commit(session, HTTPException(500, "Database Error"))
    
    @app.post(f"/{PREFIX}/delete")
    async def delete_item(request: SimpleRequest):
        item = session.query(Item).filter(Item.id == request.id).first()
        if item is None: return # If None data could have already been deleted
        session.delete(item)
        db.try_commit(session, HTTPException(500, "Database Error"))