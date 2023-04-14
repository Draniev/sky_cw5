from pydantic import BaseModel


class Armor(BaseModel):
    id: int
    name: str
    defence: float
    stamina_per_turn: float

    class Config:
        orm_mode = True


class Weapon(BaseModel):
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    class Config:
        orm_mode = True


class Equipment(BaseModel):
    weapons: list[Weapon]
    armors: list[Armor]
