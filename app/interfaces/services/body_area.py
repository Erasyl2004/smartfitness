from app.dtos.body_areas import BodyAreaBaseDTO, BodyAreaDTO
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional


@dataclass
class BodyAreaService(ABC):
    @abstractmethod
    async def get_body_area_by_id(self, body_area_id: int) -> Optional[BodyAreaDTO]:
        ...

    @abstractmethod
    async def get_all_body_areas(self) -> list[BodyAreaDTO]:
        ...

    @abstractmethod
    async def save_body_area(self, body_area: BodyAreaBaseDTO) -> BodyAreaDTO:
        ...

    @abstractmethod
    async def update_body_area(self, body_area_id: int, update_data: BodyAreaBaseDTO) -> BodyAreaDTO:
        ...

    @abstractmethod
    async def delete_body_area(self, body_area_id: int) -> None:
        ...