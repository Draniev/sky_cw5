from sqlalchemy import Column, String

from .basemodel import BaseModel


class ClassTypeModel(BaseModel):
    __tablename__ = 'class_type'
    name = Column(String(255))
