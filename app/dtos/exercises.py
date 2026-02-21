from app.kernel.dto import FromOrmDTO
from typing import Optional
from pydantic import BaseModel, AnyUrl


class ExerciseBaseDTO(BaseModel):
    body_area_id: int
    name: str
    duration: str
    calories: str
    sets: str
    reps: str
    video_url: Optional[AnyUrl]
    image_url: AnyUrl


class BodyAreaExerciseDTO(FromOrmDTO):
    name: str
    image_url: AnyUrl


class ExerciseDTO(FromOrmDTO, ExerciseBaseDTO):
    ...


class ExerciseDetailDTO(ExerciseDTO):
    benefits: list[str]