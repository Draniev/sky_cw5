from arena.arena import BaseArena
from arena.units import UnitFactory

from .dao.armor import ArmorDAO
from .dao.hall_of_fame import HallOfFameDAO
from .dao.weapon import WeaponDAO
from .services.armor import ArmorService
from .services.hall_of_fame import HallOfFameService
from .services.weapon import WeaponService
from .setup.db import db

armor_dao = ArmorDAO(db.session)
weapon_dao = WeaponDAO(db.session)
hall_of_fame_dao = HallOfFameDAO(db.session)

armor_service = ArmorService(armor_dao)
weapon_service = WeaponService(weapon_dao)
hall_of_fame_dao = HallOfFameService(hall_of_fame_dao)

unit_factory = UnitFactory()
arena = BaseArena()
