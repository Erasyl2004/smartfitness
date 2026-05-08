from app.interfaces.services.nutrition import NutritionService
from app.interfaces.services.s3 import S3Service
from app.interfaces.services.ai import AiService
from app.interfaces.repositories.nutrition import NutritionRepository
from app.dtos.nutritions import (
    NutritionBaseDTO, NutritionDTO, CalculateNutritionDTO, NutritionWeightDTO, MealDTO, CalculateWeekProfileNutritionDTO
)
from app.dtos.profile import UserProfileDTO
from app.enums.gender import UserGenderEnum
from app.enums.activity import UserPhysicalActivityEnum
from app.enums.goal import UserGoalEnum
from app.exceptions.nutrition import UnprocessableNutritionException
from dataclasses import dataclass
from typing import ClassVar
from datetime import datetime, timedelta
from fastapi import UploadFile

@dataclass(eq=False)
class NutritionServiceImpl(NutritionService):
    s3_service: S3Service
    ai_service: AiService
    repository: NutritionRepository

    activity_map: ClassVar[dict[UserPhysicalActivityEnum, float]] = {
        UserPhysicalActivityEnum.BEGINNER: 1.375,
        UserPhysicalActivityEnum.INTERMEDIATE: 1.55,
        UserPhysicalActivityEnum.ADVANCED: 1.725
    }
    goal_map: ClassVar[dict[UserGoalEnum, float]] = {
        UserGoalEnum.LOOSE_WEIGHT: 0.85,
        UserGoalEnum.BUILD_MUSCLE: 1.10,
        UserGoalEnum.STAY_FIT: 1.0,
        UserGoalEnum.IMPROVE_FLEXIBILITY: 1.0
    }

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
                    "fat": 0.0,
                    "serving_unit": n.serving_unit,
                    "meals": [],
                }

            calculated[nutrition_date]["kcal"] += n.kcal
            calculated[nutrition_date]["protein"] += n.protein
            calculated[nutrition_date]["carbs"] += n.carbs
            calculated[nutrition_date]["fat"] += n.fat
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
                    fat=data["fat"],
                    serving_amount=data["serving_amount"],
                    serving_unit=data["serving_unit"],
                ),
                meals=data["meals"],
            )
            for nutrition_date, data in sorted(calculated.items())
        ]

        return result

    def calculate_user_week_out_of_calories(self, user_profile: UserProfileDTO) -> float:
        if user_profile.gender == UserGenderEnum.MALE:
            bmr = 10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age + 5
        else:
            bmr = 10 * user_profile.weight + 6.25 * user_profile.height - 5 * user_profile.age - 161

        activity_multiplier = self.activity_map[user_profile.activity_level]
        tdee = bmr * activity_multiplier

        goal_multiplier = self.goal_map[user_profile.goal]
        daily_calories = tdee * goal_multiplier

        weekly_calories = daily_calories * 7
        return round(weekly_calories / 100) * 100

    async def get_user_week_profile_nutrition(self, user_id: int, user_profile: UserProfileDTO) -> CalculateWeekProfileNutritionDTO:
        week_nutrition = await self.calculate_user_nutrition(user_id=user_id)
        weekly_calories_out_of = self.calculate_user_week_out_of_calories(user_profile=user_profile)

        profile_nutrition = CalculateWeekProfileNutritionDTO(out_of_kcal=weekly_calories_out_of)

        for n in week_nutrition:
            profile_nutrition.total_kcal += n.weight.kcal
            profile_nutrition.total_protein += n.weight.protein
            profile_nutrition.total_carbs += n.weight.carbs
            profile_nutrition.total_fats += n.weight.fat
            profile_nutrition.total_serving_amount += n.weight.serving_amount

        return profile_nutrition

    async def recognize_nutrition_by_photo(self, user_id: int, photo: UploadFile) -> NutritionDTO:
        file_data = self.s3_service.upload_image(file=photo)
        extracted_data = await self.ai_service.process_calories(food_image_url=file_data["file_url"])

        if extracted_data.meal_name:
            base = NutritionBaseDTO(
                user_id=user_id,
                meal_name=extracted_data.meal_name,
                kcal=extracted_data.kcal,
                protein=extracted_data.protein,
                carbs=extracted_data.carbs,
                fat=extracted_data.fat,
                serving_amount=extracted_data.serving_amount,
                food_image_url=file_data["file_url"],
                serving_unit="g"
            )
            entity = await self.repository.create(
                entity_data=base.model_dump()
            )

            return NutritionDTO.model_validate(entity)

        raise UnprocessableNutritionException()