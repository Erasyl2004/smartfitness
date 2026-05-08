from app.kernel.dto import FromOrmDTO
from pydantic import BaseModel,Field
from datetime import date
from typing import Optional


class MealNutritionDTO(BaseModel):
    meal_name: str = Field(description="Meal name")
    kcal: float = Field(description="Calories for the detected serving")
    protein: float = Field(description="Protein in grams")
    carbs: float = Field(description="Carbohydrates in grams")
    fat: float = Field(description="Fat in grams")
    serving_amount: float = Field(description="Estimated serving amount in grams")


class NutritionWeightDTO(BaseModel):
    kcal: float
    protein: float
    carbs: float
    fat: float
    serving_amount: float
    serving_unit: str


class NutritionBaseDTO(NutritionWeightDTO):
    user_id: int
    meal_name: str
    food_image_url: Optional[str]


class NutritionDTO(FromOrmDTO, NutritionBaseDTO):
    ...


class MealDTO(BaseModel):
    name: str
    kcal: float


class CalculateNutritionDTO(BaseModel):
    nutrition_date: date
    weight: NutritionWeightDTO
    meals: list[MealDTO]

class CalculateWeekProfileNutritionDTO(BaseModel):
    total_kcal: float = 0.0
    out_of_kcal: float
    total_protein: float = 0.0
    total_carbs: float = 0.0
    total_fats: float = 0.0
    total_serving_amount: float = 0.0