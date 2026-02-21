from app.kernel.entity import BaseEntity
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class ExerciseEntity(BaseEntity):
    __tablename__ = "exercises"

    body_area_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("body_areas.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    duration: Mapped[str] = mapped_column(String(50), nullable=False)
    calories: Mapped[str] = mapped_column(String(50), nullable=False)
    sets: Mapped[str] = mapped_column(String(50), nullable=False)
    reps: Mapped[str] = mapped_column(String(50), nullable=False)
    video_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)