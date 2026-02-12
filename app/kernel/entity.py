from app.database.core.base import Base
from datetime import datetime
from sqlalchemy import func, TIMESTAMP, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

class BaseEntity(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, onupdate=func.now(), nullable=True)