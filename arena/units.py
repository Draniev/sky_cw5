import logging
from abc import ABC
from random import uniform
from typing import Literal

from .equipment import Armor, Weapon
from .game_constants import REGEN_STAMINA_PER_TURN
from .skills import AbstractSkill, skill_factory

logger = logging.getLogger('arena')


class BaseUnit(ABC):
    def __init__(self, name: str = 'Уставший Крестьянин'):
        self._name: str = name

        self._skill: AbstractSkill | None = None
        self._armor: Armor = Armor(id=0, name='фуфайка',
                                   defence=1, stamina_per_turn=0.5)
        self._weapon: Weapon | None = None

        self._unit_type = 'Человечище'
        self._max_health: float = 30
        self._max_stamina: float = 20
        self._attack_mod: float = 0.5
        self._defence_mod: float = 0.5
        self._stamina_mod: float = 1

        self._health = self._max_health
        self._stamina = self._max_stamina

    @property
    def get_name(self) -> str:
        return self._name

    @property
    def get_health(self) -> float:
        return self._health

    @property
    def _get_hit_damage(self) -> float:
        "Возвращает силу удара оружием в текущий ход (случайное)"

        if not self._weapon:
            return 0
        random_damage = uniform(self._weapon.min_damage,
                                self._weapon.max_damage)
        full_damage = random_damage * self._attack_mod
        return full_damage

    @property
    def _get_defence(self) -> float:
        "Возвращает силу защиты (плюс/минус 50% от показателя брони)"

        random_defence = uniform(self._armor.defence * 0.5,
                                 self._armor.defence * 1.5)
        full_defence = random_defence * self._defence_mod
        return full_defence

    @property
    def is_alife(self) -> bool:
        return True if self._health > 0 else False

    def set_weapon(self, weapon: Weapon):
        self._weapon = weapon

    def set_armor(self, armor: Armor):
        self._armor = armor

    def set_skill(self, skill: AbstractSkill):
        self._skill = skill

    def _change_health(self, health: float, reduce: bool = True) -> float:
        """Изменяет значение жизни на health, но не более MAX
           По умолчанию: уменьшает, чтобы увеличить: reduce = False
        """
        hp_before_change = self._health
        if reduce:
            self._health -= health
            if self._health < 0:
                self._health = 0
        else:
            self._health += health
            if self._health > self._max_health:
                self._health = self._max_health

        logger.debug(f'CHANGE {self.get_name} '
                     f'HP:{hp_before_change:.1f}->{self._health:.1f}')
        return self._health

    def _change_stamina(self, stamina: float, reduce: bool = True) -> float:
        """Изменяет значение жизни на stamina, но не более MAX
           По умолчанию: уменьшает, чтобы увеличить: reduce = False
        """
        st_before_change = self._stamina
        if reduce:
            self._stamina -= stamina
            if self._stamina < 0:
                self._stamina = 0
        else:
            self._stamina += stamina
            if self._stamina > self._max_stamina:
                self._stamina = self._max_stamina

        logger.debug(f'CHANGE {self.get_name} '
                     f'ST:{st_before_change:.1f}->{self._stamina:.1f}')
        return self._stamina

    def _use_armor(self, damage: float) -> float:
        "Возвращает кол-во урона, поглощённого бронёй"

        if self._stamina < self._armor.stamina_per_turn:
            adsorbed_damage = 0
        else:
            adsorbed_damage = self._get_defence
        return adsorbed_damage if adsorbed_damage < damage else damage

    def hit(self, target: 'BaseUnit'):
        "Наносит удар по противнику оружием"

        if not self._weapon:
            return (f"{self._name} хотел было атаковать {target._name}, "
                    "но не вовремя обнаружил что забыл свою шпагу!")

        if self._stamina < self._weapon.stamina_per_hit:
            self._spent_stamina('pass')
            return (f"{self._name} вздернул свой {self._weapon.name}, "
                    "но так устал, что не смог попасть по противнику")

        full_damage = self._get_hit_damage
        caused_damage = target._take_damage(full_damage)

        self._spent_stamina('hit')
        if caused_damage == 0:
            return (f"{self._name} используя {self._weapon.name} "
                    f"наносит удар, но соперник уворачивается "
                    f"и не получает урона")
        else:
            return (f"{self._name} используя {self._weapon.name} "
                    f"пробивает {target._armor.name} соперника и "
                    f"наносит {caused_damage:.1f} урона")

    def _take_damage(self, damage: float) -> float:
        "Рассчет кол-ва полученного урона в зависимости от усталости и брони"

        take_damage = damage - self._use_armor(damage)
        self._change_health(take_damage)
        self._spent_stamina('defence')
        return take_damage

    def _get_heal(self, heal: float) -> float:
        "А что если наши герои смогут и получиться в бою? :)"

        hp_before_heal = self._health
        return self._change_health(heal, reduce=False) - hp_before_heal

    def _spent_stamina(self, mod: Literal['hit',
                                          'defence',
                                          'pass',
                                          'skill']) -> float:
        "Рассчет кол-ва стамины после действий юнита"

        stamina_costs = 0
        stamina_before_spent = self._stamina

        if mod == 'pass':
            stamina_costs = 0  # На случай если нужна будет балансировка
        elif mod == 'hit' and self._weapon:
            stamina_costs = self._weapon.stamina_per_hit
        elif mod == 'defence':
            stamina_costs = self._armor.stamina_per_turn
        elif mod == 'skill' and self._skill:
            stamina_costs = self._skill.get_required_stamina

        new_stamina = self._change_stamina(stamina_costs)
        # new_stam = self._change_stamina(REGEN_STAMINA_PER_TURN, reduce=False)

        logger.debug(f'SPENT {self.get_name} '
                     f'ST:{stamina_before_spent:.1f}->{new_stamina:.1f}')
        return stamina_before_spent - new_stamina

    def regen_stamina(self) -> float:
        "Регенерация стамины раз в ЦИКЛ, после того как все сделали действие"

        stamina_before_regen = self._stamina
        new_stamina = self._change_stamina(REGEN_STAMINA_PER_TURN,
                                           reduce=False)

        logger.debug(f'REGEN {self.get_name} '
                     f'ST:{stamina_before_regen:.1f}->{new_stamina:.1f}')
        return new_stamina - stamina_before_regen

    def use_skill(self, target: 'BaseUnit'):
        "Использует специальное умение Юнита"

        if not self._skill:
            result = (f"{self._name} хотел было воспользоваться каким то "
                      "приёмом, да так плохо учился в Институте Ножевого "
                      "Боя что оступился и упал")
        else:
            result = self._skill.use(self, target)
        self._spent_stamina('skill')
        return result

    def skip_turn(self):
        "В свой ход не наносит удар, но восстанавливает силы"

        self._spent_stamina('pass')
        return f"{self._name} затаился и выжидает удобного момента для удара"

    def __repr__(self):
        return (f'{self._unit_type} {self._name}: '
                f'hp {self._health:.1f}/{self._max_health}, '
                f'st {self._stamina:.1f}/{self._max_stamina}')


