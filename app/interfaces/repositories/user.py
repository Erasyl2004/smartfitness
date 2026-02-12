from app.interfaces.repositories.crud import BaseRepository
from app.database.entities.users import UserEntity
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

@dataclass
class UserRepository(BaseRepository[UserEntity], ABC):

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        ...