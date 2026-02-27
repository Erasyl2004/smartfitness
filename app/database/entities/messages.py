from app.kernel.entity import BaseEntity
from app.enums.role import ChatMessageRoleEnum
from sqlalchemy import BigInteger, ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

class ChatMessageEntity(BaseEntity):
    __tablename__ = "chat_messages"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    role: Mapped[ChatMessageRoleEnum] = mapped_column(Enum(ChatMessageRoleEnum, name="chat_message_role_enum"), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)