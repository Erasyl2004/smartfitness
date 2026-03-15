from app.interfaces.repositories.nutrition import NutritionRepository
from app.database.entities.nutritions import NutritionEntity
from app.kernel.repository import CrudSQLRepository
from sqlalchemy.future import select
from datetime import datetime
from dataclasses import dataclass
from typing import Type

dataclass(eq=False)
class NutritionRepositoryImpl(
    NutritionRepository,
    CrudSQLRepository[NutritionEntity],
):
    entity: Type[NutritionEntity] = NutritionEntity

    async def get_by_start_and_end_date(self, user_id: int, start: datetime, end: datetime) -> list[NutritionEntity]:
        stmt = select(NutritionEntity).where(
            NutritionEntity.user_id == user_id,
            NutritionEntity.created_at >= start,
            NutritionEntity.created_at <= end
        ).order_by(NutritionEntity.created_at.asc())

        result = await self.session.execute(stmt)
        rows = result.scalars().all()

        return list(rows)