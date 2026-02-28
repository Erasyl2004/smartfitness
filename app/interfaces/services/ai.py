from app.dtos.chat_messages import ChatMessageDTO, ChatMessageBaseDTO
from dataclasses import dataclass
from langchain_core.messages import BaseMessage
from abc import ABC, abstractmethod


@dataclass
class AiService(ABC):

    @abstractmethod
    def to_lc_messages(self, chat_messages: list[ChatMessageDTO]) -> list[BaseMessage]:
        ...

    @abstractmethod
    async def run_fitness_assistant(
        self,
        chat_messages: list[ChatMessageDTO],
    ) -> ChatMessageBaseDTO:
        ...