from app.enums.role import ChatMessageRoleEnum
from app.kernel.dto import FromOrmDTO
from pydantic import BaseModel


class ChatMessageBaseDTO(BaseModel):
    role: ChatMessageRoleEnum
    content: str

class UserChatMessage(ChatMessageBaseDTO):
    user_id: int

class ChatMessageDTO(FromOrmDTO, UserChatMessage):
    ...
