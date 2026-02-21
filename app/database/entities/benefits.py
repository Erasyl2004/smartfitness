from app.kernel.entity import BaseEntity
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class ExerciseBenefitEntity(BaseEntity):
    __tablename__ = "exercise_benefits"

    exercise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("exercises.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(2000), unique=False, nullable=False)