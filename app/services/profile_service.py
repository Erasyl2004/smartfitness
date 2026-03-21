from app.interfaces.services.profile import UserProfileService
from app.interfaces.repositories.profile import UserProfileRepository
from app.dtos.profile import UserProfileBaseDTO, UserProfileDTO
from app.exceptions.profile import UserProfileAlreadyExistsException
from dataclasses import dataclass
from typing import Optional

@dataclass(eq=False)
class UserProfileServiceImpl(UserProfileService):
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