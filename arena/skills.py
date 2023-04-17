from __future__ import annotations

from abc import ABC, abstractmethod
from random import choice
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from units import BaseUnit


class AbstractSkill(ABC):
    def __init__(self):
        self.name = 'Базовый'
        self.power: float = 0
        self.required_stamina: float = 0
        self.regen_count: int = 5

    @property
    def get_required_stamina(self):
        return self.required_stamina

    def use(self, attacker: BaseUnit, target: BaseUnit):
        if self.required_stamina > attacker._stamina:
            return (f"{attacker.get_name} попробовал применить {self.name} "
                    "но так сильно устал что ничего не получилось")
        return self.skill_effect(attacker, target)

    @abstractmethod
    def skill_effect(self, attacker: BaseUnit, target: BaseUnit) -> str:
        pass


class SkillKick(AbstractSkill):
    def __init__(self):
        self.name = 'Свирепый Пинок'
        self.power = 12
        self.required_stamina = 6
        self.regen_count = 5

    def skill_effect(self, attacker: BaseUnit, target: BaseUnit) -> str:
        full_damage = self.power * attacker._attack_mod
        caused_damage = target._take_damage(full_damage)

        if caused_damage == 0:
            return (f"{attacker._name} используя {self.name} "
                    f"наносит удар, но соперник уворачивается "
                    f"и не получает урона")
        else:
            return (f"{attacker._name} используя {self.name} "
                    f"сбивает соперника с ног и "
                    f"наносит {caused_damage:.1f} урона")


class SkillPrick(AbstractSkill):
    def __init__(self):
        self.name = 'Мощный Укол'
        self.power = 15
        self.required_stamina = 5
        self.regen_count = 4

    def skill_effect(self, attacker: BaseUnit, target: BaseUnit) -> str:
        full_damage = self.power * attacker._attack_mod
        caused_damage = target._take_damage(full_damage)

        if caused_damage == 0:
            return (f"{attacker._name} используя {self.name} "
                    f"наносит удар, но соперник уворачивается "
                    f"и не получает урона")
        else:
            return (f"{attacker._name} используя {self.name} "
                    f"пробивает {target._armor.name} соперника и "
                    f"наносит {caused_damage:.1f} урона")


class SkillPrayer(AbstractSkill):
    def __init__(self):
        self.name = 'Молитва Господу'
        self.power = 15
        self.required_stamina = 3
        self.regen_count = 3

    def skill_effect(self, attacker: BaseUnit, target: BaseUnit) -> str:
        full_heal = self.power * attacker._attack_mod
        caused_heal = attacker._get_heal(full_heal)

        return (f"{attacker._name} вместо атаки применил {self.name}, "
                f"получил благословение и восстановил {caused_heal:.1f} "
                f"жизненной силы")


def skill_factory(unit_type: str) -> AbstractSkill:
    "Выберает случайное доступное умение в зависимости от типа"

    if unit_type == 'warrior':
        skill = SkillKick
    elif unit_type == 'thief':
        skill = choice([SkillPrick, SkillKick])
    elif unit_type == 'priest':
        skill = SkillPrayer
    else:
        raise TypeError

    return skill()
