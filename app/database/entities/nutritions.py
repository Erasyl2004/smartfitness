from app.kernel.entity import BaseEntity
from sqlalchemy import BigInteger, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column

class NutritionEntity(BaseEntity):
    __tablename__ = "nutritions"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    meal_name: Mapped[str] = mapped_column(String(200), nullable=False)
    kcal: Mapped[float] = mapped_column(Float, nullable=False)
    protein: Mapped[float] = mapped_column(Float, nullable=False)
    carbs: Mapped[float] = mapped_column(Float, nullable=False)
    serving_amount: Mapped[float] = mapped_column(Float, nullable=False)
    serving_unit: Mapped[str] = mapped_column(String(50), nullable=False)