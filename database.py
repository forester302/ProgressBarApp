from datetime import date, datetime
from sqlalchemy import Enum, ForeignKey, create_engine, Column, Integer, String, DateTime, Date
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, sessionmaker, relationship, declarative_base
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

    class DataTypeEnum(PyEnum):
        int = 0,
        float = 1,
        string = 2,
    data_type: Mapped[DataTypeEnum] = Column(Enum(DataTypeEnum), nullable=False)
    class DataDisplayEnum(PyEnum):
        all = 0,
        truncate = 1,
        none = 2,
    data_display: Mapped[DataDisplayEnum] = Column(Enum(DataDisplayEnum), nullable=False)

    data_label:Mapped[str] = Column(String, nullable=True)
    class DataLabelPosEnum(PyEnum):
        left = 0,
        right = 1
        up = 2
        down = 3
    data_label_pos: Mapped[DataLabelPosEnum] = Column(Enum(DataLabelPosEnum), nullable=True)
    class DataEditEnum(PyEnum):
        textbox = 0,
        input = 1,
        dropdown = 2,
        slider = 3
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
    class StatusTypeEnum(PyEnum):
        not_started = 0
        in_progress = 2
        complete = 3
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

if __name__ == "__main__":
    from eralchemy import render_er

    render_er(Base, 'ERD.png')
