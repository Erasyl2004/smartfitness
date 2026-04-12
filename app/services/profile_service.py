from app.interfaces.services.profile import UserProfileService
from app.interfaces.services.nutrition import NutritionService
from app.interfaces.repositories.profile import UserProfileRepository
from app.dtos.profile import UserProfileBaseDTO, UserProfileDTO, UserWeekProfileDTO
from app.dtos.users import UserDTO
from app.exceptions.profile import UserProfileAlreadyExistsException
from dataclasses import dataclass
from typing import Optional

@dataclass(eq=False)
class UserProfileServiceImpl(UserProfileService):
    nutrition_service: NutritionService
    repo: UserProfileRepository

    async def get_profile_by_user_id(self, user_id: int) -> Optional[UserProfileDTO]:
        entity = await self.repo.get_by_user_id(
            user_id=user_id
        )

        if entity:
            return UserProfileDTO.model_validate(entity)

    async def create_profile(self, user_id: int, profile: UserProfileBaseDTO) -> UserProfileDTO:
        exists_profile = await self.get_profile_by_user_id(user_id=user_id)

        if exists_profile:
            raise UserProfileAlreadyExistsException()

        profile_entity = await self.repo.create(
            entity_data={
                **profile.model_dump(),
                "user_id": user_id
            }
        )

        return UserProfileDTO.model_validate(profile_entity)

    async def get_user_week_nutrition_profile(self, user: UserDTO) -> UserWeekProfileDTO:
        week_nutrition = await self.nutrition_service.get_user_week_profile_nutrition(
            user_id=user.id
        )
        user_profile = await self.get_profile_by_user_id(user_id=user.id)

        return UserWeekProfileDTO(
            user_email=str(user.email),
            height=user_profile.height,
            weight=user_profile.weight,
            week_nutrition=week_nutrition
        )