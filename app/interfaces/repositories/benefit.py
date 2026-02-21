from app.interfaces.repositories.crud import BaseRepository
from app.database.entities.benefits import ExerciseBenefitEntity
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class BenefitRepository(BaseRepository[ExerciseBenefitEntity], ABC):

    @abstractmethod
    async def get_all_by_exercise_id(self, exercise_id: int) -> list[ExerciseBenefitEntity]:
        ...