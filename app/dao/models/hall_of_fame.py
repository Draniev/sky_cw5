from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .basemodel import BaseModel


class HallOfFameModel(BaseModel):
    __tablename__ = 'hall_of_fame'
    turns = Column(Integer)

    u1_name = Column(String(255))
    u1_class_id = Column(Integer, ForeignKey('class_type.id'))
    u1_weapon_id = Column(Integer, ForeignKey('weapon.id'))
    u1_armor_id = Column(Integer, ForeignKey('armor.id'))

    u2_name = Column(String(255))
    u2_class_id = Column(Integer, ForeignKey('class_type.id'))
    u2_weapon_id = Column(Integer, ForeignKey('weapon.id'))
    u2_armor_id = Column(Integer, ForeignKey('armor.id'))

    u1_class = relationship('ClassTypeModel',
                            foreign_keys=[u1_class_id],
                            )
    u1_weapon = relationship('WeaponModel',
                             foreign_keys=[u1_weapon_id],
                             )
    u1_armor = relationship('ArmorModel',
                            foreign_keys=[u1_armor_id],
                            )
    u2_class = relationship('ClassTypeModel',
                            foreign_keys=[u2_class_id],
                            )
    u2_weapon = relationship('WeaponModel',
                             foreign_keys=[u2_weapon_id],
                             )
    u2_armor = relationship('ArmorModel',
                            foreign_keys=[u2_armor_id],
                            )
