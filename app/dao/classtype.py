from .base_dao import BaseDAO
from .models.classtype import ClassTypeModel


class ClassTypeDAO(BaseDAO[ClassTypeModel]):
    __model__ = ClassTypeModel
