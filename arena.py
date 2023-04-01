from units import BaseUnit


def circle_count(max_count: int, current: int):
    return current + 1 if current < max_count else 0


class BaseArena:
    def __init__(self, *args):
        self.units: list[BaseUnit] = [*args]
        self._current_attacker: int = 0
        self._current_target: int = 1

        if len(self.units) < 2:
            raise TypeError

    @property
    def get_attacker(self) -> BaseUnit:
        return self.units[self._current_attacker]

    @property
    def get_target(self) -> BaseUnit:
        return self.units[self._current_target]

    def make_a_move(self, move_type: str) -> str:
        attacker = self.get_attacker
        target = self.get_target
        if move_type == 'hit':
            result = attacker.hit(target)
        elif move_type == 'pass':
            result = attacker.skip_turn()
        elif move_type == 'feat':
            result = attacker.use_skill(target)
        else:
            raise TypeError

        self._change_current()
        return result

    def _change_current(self):
        max_index = len(self.units) - 1
        self._current_attacker = circle_count(max_index,
                                              self._current_attacker)
        self._current_target = circle_count(max_index,
                                            self._current_target)
