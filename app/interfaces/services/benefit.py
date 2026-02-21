from app.dtos.benefits import BenefitCreateDTO, BenefitDTO
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class BenefitService(ABC):

    @abstractmethod
    async def get_all_exercise_benefits(self, exercise_id: int) -> list[BenefitDTO]:
        ...

    @abstractmethod
    async def save_benefit(self, exercise_id: int, benefit_create: BenefitCreateDTO) -> BenefitDTO:
        ...