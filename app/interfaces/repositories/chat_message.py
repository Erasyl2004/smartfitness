from app.interfaces.repositories.crud import BaseRepository
from app.database.entities.messages import ChatMessageEntity
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class ChatMessageRepository(BaseRepository[ChatMessageEntity], ABC):

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> list[ChatMessageEntity]:
        ...

    @abstractmethod
    async def delete_by_user_id(self, user_id: int) -> None:
        ...