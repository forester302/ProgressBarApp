import inspect
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, datetime
from sqlalchemy.orm import Session

from database import Item, Source

from . import SimpleRequest

PREFIX = "item"
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

def register(app: FastAPI, session: Session):
    @app.post(f"/{PREFIX}")
    async def get_item(request: SimpleRequest) -> ItemResponse:
        data = session.query(Item).filter(Item.id == request.id).first()
        if data is None: raise HTTPException(404, "Item not found")
        return make_item_response(data)