from app.interfaces.services.user import UserService
from app.interfaces.repositories.user import UserRepository
from app.exceptions.user import UserAlreadyExistsException
from app.security.crypto import hash_cred
from app.dtos.users import CredentialsDTO, UserBaseDTO, UserDTO
from app.enums.user_status import UserStatusEnum
from dataclasses import dataclass
from typing import Optional

@dataclass(eq=False)
class UserServiceImpl(UserService):
    repo: UserRepository

    async def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        user_entity = await self.repo.get_by_email(email=email)

        if user_entity:
            return UserDTO.model_validate(user_entity)

    async def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        user_entity = await self.repo.get_by_id(entity_id=user_id)

        if user_entity:
            return UserDTO.model_validate(user_entity)

    async def create_user(self, register_payload: CredentialsDTO) -> UserDTO:
        is_user_exists = await self.get_user_by_email(email=str(register_payload.email))

        if is_user_exists:
            raise UserAlreadyExistsException(email=str(register_payload.email))

        user_base = UserBaseDTO(
            email=register_payload.email,
            password=hash_cred(cred=register_payload.password),
            status=UserStatusEnum.PENDING_VERIFICATION
        )

        user_entity = await self.repo.create(entity_data=user_base.model_dump())
        return UserDTO.model_validate(user_entity)

    async def activate_user(self, user_id: int) -> UserDTO:
        user_entity = await self.repo.update(
            entity_id=user_id,
            entity_data={
                "status": UserStatusEnum.ACTIVE
            }
        )

        return UserDTO.model_validate(user_entity)