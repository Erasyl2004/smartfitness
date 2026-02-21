from app.dtos.exercises import ExerciseBaseDTO, ExerciseDTO, BodyAreaExerciseDTO, ExerciseDetailDTO
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional


@dataclass
class ExerciseService(ABC):

    @abstractmethod
    async def get_exercise_by_id(self, exercise_id: int) -> Optional[ExerciseDTO]:
        ...

    @abstractmethod
    async def get_exercise_details_by_id(self, exercise_id: int) -> Optional[ExerciseDetailDTO]:
        ...

    @abstractmethod
    async def get_all_body_area_exercises(self, body_area_id: int) -> list[BodyAreaExerciseDTO]:
        ...

    @abstractmethod
    async def save_exercise(self, exercise: ExerciseBaseDTO) -> ExerciseDTO:
        ...

    @abstractmethod
    async def update_exercise(self, exercise_id: int, update_data: ExerciseBaseDTO) -> ExerciseDTO:
        ...

    @abstractmethod
    async def delete_exercise(self, exercise_id: int) -> None:
        ...