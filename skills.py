from abc import ABC, abstractmethod


class AbstractSkill(ABC):
    def __init__(self):
        self.name = 'Базовый'
        self.power: float = 0
        self.required_stamina: float = 0

    def use(self, user, target):
        pass

    @abstractmethod
    def skill_effect(self, user, target):
        pass
