from sqlalchemy import Column, DateTime, Integer, func

from app.setup.db import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    created = Column(DateTime, nullable=False, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
