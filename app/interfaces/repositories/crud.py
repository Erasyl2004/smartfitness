from app.kernel.entity import BaseEntity
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Any
from dataclasses import dataclass

BE = TypeVar("BE", bound=BaseEntity)

@dataclass
class BaseRepository(ABC, Generic[BE]):
    session: AsyncSession

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[BE]:
        ...

    @abstractmethod
    async def get_all(self) -> list[BE]:
        ...

    @abstractmethod
    async def create(self, entity_data: dict[str, Any]) -> BE:
        ...

    @abstractmethod
    async def delete_by_id(self, entity_id: int) -> None:
        ...

    @abstractmethod
    async def update(self, entity_id: int, entity_data: dict[str, Any]) -> BE:
        ...