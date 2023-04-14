from ..dao.armor import ArmorDAO
from ..dao.models.armor import ArmorModel


class ArmorService():
    def __init__(self, armor_dao: ArmorDAO) -> None:
        self.armor_dao = armor_dao

    def get_all(self) -> list[ArmorModel]:
        return self.armor_dao.get_all()

    def get_by_id(self, id: int) -> ArmorModel:
        return self.armor_dao.get_one(id)

    def get_by_name(self, name: str) -> ArmorModel:
        return self.armor_dao.get_by_name(name)
