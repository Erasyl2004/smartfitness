from app.interfaces.repositories.crud import BaseRepository
from app.database.entities.profile import UserProfileEntity
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

@dataclass
class UserProfileRepository(BaseRepository[UserProfileEntity], ABC):

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[UserProfileEntity]:
        ...