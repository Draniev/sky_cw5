from abc import ABC, abstractmethod

from units import BaseUnit


class AbstractSkill(ABC):
    def __init__(self):
        self.name = 'Базовый'
        self.power: float = 0
        self.required_stamina: float = 0

    @property
    def get_required_stamina(self):
        return self.required_stamina

    def use(self, attacker: BaseUnit, target: BaseUnit):
        if self.required_stamina > attacker.get_stamina:
            return (f"{attacker.get_name} попробовал применить {self.name} "
                    "но так сильно устал что ничего не получилось")
        return self.skill_effect(attacker, target)

    @abstractmethod
    def skill_effect(self, attacker: BaseUnit, target: BaseUnit):
        pass


class SkillKick(AbstractSkill):
    def __init__(self):
        self.name = 'Свирепый Пинок'
        self.power = 12
        self.required_stamina = 6

    def skill_effect(self, attacker: BaseUnit, target: BaseUnit):
        pass


class SkillPrick(AbstractSkill):
    def __init__(self):
        self.name = 'Мощный укол'
        self.power = 15
        self.required_stamina = 5

    def skill_effect(self, attacker: BaseUnit, target: BaseUnit):
        pass


class SkillPrayer(AbstractSkill):
    def __init__(self):
        self.name = 'Молитва Господу'
        self.power = 15
        self.required_stamina = 3

    def skill_effect(self, attacker: BaseUnit, target: BaseUnit):
        pass


def skill_factory(unit_type: str) -> AbstractSkill:

    if unit_type == 'warrior':
        pass
    elif unit_type == 'thief':
        pass
    elif unit_type == 'priest':
        pass
    else:
        raise TypeError
