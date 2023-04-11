from sqlalchemy import Column, Float, String

from .basemodel import BaseModel


class WeaponModel(BaseModel):
    __tablename__ = 'weapon'
    name = Column(String(255))
    min_damage = Column(Float)
    max_damage = Column(Float)
    stamina_per_hit = Column(Float)
