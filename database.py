from datetime import date, datetime
from sqlalchemy import Enum, ForeignKey, create_engine, Column, Integer, String, DateTime, Date
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, sessionmaker, relationship, declarative_base, Session
from sqlalchemy.sql import func

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class SourceType(Base):
    __tablename__ = "source_types"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)

    sources: Mapped["Source"] = relationship("Source", back_populates="source_type")
    source_data: Mapped[list["SourceData"]] = relationship("SourceData", back_populates="source_type")


class SourceData(Base):
    __tablename__ = "source_data"

    id: Mapped[int] = Column(Integer, primary_key=True)
    source_type_id: Mapped[int] = Column(Integer, ForeignKey("source_types.id"))

    class DataTypeEnum(str, PyEnum):
        int = "int",
        float = "float",
        string = "string",
    data_type: Mapped[DataTypeEnum] = Column(Enum(DataTypeEnum), nullable=False)
    class DataDisplayEnum(str, PyEnum):
        all = "all",
        truncate = "truncate",
        none = "none",
    data_display: Mapped[DataDisplayEnum] = Column(Enum(DataDisplayEnum), nullable=False)

    data_label:Mapped[str] = Column(String, nullable=True)
    class DataLabelPosEnum(str, PyEnum):
        left = "left",
        right = "right"
        up = "up"
        down = "down"
    data_label_pos: Mapped[DataLabelPosEnum] = Column(Enum(DataLabelPosEnum), nullable=True)
    class DataEditEnum(str, PyEnum):
        textbox = "textbox",
        input = "input",
        dropdown = "dropdown",
        slider = "slider"
    data_edit: Mapped[DataEditEnum] = Column(Enum(DataEditEnum), nullable=False)
    data_options: Mapped[str] = Column(String, nullable=True)

    source_type: Mapped[SourceType] = relationship("SourceType", back_populates="source_data")

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = Column(Integer, primary_key=True)
    source_type_id: Mapped[int] = Column(Integer, ForeignKey(
        "source_types.id"), nullable=False)
    name: Mapped[str] = Column(String, nullable=False)

    status_groups: Mapped[list["StatusGroup"]] = relationship("StatusGroup", back_populates="source")
    source_type: Mapped[SourceType] = relationship("SourceType", back_populates="sources")
    items: Mapped[list["Item"]] = relationship("Item", back_populates="source")

class StatusGroup(Base):
    __tablename__ = "status_groups"

    id: Mapped[int] = Column(Integer, primary_key=True)
    source_id: Mapped[int] = Column(Integer, ForeignKey('sources.id'), nullable=False)
    name: Mapped[str] = Column(String)
    class StatusTypeEnum(str, PyEnum):
        not_started = "not_started"
        in_progress = "in_progress"
        complete = "complete"
    type: Mapped[StatusTypeEnum] = Column(Enum(StatusTypeEnum))

    source: Mapped[Source] = relationship("Source", back_populates="status_groups")
    statuses: Mapped[list["Status"]] = relationship("Status", back_populates="status_group")

class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = Column(Integer, primary_key=True)
    status_group_id: Mapped[int] = Column(Integer, ForeignKey(
        'status_groups.id'), nullable=False)
    name: Mapped[str] = Column(String, nullable=False)

    status_group: Mapped[StatusGroup] = relationship("StatusGroup", back_populates="statuses")
    items: Mapped["Item"] = relationship("Item", back_populates="status")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = Column(Integer, primary_key=True)
    source_id: Mapped[int] = Column(Integer, ForeignKey("sources.id"), nullable=False)
    status_id: Mapped[int] = Column(Integer, ForeignKey("statuses.id"), nullable=False)

    date_submitted: Mapped[date] = Column(Date, nullable=True)
    last_updated: Mapped[datetime] = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    data: Mapped[str] = Column(String, nullable=True)

    source: Mapped[Source] = relationship("Source", back_populates="items")
    status: Mapped[Status] = relationship("Status", back_populates="items")

Base.metadata.create_all(engine)

session = SessionLocal()

def try_commit(session: Session, e: Exception):
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

if __name__ == "__main__":
    from eralchemy import render_er

    render_er(Base, 'ERD.png')
