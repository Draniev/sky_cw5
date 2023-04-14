from typing import TypeVar

from .dao.models.basemodel import BaseModel

T = TypeVar('T', bound=BaseModel)


def names_list(items: list[T]) -> list[str]:
    names = []
    for item in items:
        names.append(item.name)
    return names
