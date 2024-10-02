from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import SourceType
import database as db

from sqlalchemy.orm import Session

from . import SimpleResponse

PREFIX = "source-data"

class SourceData(BaseModel):
    id: int
    data_type: str
    data_display: str
    data_label: str
    data_label_pos: str
    data_edit: str
    data_options: Optional[str]


class SourceTypeDataResponse(BaseModel):
    id: int
    name: str
    data: list[SourceData]


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


def register(app: FastAPI, session: Session):
    class CreateTypeDataRequest(BaseModel):
        type_id: int
        data_type: db.SourceData.DataTypeEnum
        data_display: db.SourceData.DataDisplayEnum
        data_label: str
        data_label_pos: db.SourceData.DataLabelPosEnum
        data_edit: db.SourceData.DataEditEnum
        data_option: str

    @app.post(f"/{PREFIX}/create", status_code=201)
    async def create_type_data(request: CreateTypeDataRequest) -> SimpleResponse:
        data = db.SourceData()
        data.data_type = request.data_type
        data.data_display = request.data_display
        data.data_label = request.data_label
        data.data_label_pos = request.data_label_pos
        data.data_edit = request.data_edit
        data.data_option = request.data_option
        session.add(data)
        db.try_commit(session, HTTPException(500, "Database Error"))
        return SimpleResponse(id=data.id)
    
    class UpdateTypeDataRequest(BaseModel):
        id: int
        data_type: db.SourceData.DataTypeEnum
        data_display: db.SourceData.DataDisplayEnum
        data_label: str
        data_label_pos: db.SourceData.DataLabelPosEnum
        data_edit: db.SourceData.DataEditEnum
        data_option: str
    
    @app.post(f"/{PREFIX}/update")
    async def create_type_data(request: UpdateTypeDataRequest):
        data = session.query(db.SourceData).filter(db.SourceData.id == request.id).first()
        if data is None: raise HTTPException(404, "Type data not found")
        data.data_type = request.data_type
        data.data_display = request.data_display
        data.data_label = request.data_label
        data.data_label_pos = request.data_label_pos
        data.data_edit = request.data_edit
        data.data_option = request.data_option
        db.try_commit(session, HTTPException(500, "Database Error"))
