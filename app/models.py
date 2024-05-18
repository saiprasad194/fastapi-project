from app.db.database import engine, Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Enum
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr


class UnderlyingBase:

    @declared_attr
    def __tablename__(cls):  # noqa
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


BaseModel = declarative_base(cls=UnderlyingBase)
