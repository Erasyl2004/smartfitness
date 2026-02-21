from app.interfaces.services.benefit import BenefitService
from app.interfaces.repositories.benefit import BenefitRepository
from app.dtos.benefits import BenefitCreateDTO, BenefitDTO
from dataclasses import dataclass


@dataclass(eq=False)
class BenefitServiceImpl(BenefitService):
    repo: BenefitRepository

    async def get_all_exercise_benefits(self, exercise_id: int) -> list[BenefitDTO]:
        entities = await self.repo.get_all_by_exercise_id(exercise_id=exercise_id)
        return [BenefitDTO.model_validate(entity) for entity in entities]

    async def save_benefit(self, exercise_id: int, benefit_create: BenefitCreateDTO) -> BenefitDTO:
        entity = await self.repo.create(
            entity_data={
                "content": benefit_create.content,
                "exercise_id": exercise_id
            }
        )

        return BenefitDTO.model_validate(entity)