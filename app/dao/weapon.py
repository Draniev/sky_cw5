from .base_dao import BaseDAO
from .models.weapon import WeaponModel


class WeaponDAO(BaseDAO[WeaponModel]):
    __model__ = WeaponModel
