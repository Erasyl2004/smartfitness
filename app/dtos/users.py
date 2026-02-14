from app.kernel.dto import FromOrmDTO
from app.enums.user_status import UserStatusEnum
from pydantic import BaseModel, EmailStr


class CredentialsDTO(BaseModel):
    email: EmailStr
    password: str


class UserBaseDTO(BaseModel):
    password: bytes
    email: EmailStr
    status: UserStatusEnum


class UserDTO(FromOrmDTO, UserBaseDTO):
    ...