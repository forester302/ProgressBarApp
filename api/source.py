import inspect
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Source, SourceType
import database as db
from sqlalchemy.orm import Session

from . import SimpleRequest, SimpleResponse
from .items import ItemResponse, make_item_response

PREFIX = "source"
def register(app: FastAPI, session: Session):
    class SourceResponse(BaseModel):
        id: int
        name: str
        type: int

    @app.post(f"/{PREFIX}/all")
    async def get_sources() -> list[SourceResponse]:
        sources = session.query(Source)
        if (sources.first() is None): return []
        else:
            l = []
            for source in sources.all():
                l.append(SourceResponse(id=source.id, name=source.name, type=source.source_type_id))
            return l
        
    class SourceRequest(BaseModel):
        id: int

    @app.post(f"/{PREFIX}")
    async def get_source(request: SourceRequest) -> SourceResponse:
        source = session.query(Source).filter(Source.id == request.id).first()
        if source is None: raise HTTPException(404, "Source not found")
        return SourceResponse(id=source.id, name=source.name, type=source.source_type_id)
    
    
    class CreateSourceRequest(BaseModel):
        type_id: int
        name: str
    

    @app.post(f"/{PREFIX}/create", status_code=201)
    async def create_source(request: CreateSourceRequest) -> SimpleResponse:
        source = db.Source()
        source.source_type_id = request.type_id
        source.name = request.name
        session.add(source)
        db.try_commit(session, HTTPException(500, "Database Error"))
        return SimpleResponse(id=source.id)

    class UpdateSourceRequest(BaseModel):
        id: int
        name: str
        type_id: int

    @app.post(f"/{PREFIX}/update")
    async def update_source(request: UpdateSourceRequest):
        source = session.query(Source).filter(Source.id == request.id).first()
        if source is None: raise HTTPException(404, "Source not found")
        source.name = request.name
        source.source_type_id = request.type_id
        db.try_commit(session, HTTPException(500, "Database Error"))

    @app.post(f"/{PREFIX}/delete")
    async def delete_source(request: SimpleRequest):
        source = session.query(Source).filter(Source.id == request.id).first()
        if source is None: return
        session.delete(source)
        db.try_commit(session, HTTPException(500, "Database Error"))

    @app.post(f"/{PREFIX}/items")
    async def get_items_from_source(request: SimpleRequest) -> list[ItemResponse]:
        data = session.query(Source).filter(Source.id == request.id).first()
        if data is None: return []
        l = []
        for item in data.items:
            l.append(make_item_response(item))
        return l
    
    @app.post(f"/{PREFIX}/items/count")
    async def count_items_from_source(request: SimpleRequest) -> int:
        data = session.query(Source).filter(Source.id == request.id).first()
        if data is None: return 0
        return len(data.items)
        
