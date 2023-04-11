from .base_dao import BaseDAO
from .models.armor import ArmorModel


class ArmorDAO(BaseDAO[ArmorModel]):
    __model__ = ArmorModel
