import logging
from random import choice

from art import tprint

from arena import BaseArena
from load_data import equipment
from units import UnitFactory

logger = logging.getLogger('arena')
console_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel('DEBUG')

if __name__ == '__main__':
    tprint("battle", font="univerce")

    # blade1 = Weapon(id=1, name='Простой клинок',
    #                 min_damage=2.5, max_damage=6.5,
    #                 stamina_per_hit=2)
    # armor1 = Armor(id=1, name='Кольчужка', defence=3, stamina_per_turn=1)
    blade1 = choice(equipment.weapons)
    blade2 = choice(equipment.weapons)
    armor1 = choice(equipment.armors)
    armor2 = choice(equipment.armors)

    unit_factory = UnitFactory()
    user1 = unit_factory.create('Корявый Победум', 'warrior', blade1, armor1)
    # user2 = unit_factory.create('Хитрый Кофтун', 'warrior', blade1, armor1)
    user2 = unit_factory.create(
        'Святейший Анатолием', 'priest', blade2, armor2)
    arena = BaseArena(user1, user2)

    user_input = ""
    while user_input not in ('exit', 'stop', 'стоп'):
        user_input = input(
            "\nСделайте ход (hit, pass, feat) или stop|status: ")
        if user_input in ('status', 'статус', 'exit', 'stop', 'стоп'):
            print(user1)
            print(user2)
        else:
            try:
                res = arena.make_a_move(user_input)
                print(res)
            except Exception as e:
                print(f"Error: {e}")
