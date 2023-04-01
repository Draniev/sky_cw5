from art import tprint

from arena import BaseArena
from equipment import Armor, Weapon
from units import UnitFactory

if __name__ == '__main__':
    tprint("battle", font="univerce")

    blade1 = Weapon(1, 'Простой клинок', 2.5, 6.5, 2)
    armor1 = Armor(1, 'Кольчужка', 3, 1)

    unit_factory = UnitFactory()
    user1 = unit_factory.create('Корявый Победум', 'warrior', blade1, armor1)
    user2 = unit_factory.create('Хитрый Кофтун', 'warrior', blade1, armor1)
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
