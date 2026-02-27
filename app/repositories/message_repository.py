from app.interfaces.repositories.chat_message import ChatMessageRepository
from app.database.entities.messages import ChatMessageEntity
from app.kernel.repository import CrudSQLRepository
from sqlalchemy.future import select
from sqlalchemy import delete
from dataclasses import dataclass
from typing import Type

dataclass(eq=False)
class ChatMessageRepositoryImpl(
    CrudSQLRepository[ChatMessageEntity],
    ChatMessageRepository
):
    entity: Type[ChatMessageEntity] = ChatMessageEntity

    async def get_all_by_user_id(self, user_id: int) -> list[ChatMessageEntity]:
        query = select(ChatMessageEntity).where(ChatMessageEntity.user_id == user_id).order_by(
            ChatMessageEntity.created_at.asc()
        )

        result = (await self.session.execute(query)).scalars().all()
        return list(result)

    async def delete_by_user_id(self, user_id: int) -> None:
        query = delete(ChatMessageEntity).where(ChatMessageEntity.user_id == user_id)
        await self.session.execute(query)