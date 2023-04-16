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


class BaseArena:
    def __init__(self, *args):
        self._units: dict[UNITS, BaseUnit | None] = {'hero': None, 'enemy': None}
        self._action: dict[UNITS, ACTIONS | None] = {'hero': None, 'enemy': None}
        self._round: int = 0
        self.is_battle_going_on: bool = False
        self.winner: BaseUnit | None = None
        self.loser: BaseUnit | None = None
        self.arena_log = ArenaLog()
        # self._current_attacker: int = 0
        # self._current_target: int = 1

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
            self.is_battle_going_on = False
            result = 'Бой внезапно закончен'
        else:
            raise TypeError
        return result

    def fight_cur_round(self):
        if not self.is_battle_going_on:
            return "Идите домой, бой уже окончен (или даже не начинался)!"
        log = self.arena_log.add_new_round()

        hero_action = self._make_action(self._action['hero'],
                                        self._units['hero'],
                                        self._units['enemy'])

        log = self.arena_log.add_record(hero_action)
        if not self._units['enemy'].is_alife:
            hero_win = self._close_arena(winner='hero', loser='enemy')
            log = self.arena_log.add_record(hero_win)
            return log

        enemy_action = self._make_action(self._action['enemy'],
                                         self._units['enemy'],
                                         self._units['hero'])

        log = self.arena_log.add_record(enemy_action)
        if not self._units['hero'].is_alife:
            enemy_win = self._close_arena(winner='enemy', loser='hero')
            log = self.arena_log.add_record(enemy_win)
            return log

        self._round += 1
        self._units['hero'].regen_stamina()
        self._units['enemy'].regen_stamina()
        return log

    def _close_arena(self, winner: UNITS, loser: UNITS):
        self.is_battle_going_on = False
        self.winner = self._units[winner]
        self.loser = self._units[loser]
        rec = f'На этом жизненные силы {self.loser.get_name} закончились и он упал ' \
              f'оземь. Бой был сложный, но {self.winner.get_name} победил!'
        return rec

    def start_arena(self):
        self.is_battle_going_on = True
