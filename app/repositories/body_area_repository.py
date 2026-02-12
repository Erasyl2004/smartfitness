from app.interfaces.repositories.body_area import BodyAreaRepository
from app.database.entities.body_areas import BodyAreaEntity
from app.kernel.repository import CrudSQLRepository
from typing import Type
from dataclasses import dataclass

dataclass(eq=False)
class BodyAreaRepositoryImpl(
    CrudSQLRepository[BodyAreaEntity],
    BodyAreaRepository
):
    entity: Type[BodyAreaEntity] = BodyAreaEntity