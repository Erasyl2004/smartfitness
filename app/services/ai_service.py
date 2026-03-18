from app.interfaces.services.ai import AiService
from app.interfaces.templates.prompt import PromptTemplate
from app.enums.role import ChatMessageRoleEnum
from app.dtos.chat_messages import ChatMessageDTO, ChatMessageBaseDTO
from app.dtos.nutritions import MealNutritionDTO
from dataclasses import dataclass
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage
)


@dataclass(eq=False)
class AiServiceImpl(AiService):
    model: ChatGoogleGenerativeAI
    prompt_template: PromptTemplate

    def to_lc_messages(self, chat_messages: list[ChatMessageDTO]) -> list[BaseMessage]:
        out: list[BaseMessage] = [SystemMessage(content=self.prompt_template.from_template())]

        for m in chat_messages:
            if m.role == ChatMessageRoleEnum.USER:
                out.append(HumanMessage(content=m.content))
            elif m.role == ChatMessageRoleEnum.FITNESS_ASSISTANT:
                out.append(AIMessage(content=m.content))

        return out

    async def run_fitness_assistant(
        self,
        chat_messages: list[ChatMessageDTO],
    ) -> ChatMessageBaseDTO:
        lc_messages = self.to_lc_messages(chat_messages=chat_messages)
        ai_msg = await self.model.ainvoke(lc_messages)

        return ChatMessageBaseDTO(
            role=ChatMessageRoleEnum.FITNESS_ASSISTANT,
            content=ai_msg.content
        )

    async def process_calories(
        self,
        food_image_url: str
    ) -> MealNutritionDTO:
        calories_prompt = self.prompt_template.from_template_calories()
        structured_model = self.model.with_structured_output(
            schema=MealNutritionDTO,
            method="json_schema"
        )

        human_message = HumanMessage(content=[
            {"type": "text", "text": calories_prompt},
            {"type": "image", "url": food_image_url}
        ])

        return await structured_model.ainvoke([human_message])