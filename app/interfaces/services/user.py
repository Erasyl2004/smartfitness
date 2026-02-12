from app.dtos.users import CredentialsDTO, UserDTO
from dataclasses import dataclass
from typing import Optional
from abc import ABC, abstractmethod

@dataclass
class UserService(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        ...

    @abstractmethod
    async def create_user(self, register_payload: CredentialsDTO) -> UserDTO:
        ...