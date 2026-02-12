from app.kernel.dto import FromOrmDTO
from pydantic import BaseModel, EmailStr

class CredentialsDTO(BaseModel):
    email: EmailStr
    password: str

class UserBaseDTO(BaseModel):
    password: bytes
    email: EmailStr
    active: bool = True

class UserDTO(FromOrmDTO, UserBaseDTO):
    ...