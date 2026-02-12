from app.interfaces.services.body_area import BodyAreaService
from app.interfaces.repositories.body_area import BodyAreaRepository
from app.dtos.body_areas import BodyAreaBaseDTO, BodyAreaDTO
from app.exceptions.body_area import BodyAreaNotFoundException
from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False)
class BodyAreaServiceImpl(BodyAreaService):
    repo: BodyAreaRepository

    async def get_body_area_by_id(self, body_area_id: int) -> Optional[BodyAreaDTO]:
        entity = await self.repo.get_by_id(entity_id=body_area_id)

        if entity:
            return BodyAreaDTO.model_validate(entity)

    async def get_all_body_areas(self) -> list[BodyAreaDTO]:
        entities = await self.repo.get_all()

        return [BodyAreaDTO.model_validate(entity) for entity in entities]

    async def save_body_area(self, body_area: BodyAreaBaseDTO) -> BodyAreaDTO:
        entity = await self.repo.create(entity_data=body_area.model_dump())

        return BodyAreaDTO.model_validate(entity)

    async def update_body_area(self, body_area_id: int, update_data: BodyAreaBaseDTO) -> BodyAreaDTO:
        body_area = await self.get_body_area_by_id(body_area_id=body_area_id)

        if not body_area:
            raise BodyAreaNotFoundException(body_area_id=body_area_id)

        updated_entity = await self.repo.update(
            entity_id=body_area_id,
            entity_data=update_data.model_dump()
        )

        return BodyAreaDTO.model_validate(updated_entity)

    async def delete_body_area(self, body_area_id: int) -> None:
        body_area = await self.repo.get_by_id(entity_id=body_area_id)

        if not body_area:
            raise BodyAreaNotFoundException(body_area_id=body_area_id)

        await self.repo.delete_by_id(entity_id=body_area_id)