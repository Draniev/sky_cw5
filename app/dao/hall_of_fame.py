from .base_dao import BaseDAO
from .models.hall_of_fame import HallOfFameModel


class HallOfFameDAO(BaseDAO[HallOfFameModel]):
    __model__ = HallOfFameModel
