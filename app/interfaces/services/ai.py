from app.dtos.chat_messages import ChatMessageDTO, ChatMessageBaseDTO
from app.dtos.nutritions import MealNutritionDTO
from dataclasses import dataclass
from langchain_core.messages import BaseMessage
from abc import ABC, abstractmethod


@dataclass
class AiService(ABC):

    @abstractmethod
    async def to_lc_messages(self, user_id: int, chat_messages: list[ChatMessageDTO]) -> list[BaseMessage]:
        ...

    @abstractmethod
    async def run_fitness_assistant(
        self,
        user_id: int,
        chat_messages: list[ChatMessageDTO],
    ) -> ChatMessageBaseDTO:
        ...

    @abstractmethod
    async def process_calories(
        self,
        food_image_url: str
    ) -> MealNutritionDTO:
        ...