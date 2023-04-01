from abc import ABC
from random import uniform
from typing import Literal

from equipment import Armor, Weapon
from game_constants import REGEN_STAMINA_PER_TURN
from skills import AbstractSkill


class BaseUnit(ABC):
    def __init__(self, name: str = 'Уставший Крестьянин'):
        self.name: str = name

        self.unit_type = 'Человечище'
        self.max_health: float = 30
        self.max_stamina: float = 20
        self.attack_mod: float = 0.5
        self.defence_mod: float = 0.5
        self.stamina_mod: float = 1

        self.skill: AbstractSkill = None
        self.armor: Armor = None
        self.weapon: Weapon = None

        self.health = self.max_health
        self.stamina = self.max_stamina

    @property
    def get_name(self):
        return self.name

    @property
    def get_stamina(self):
        return self.stamina

    @property
    def get_health(self):
        return self.health

    @property
    def is_alife(self) -> bool:
        return True if self.health > 0 else False

    def set_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def set_armor(self, armor: Armor):
        self.armor = armor

    def hit(self, target: 'BaseUnit'):
        if self.stamina < self.weapon.stamina_per_hit:
            self._regenerate_stamina('pass')
            return (f"{self.name} вздернул свой {self.weapon.name}, "
                    "но так устал, что не смог попасть по противнику")

        random_damage = uniform(self.weapon.min_damage,
                                self.weapon.max_damage)
        full_damage = random_damage * self.attack_mod
        caused_damage = target._get_damage(full_damage)

        self._regenerate_stamina('hit')
        if caused_damage == 0:
            return (f"{self.name} используя {self.weapon.name} "
                    f"наносит удар, но соперник уворачивается"
                    f"и не получает урона")
        else:
            return (f"{self.name} используя {self.weapon.name} "
                    f"пробивает {target.armor.name} соперника и"
                    f" наносит {caused_damage:.1f} урона")

    def _get_damage(self, damage):
        "Рассчет кол-ва полученного урона в зависимости от усталости и брони"

        if self.stamina < self.armor.stamina_per_turn:
            get_damage = damage
        else:
            get_damage = damage - self.armor.defence * self.defence_mod

        if get_damage < 0:
            get_damage = 0
        else:
            self.health -= get_damage

        self._regenerate_stamina('defence')
        return get_damage

    def _regenerate_stamina(self, mod: Literal['hit', 'defence', 'pass']):
        if mod == 'hit':
            stamina_costs = self.weapon.stamina_per_hit
        elif mod == 'defence':
            stamina_costs = self.armor.stamina_per_turn
        elif mod == 'pass':
            stamina_costs = 0

        self.stamina -= stamina_costs if self.stamina > stamina_costs else 0
        self.stamina += REGEN_STAMINA_PER_TURN * self.stamina_mod
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina

    def use_skill(self, target: 'BaseUnit'):
        pass

    def skip_turn(self):

        self._regenerate_stamina('pass')
        return f"{self.name} затаился и выжидает удобного момента для удара"

    def __repr__(self):
        return (f'{self.unit_type} {self.name}: '
                f'hp {self.health:.1f}/{self.max_health}, '
                f'st {self.stamina:.1f}/{self.max_stamina}')


class UnitWarrior(BaseUnit):
    def __init__(self, name: str = 'Мимопроходивший Воин'):
        self.name: str = name

        self.unit_type = 'Воин'
        self.max_health: float = 60
        self.max_stamina: float = 30
        self.attack_mod: float = 0.8
        self.stamina_mod: float = 0.9
        self.defence_mod: float = 1.2

        self.skill: AbstractSkill = None
        self.armor: Armor = None
        self.weapon: Weapon = None

        self.health = self.max_health
        self.stamina = self.max_stamina


class UnitThief(BaseUnit):
    def __init__(self, name: str = 'Скрытный воришка'):
        self.name: str = name

        self.unit_type = 'Вор'
        self.max_health: float = 50
        self.max_stamina: float = 25
        self.attack_mod: float = 1.5
        self.stamina_mod: float = 1.2
        self.defence_mod: float = 1.0

        self.skill: AbstractSkill = None
        self.armor: Armor = None
        self.weapon: Weapon = None

        self.health = self.max_health
        self.stamina = self.max_stamina


class UnitFactory:
    def create(self,
               name: str,
               unit_type: str,
               weapon: Weapon = None,
               armor: Armor = None):

        if unit_type == 'warrior':
            unit = UnitWarrior(name)
        elif unit_type == 'thief':
            unit = UnitThief(name)
        elif unit_type == 'priest':
            pass
        else:
            raise TypeError

        if weapon:
            unit.set_weapon(weapon)
        if armor:
            unit.set_armor(armor)

        return unit
