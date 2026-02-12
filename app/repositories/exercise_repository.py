from app.interfaces.repositories.exercise import ExerciseRepository
from app.database.entities.exercises import ExerciseEntity
from app.kernel.repository import CrudSQLRepository
from sqlalchemy.future import select
from typing import Type
from dataclasses import dataclass

dataclass(eq=False)
class ExerciseRepositoryImpl(
    CrudSQLRepository[ExerciseEntity],
    ExerciseRepository
):
    entity: Type[ExerciseEntity] = ExerciseEntity

    async def get_all_by_body_area_id(self, body_area_id: int) -> list[ExerciseEntity]:
        query = select(ExerciseEntity).where(ExerciseEntity.body_area_id == body_area_id)
        result = await self.session.execute(query)

        records = result.scalars().all()
        return list(records)