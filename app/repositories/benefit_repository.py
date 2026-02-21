from app.interfaces.repositories.benefit import BenefitRepository
from app.database.entities.benefits import ExerciseBenefitEntity
from app.kernel.repository import CrudSQLRepository
from sqlalchemy.future import select
from typing import Type
from dataclasses import dataclass

dataclass(eq=False)
class BenefitRepositoryImpl(
    CrudSQLRepository[ExerciseBenefitEntity],
    BenefitRepository
):
    entity: Type[ExerciseBenefitEntity] = ExerciseBenefitEntity

    async def get_all_by_exercise_id(self, exercise_id: int) -> list[ExerciseBenefitEntity]:
        query = select(ExerciseBenefitEntity).where(ExerciseBenefitEntity.exercise_id == exercise_id)
        result = await self.session.execute(query)

        return list(result.scalars().all())