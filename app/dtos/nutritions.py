from app.kernel.dto import FromOrmDTO
from pydantic import BaseModel
from datetime import date


class NutritionWeightDTO(BaseModel):
    kcal: float
    protein: float
    carbs: float
    serving_amount: float
    serving_unit: str


class NutritionBaseDTO(NutritionWeightDTO):
    user_id: int
    meal_name: str


class NutritionDTO(FromOrmDTO, NutritionBaseDTO):
    ...


class MealDTO(BaseModel):
    name: str
    kcal: float


class CalculateNutritionDTO(BaseModel):
    nutrition_date: date
    weight: NutritionWeightDTO
    meals: list[MealDTO]