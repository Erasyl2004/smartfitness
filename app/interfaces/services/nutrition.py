from app.dtos.nutritions import NutritionDTO, CalculateNutritionDTO, CalculateWeekProfileNutritionDTO
from dataclasses import dataclass
from abc import ABC, abstractmethod
from fastapi import UploadFile


@dataclass
class NutritionService(ABC):

    @abstractmethod
    async def get_user_week_nutrition(self, user_id: int) -> list[NutritionDTO]:
        ...

    @abstractmethod
    async def calculate_user_nutrition(self, user_id: int) -> list[CalculateNutritionDTO]:
        ...

    @abstractmethod
    async def get_user_week_profile_nutrition(self, user_id: int) -> CalculateWeekProfileNutritionDTO:
        ...

    @abstractmethod
    async def recognize_nutrition_by_photo(self, user_id: int, photo: UploadFile) -> NutritionDTO:
        ...