from app.kernel.entity import BaseEntity
from app.enums.activity import UserPhysicalActivityEnum
from app.enums.gender import UserGenderEnum
from app.enums.goal import UserGoalEnum
from sqlalchemy import BigInteger, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column


class UserProfileEntity(BaseEntity):
    __tablename__ = "user_profiles"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    age: Mapped[int] = mapped_column(BigInteger, nullable=False)
    height: Mapped[int] = mapped_column(BigInteger, nullable=False)
    weight: Mapped[int] = mapped_column(BigInteger, nullable=False)
    gender: Mapped[UserGenderEnum] = mapped_column(
        Enum(UserGenderEnum, name="user_gender_enum"), nullable=False
    )
    activity_level: Mapped[UserPhysicalActivityEnum] = mapped_column(
        Enum(UserPhysicalActivityEnum, name="user_activity_level_enum"), nullable=False
    )
    goal: Mapped[UserGoalEnum] = mapped_column(
        Enum(UserGoalEnum, name="user_goal_enum"), nullable=False
    )