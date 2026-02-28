from app.interfaces.services.chat import ChatMessageService
from app.interfaces.services.ai import AiService
from app.interfaces.repositories.chat_message import ChatMessageRepository
from app.enums.role import ChatMessageRoleEnum
from app.dtos.chat_messages import UserChatMessage, ChatMessageBaseDTO, ChatMessageDTO
from dataclasses import dataclass


@dataclass(eq=False)
class ChatMessageServiceImpl(ChatMessageService):
    ai_service: AiService
    repo: ChatMessageRepository

    async def get_all_chat_messages(self, user_id: int) -> list[ChatMessageDTO]:
        entities = await self.repo.get_all_by_user_id(
            user_id=user_id
        )

        return [ChatMessageDTO.model_validate(entity) for entity in entities]

    async def save_message(self, user_id: int, message: ChatMessageBaseDTO) -> ChatMessageDTO:
        user_message = UserChatMessage(
            user_id=user_id,
            content=message.content,
            role=message.role
        )

        entity = await self.repo.create(entity_data=user_message.model_dump(mode="json"))

        return ChatMessageDTO.model_validate(entity)

    async def process_user_message(self, user_id: int, content: str) -> ChatMessageDTO:
        await self.save_message(
            user_id=user_id,
            message=ChatMessageBaseDTO(
                role=ChatMessageRoleEnum.USER,
                content=content
            )
        )
        chat_history = await self.get_all_chat_messages(user_id=user_id)

        assistant_message = await self.ai_service.run_fitness_assistant(
            chat_messages=chat_history
        )

        return await self.save_message(user_id=user_id, message=assistant_message)

    async def clear_chat_history(self, user_id: int) -> None:
        return await self.repo.delete_by_user_id(
            user_id=user_id
        )