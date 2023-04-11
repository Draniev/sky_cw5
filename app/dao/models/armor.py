from sqlalchemy import Column, Float, String

from .basemodel import BaseModel


class ArmorModel(BaseModel):
    __tablename__ = 'armor'
    name = Column(String(255))
    degence = Column(Float)
    stamina_per_turn = Column(Float)
