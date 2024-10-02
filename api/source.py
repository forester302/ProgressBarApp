import inspect
from fastapi import FastAPI
from pydantic import BaseModel
from database import Source, SourceType
from sqlalchemy.orm import Session
class SourceData(BaseModel):
    id: int
    data_type: str
    data_display: str
    data_label: str
    data_label_pos: str
    data_edit: str
    data_options: str | None

def make_source_data_list(type_: SourceType):
    return [
        SourceData(
            id=data.id, 
            data_type=data.data_type, 
            data_display=data.data_display,
            data_label=data.data_label,
            data_label_pos=data.data_label_pos,
            data_edit=data.data_edit,
            data_options=data.data_options
        ) for data in type_.source_data]

def sources(app: FastAPI, session: Session):
    class SourceResponse(BaseModel):
        id: int
        name: str
        type: int

    @app.post("/sources")
    async def get_sources() -> list[SourceResponse]:
        sources = session.query(Source)
        if (sources.first() is None):
            return []
        else:
            l = []
            for source in sources.all():
                l.append(SourceResponse(id=source.id, name=source.name, type=source.source_type_id))
            return l

def typeData(app: FastAPI, session: Session):
    class SourceDataQuery(BaseModel):
        id: int
    class SourceDataResponse(BaseModel):
        id: int
        name: str
        data: list[SourceData]
    @app.post("/type")
    async def get_type(query: SourceDataQuery) -> SourceDataResponse:
        type_ = session.query(SourceType).filter(SourceType.id == query.id).first()
        if type_ is not None:
            return SourceDataResponse(id=type_.id, name=type_.name, data=make_source_data_list(type_))
        return SourceDataResponse(id=0, name="", data=[])
    
    @app.post("/types")
    async def get_types() -> list[SourceDataResponse]:
        data = session.query(SourceType)
        if data.first() is None:
            return []
        else:
            l = []
            for type_ in data.all():
                l.append(SourceDataResponse(id=type_.id, name=type_.name, data=make_source_data_list(type_)))
            return l

def register(app: FastAPI, session: Session):
    for name, obj in globals().items():
        if inspect.isfunction(obj) and obj.__module__ == __name__ and name not in {"register", "make_source_data_list"}:
            obj(app, session)