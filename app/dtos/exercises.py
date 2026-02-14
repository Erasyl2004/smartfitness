from app.kernel.dto import FromOrmDTO
from typing import Optional
from pydantic import BaseModel


class ExerciseBaseDTO(BaseModel):
    body_area_id: int
    name: str
    description: str
    video_url: Optional[str]


class ExerciseDTO(FromOrmDTO, ExerciseBaseDTO):
    ...