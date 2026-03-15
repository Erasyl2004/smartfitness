from app.interfaces.services.nutrition import NutritionService
from app.dtos.nutritions import NutritionDTO, CalculateNutritionDTO, NutritionWeightDTO, MealDTO
from app.interfaces.repositories.nutrition import NutritionRepository
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(eq=False)
class NutritionServiceImpl(NutritionService):
    repository: NutritionRepository

    async def get_user_week_nutrition(self, user_id: int) -> list[NutritionDTO]:
        now = datetime.now()

        start = datetime.combine((now - timedelta(days=7)).date(), datetime.min.time())
        end = datetime.combine((now + timedelta(days=7)).date(), datetime.max.time())

        entities = await self.repository.get_by_start_and_end_date(
            user_id=user_id,
            start=start,
            end=end
        )

        return [NutritionDTO.model_validate(entity) for entity in entities]

    async def calculate_user_nutrition(self, user_id: int) -> list[CalculateNutritionDTO]:
        week_nutrition = await self.get_user_week_nutrition(user_id=user_id)
        calculated = {}

        for n in week_nutrition:
            nutrition_date = n.created_at.date()

            if nutrition_date not in calculated:
                calculated[nutrition_date] = {
                    "kcal": 0.0,
                    "protein": 0.0,
                    "carbs": 0.0,
                    "serving_amount": 0.0,
                    "serving_unit": n.serving_unit,
                    "meals": [],
                }

            calculated[nutrition_date]["kcal"] += n.kcal
            calculated[nutrition_date]["protein"] += n.protein
            calculated[nutrition_date]["carbs"] += n.carbs
            calculated[nutrition_date]["serving_amount"] += n.serving_amount

            calculated[nutrition_date]["meals"].append(
                MealDTO(
                    name=n.meal_name,
                    kcal=n.kcal,
                )
            )

        result = [
            CalculateNutritionDTO(
                nutrition_date=nutrition_date,
                weight=NutritionWeightDTO(
                    kcal=data["kcal"],
                    protein=data["protein"],
                    carbs=data["carbs"],
                    serving_amount=data["serving_amount"],
                    serving_unit=data["serving_unit"],
                ),
                meals=data["meals"],
            )
            for nutrition_date, data in sorted(calculated.items())
        ]

        return result