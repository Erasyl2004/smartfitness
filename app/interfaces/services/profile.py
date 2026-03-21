from app.dtos.profile import UserProfileBaseDTO, UserProfileDTO
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

@dataclass
class UserProfileService(ABC):

    @abstractmethod
    async def get_profile_by_user_id(self, user_id: int) -> Optional[UserProfileBaseDTO]:
        ...

    @abstractmethod
    async def create_profile(self, user_id: int, profile: UserProfileBaseDTO) -> UserProfileDTO:
        ...