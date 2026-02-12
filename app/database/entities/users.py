from app.kernel.entity import BaseEntity
from sqlalchemy import String, LargeBinary, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class UserEntity(BaseEntity):
    __tablename__ = "users"

    email: Mapped[Optional[str]] = mapped_column(String(200), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)