from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Query, scoped_session

from .models.basemodel import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseDAO(Generic[T]):
    __model__ = T

    def __init__(self, session: scoped_session):
        self.session = session

    def get_one(self, uid: int) -> T | None:
        return self.session.get(self.__model__, uid)

    def get_all(self) -> list[T]:
        stmt: Query = self.session.execute(select(self.__model__)).scalars()
        return stmt.all()

    def create(self, entity_data: dict) -> T:
        entity = self.__model__(**entity_data)
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        return entity

    def delete(self, uid) -> T | None:
        entity = self.get_one(uid)

        self.session.delete(entity)
        self.session.commit()
        return entity
