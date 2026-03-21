from app.enums.user_status import UserStatusEnum
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
    async def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        ...

    @abstractmethod
    async def create_user(self, register_payload: CredentialsDTO) -> UserDTO:
        ...

    @abstractmethod
    async def update_status(self, user_id: int, status: UserStatusEnum) -> UserDTO:
        ...