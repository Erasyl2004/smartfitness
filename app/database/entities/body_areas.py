from app.kernel.entity import BaseEntity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class BodyAreaEntity(BaseEntity):
    __tablename__ = "body_areas"

    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)