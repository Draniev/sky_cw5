import logging
from typing import Literal

from .units import BaseUnit

logger = logging.getLogger('arena')

UNITS = Literal['hero', 'enemy']
ACTIONS = Literal['hit', 'pass', 'feat']


def circle_count(max_count: int, current: int):
    return current + 1 if current < max_count else 0


class ArenaLog:
    def __init__(self):
        self.log: list[list[str]] = []

    def add_record(self, record: str):
        self.log[-1].append(record)
        return self.log[-1]

    def add_new_round(self):
        self.log.append([])
        return self.log[-1]

    def get_log(self) -> list[tuple]:
        return self.log

    def get_plain_log(self) -> list[str]:
        plain_log = []
        if len(self.log) == 0:
            return plain_log

        round_index = 0
        for round in self.log:
            for action in round:
                str_log = ": ".join([str(round_index), action])
                plain_log.append(str_log)
            round_index += 1
        return plain_log

    def purge(self):
        self.log = []


class BaseArena:
    def __init__(self, *args):
        self._units: dict[UNITS, BaseUnit | None] = {'hero': None, 'enemy': None}
        self._action: dict[UNITS, ACTIONS | None] = {'hero': None, 'enemy': None}
        self._round: int = 0
        self.is_battle_going_on: bool = False
        self.winner: BaseUnit | None = None
        self.loser: BaseUnit | None = None
        self.log = ArenaLog()

    def set_unit(self, cur_unit: UNITS, unit: BaseUnit):
        self._units[cur_unit] = unit

    def set_action(self, cur_unit: UNITS, action: ACTIONS):
        self._action[cur_unit] = action

    def _make_action(self, action: ACTIONS | Literal['exit'],
                     attacker: BaseUnit,
                     target: BaseUnit) -> str:
        if action == 'hit':
            result = attacker.hit(target)
        elif action == 'pass':
            result = attacker.skip_turn()
        elif action == 'feat':
            result = attacker.use_skill(target)
        elif action == 'exit':
            result = self.force_stop()
        else:
            raise TypeError
        return result

    def fight_cur_round(self):
        log = self.log.add_new_round()
        if not self.is_battle_going_on:
            msg = "Идите домой, бой уже окончен (или даже не начинался)!"
            log = self.log.add_record(msg)
            return log

        hero_action = self._make_action(self._action['hero'],
                                        self._units['hero'],
                                        self._units['enemy'])

        log = self.log.add_record(hero_action)
        if not self._units['enemy'].is_alife:
            hero_win = self._stop(winner='hero', loser='enemy')
            log = self.log.add_record(hero_win)
            return log

        enemy_action = self._make_action(self._action['enemy'],
                                         self._units['enemy'],
                                         self._units['hero'])

        log = self.log.add_record(enemy_action)
        if not self._units['hero'].is_alife:
            enemy_win = self._stop(winner='enemy', loser='hero')
            log = self.log.add_record(enemy_win)
            return log

        self._round += 1
        self._units['hero'].regen_stamina()
        self._units['enemy'].regen_stamina()
        self._units['hero'].regen_skill()
        self._units['enemy'].regen_skill()
        return log

    def _stop(self, winner: UNITS, loser: UNITS):
        self.is_battle_going_on = False
        self.winner = self._units[winner]
        self.loser = self._units[loser]
        rec = f'На этом жизненные силы {self.loser.get_name} закончились и он упал ' \
              f'оземь. Бой был сложный, но {self.winner.get_name} победил!'
        return rec

    def force_stop(self):
        self.is_battle_going_on = False
        rec = 'Бой закончен неожиданно, все разбежались!'
        return rec

    def start(self):
        self.is_battle_going_on = True

    def get_clean(self):
        self._units = {'hero': None, 'enemy': None}
        self._round = 0
        self.log.purge()
        self.winner = None
        self.loser = None
        self.is_battle_going_on = False
