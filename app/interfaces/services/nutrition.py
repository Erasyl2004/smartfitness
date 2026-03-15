from app.dtos.nutritions import NutritionDTO, CalculateNutritionDTO
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class NutritionService(ABC):

    @abstractmethod
    async def get_user_week_nutrition(self, user_id: int) -> list[NutritionDTO]:
        ...

    @abstractmethod
    async def calculate_user_nutrition(self, user_id: int) -> list[CalculateNutritionDTO]:
        ...