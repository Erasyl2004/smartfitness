from app.interfaces.services.exercise import ExerciseService
from app.interfaces.services.benefit import BenefitService
from app.interfaces.repositories.exercise import ExerciseRepository
from app.dtos.exercises import ExerciseBaseDTO, ExerciseDTO, BodyAreaExerciseDTO, ExerciseDetailDTO
from app.exceptions.exercise import ExerciseNotFoundException
from dataclasses import dataclass
from pydantic import AnyUrl
from typing import Optional


@dataclass(eq=False)
class ExerciseServiceImpl(ExerciseService):
    benefit_service: BenefitService
    repo: ExerciseRepository

    async def get_exercise_by_id(self, exercise_id: int) -> Optional[ExerciseDTO]:
        entity = await self.repo.get_by_id(entity_id=exercise_id)

        if entity:
            return ExerciseDTO.model_validate(entity)

    async def get_exercise_details_by_id(self, exercise_id: int) -> Optional[ExerciseDetailDTO]:
        exercise = await self.get_exercise_by_id(exercise_id=exercise_id)

        if exercise:
            benefits = await self.benefit_service.get_all_exercise_benefits(
                exercise_id=exercise_id
            )

            return ExerciseDetailDTO(
                **exercise.model_dump(),
                benefits=[benefit.content for benefit in benefits]
            )

    async def get_all_body_area_exercises(self, body_area_id: int) -> list[BodyAreaExerciseDTO]:
        entities = await self.repo.get_all_by_body_area_id(body_area_id=body_area_id)

        return [
            BodyAreaExerciseDTO(
                id=entity.id,
                name=entity.name,
                image_url=AnyUrl(entity.image_url),
                created_at=entity.created_at,
                updated_at=entity.updated_at
            )
            for entity in entities
        ]

    async def save_exercise(self, exercise: ExerciseBaseDTO) -> ExerciseDTO:
        entity = await self.repo.create(entity_data=exercise.model_dump(mode="json"))

        return ExerciseDTO.model_validate(entity)

    async def update_exercise(self, exercise_id: int, update_data: ExerciseBaseDTO) -> ExerciseDTO:
        exercise = await self.get_exercise_by_id(exercise_id=exercise_id)

        if not exercise:
            raise ExerciseNotFoundException(exercise_id=exercise_id)

        updated_entity = await self.repo.update(
            entity_id=exercise_id,
            entity_data=update_data.model_dump()
        )

        return ExerciseDTO.model_validate(updated_entity)

    async def delete_exercise(self, exercise_id: int) -> None:
        exercise = await self.get_exercise_by_id(exercise_id=exercise_id)

        if not exercise:
            raise ExerciseNotFoundException(exercise_id=exercise_id)

        await self.repo.delete_by_id(entity_id=exercise_id)