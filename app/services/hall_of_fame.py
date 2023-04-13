from ..dao.hall_of_fame import HallOfFameDAO
from ..dao.models.hall_of_fame import HallOfFameModel


class HallOfFameService():
    def __init__(self, hall_of_fame_dao: HallOfFameDAO) -> None:
        self.hall_of_fame_dao = hall_of_fame_dao

    def load_all(self) -> list[HallOfFameModel]:
        return self.hall_of_fame_dao.get_all()

    def load_id(self, id: int) -> HallOfFameModel:
        return self.hall_of_fame_dao.get_one(id)

    def create_new(self, record: dict):
        return self.hall_of_fame_dao.create(record)
