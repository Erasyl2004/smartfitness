from app.kernel.entity import BaseEntity
from app.enums.user_status import UserStatusEnum
from sqlalchemy import String, LargeBinary, Enum
from sqlalchemy.orm import Mapped, mapped_column

class UserEntity(BaseEntity):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    status: Mapped[UserStatusEnum] = mapped_column(Enum(UserStatusEnum, name="user_status_enum"), nullable=False)