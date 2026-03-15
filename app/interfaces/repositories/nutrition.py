from app.interfaces.repositories.crud import BaseRepository
from app.database.entities.nutritions import NutritionEntity
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime

@dataclass
class NutritionRepository(BaseRepository[NutritionEntity], ABC):

    @abstractmethod
    async def get_by_start_and_end_date(self, user_id: int, start: datetime, end: datetime) -> list[NutritionEntity]:
        ...