class UnitWarrior(BaseUnit):
    def __init__(self, name: str = 'Мимопроходивший Воин'):
        super().__init__(name)

        self._unit_type = 'Воин'
        self._max_health: float = 60
        self._max_stamina: float = 30
        self._attack_mod: float = 2.9
        self._stamina_mod: float = 0.8
        self._defence_mod: float = 1.2

        self._health = self._max_health
        self._stamina = self._max_stamina


class UnitThief(BaseUnit):
    def __init__(self, name: str = 'Скрытный воришка'):
        super().__init__(name)

        self._unit_type = 'Вор'
        self._max_health: float = 50
        self._max_stamina: float = 25
        self._attack_mod: float = 1.5
        self._stamina_mod: float = 1.2
        self._defence_mod: float = 1.0

        self._health = self._max_health
        self._stamina = self._max_stamina


class UnitPriest(BaseUnit):
    def __init__(self, name: str = 'Серый Проповедник'):
        super().__init__(name)

        self._unit_type = 'Священник'
        self._max_health: float = 30
        self._max_stamina: float = 20
        self._attack_mod: float = 1.0
        self._stamina_mod: float = 1.0
        self._defence_mod: float = 1.0

        self._health = self._max_health
        self._stamina = self._max_stamina


class UnitFactory:
    def create(self,
               name: str,
               unit_type: str,
               weapon: Weapon | None = None,
               armor: Armor | None = None):

        if unit_type == 'warrior':
            unit = UnitWarrior(name)
        elif unit_type == 'thief':
            unit = UnitThief(name)
        elif unit_type == 'priest':
            unit = UnitPriest(name)
        else:
            raise TypeError

        if weapon:
            unit.set_weapon(weapon)
        if armor:
            unit.set_armor(armor)

        skill = skill_factory(unit_type)
        unit.set_skill(skill)

        return unit
