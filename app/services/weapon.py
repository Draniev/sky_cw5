from ..dao.models.weapon import WeaponModel
from ..dao.weapon import WeaponDAO


class WeaponService():
    def __init__(self, weapon_dao: WeaponDAO) -> None:
        self.weapon_dao = weapon_dao

    def load_all(self) -> list[WeaponModel]:
        return self.weapon_dao.get_all()

    def load_id(self, id: int) -> WeaponModel:
        return self.weapon_dao.get_one(id)
