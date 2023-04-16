import logging
from random import choice
from typing import Literal

from art import tprint

from arena.arena import BaseArena, UNITS, ACTIONS
from arena.units import UnitFactory
from load_data import equipment

logger = logging.getLogger('arena')
console_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel('DEBUG')


def choose_action(name: str):
    action = ''
    while action not in (ACTIONS, Literal['exit']):
        action = input(f"\n{name}: Сделайте ход (hit, pass, feat) "
                       f"или (stop, status): ")
        if user_input in ('status', 'статус'):
            print(user1)
            print(user2)
        return action


if __name__ == '__main__':
    tprint("battle", font="univerce")

    blade1 = choice(equipment.weapons)
    blade2 = choice(equipment.weapons)
    armor1 = choice(equipment.armors)
    armor2 = choice(equipment.armors)

    unit_factory = UnitFactory()
    user1 = unit_factory.create('Корявый Победум', 'warrior', blade1, armor1)
    user2 = unit_factory.create(
        'Святейший Анатолием', 'priest', blade2, armor2)
    arena = BaseArena()
    arena.set_unit('hero', user1)
    arena.set_unit('enemy', user2)
    arena.start_arena()

    user_input = ""

    while arena.is_battle_going_on:
        u1_action = choose_action(user1.get_name)
        arena.set_action('hero', u1_action)

        u2_action = choose_action(user2.get_name)
        arena.set_action('enemy', u2_action)

        log = arena.fight_cur_round()
        for item in log:
            print(item)
