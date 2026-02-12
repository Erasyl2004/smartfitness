from app.interfaces.repositories.crud import BaseRepository
from app.database.entities.exercises import ExerciseEntity
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class ExerciseRepository(BaseRepository[ExerciseEntity], ABC):

    @abstractmethod
    async def get_all_by_body_area_id(self, body_area_id: int) -> list[ExerciseEntity]:
        ...