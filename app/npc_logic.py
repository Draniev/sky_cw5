from arena.arena import ACTIONS
from arena.units import BaseUnit


def npc_choose_action(unit: BaseUnit) -> ACTIONS:
    """Функция решает каким ударом воспользоваться противнику, но
    только на основании данных о себе (о противнике не знаем)"""

    if unit.is_skill_ready and unit._stamina >= unit._skill.required_stamina:
        if unit._unit_type != 'Священник':
            return 'feat'
        elif unit.get_health < (unit._max_health / 2):
            return 'feat'

    if unit._stamina >= unit._weapon.stamina_per_hit:
        return 'hit'
    else:
        return 'pass'
