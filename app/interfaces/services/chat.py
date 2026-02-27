from app.dtos.chat_messages import ChatMessageBaseDTO, ChatMessageDTO
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ChatMessageService(ABC):

    @abstractmethod
    async def get_all_chat_messages(self, user_id: int) -> list[ChatMessageDTO]:
        ...

    @abstractmethod
    async def save_message(self, user_id: int, message: ChatMessageBaseDTO) -> ChatMessageDTO:
        ...

    @abstractmethod
    async def clear_chat_history(self, user_id: int) -> None:
        ...