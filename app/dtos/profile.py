from app.kernel.dto import FromOrmDTO
from app.enums.activity import UserPhysicalActivityEnum
from app.enums.gender import UserGenderEnum
from app.enums.goal import UserGoalEnum
from pydantic import BaseModel


class UserProfileBaseDTO(BaseModel):
    age: int
    height: int
    weight: int
    gender: UserGenderEnum
    activity_level: UserPhysicalActivityEnum
    goal: UserGoalEnum


class UserProfileDTO(FromOrmDTO, UserProfileBaseDTO):
    user_id: int
    ...