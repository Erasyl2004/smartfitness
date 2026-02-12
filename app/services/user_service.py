from app.interfaces.services.user import UserService
from app.interfaces.repositories.user import UserRepository
from app.security.crypto import hash_password
from app.dtos.users import CredentialsDTO, UserBaseDTO, UserDTO
from dataclasses import dataclass
from typing import Optional

@dataclass(eq=False)
class UserServiceImpl(UserService):
    repo: UserRepository

    async def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        user_entity = await self.repo.get_by_email(email=email)

        if user_entity:
            return UserDTO.model_validate(user_entity)

    async def create_user(self, register_payload: CredentialsDTO) -> UserDTO:
        user_base = UserBaseDTO(
            email=register_payload.email,
            password=hash_password(password=register_payload.password)
        )

        user_entity = await self.repo.create(entity_data=user_base.model_dump())
        return UserDTO.model_validate(user_entity)