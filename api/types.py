from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SourceType
import database as db
from .source_data import SourceTypeDataResponse, make_source_data_list
from . import SimpleRequest, SimpleResponse

PREFIX = "source-type"
def register(app: FastAPI, session: Session):
    @app.post(f"/{PREFIX}/all")
    async def get_types() -> list[SourceTypeDataResponse]:
        data = session.query(SourceType)
        if data.first() is None:
            return []
        else:
            l = []
            for type_ in data.all():
                l.append(SourceTypeDataResponse(
                    id=type_.id, name=type_.name, data=make_source_data_list(type_)))
            return l

    @app.post(f"/{PREFIX}")
    async def get_type(query: SimpleRequest) -> SourceTypeDataResponse:
        type_ = session.query(SourceType).filter(
            SourceType.id == query.id).first()
        if type_ is None:
            raise HTTPException(404, "Type not found")
        return SourceTypeDataResponse(id=type_.id, name=type_.name, data=make_source_data_list(type_))

    class CreateTypeRequest(BaseModel):
        name: str

    @app.post(f"/{PREFIX}/create", status_code=201)
    async def create_type(request: CreateTypeRequest) -> SimpleResponse:
        type_ = SourceType()
        type_.name = request.name
        session.add(type_)
        db.try_commit(session, HTTPException(500, "Database Error"))
        return SimpleResponse(id=type_.id)

    class UpdateTypeRequest(BaseModel):
        id: int
        name: str

    @app.post(f"/{PREFIX}/update")
    async def update_type(request: UpdateTypeRequest):
        type_ = session.query(SourceType).filter(SourceType.id == request.id).first()
        if type_ is None: raise HTTPException(404, "Type not found")
        type_.name = request.name
        db.try_commit(session, HTTPException(500, "Database Error"))
