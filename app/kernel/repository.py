from app.interfaces.repositories.crud import (
    BaseRepository, BE
)
from sqlalchemy import select, delete, update
from typing import Optional, Type, Any
from dataclasses import dataclass

@dataclass
class CrudSQLRepository(BaseRepository[BE]):
    entity: Type[BE]

    async def get_by_id(self, entity_id: int) -> Optional[BE]:
        query = (
            select(self.entity).where(self.entity.id == entity_id)
        )

        result = await self.session.execute(query)
        record = result.scalar_one_or_none()

        return record

    async def get_all(self) -> list[BE]:
        query = select(self.entity)

        result = await self.session.execute(query)
        record = result.scalars().all()

        return list(record)

    async def create(self, entity_data: dict[str, Any]) -> BE:
        message_entity = self.entity(**entity_data)
        self.session.add(message_entity)

        await self.session.flush()
        await self.session.refresh(message_entity)

        return message_entity

    async def delete_by_id(self, entity_id: int) -> None:
        query = (
            delete(self.entity).where(self.entity.id == entity_id)
        )

        await self.session.execute(query)

    async def update(self, entity_id: int, entity_data: dict[str, Any]) -> BE:
        query = (
            update(self.entity)
            .where(self.entity.id == entity_id)
            .values(**entity_data)
            .returning(self.entity)
        )

        result = await self.session.execute(query)
        record = result.scalar_one_or_none()

        return record