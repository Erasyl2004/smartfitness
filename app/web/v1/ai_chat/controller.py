from app.interfaces.services.chat import ChatMessageService
from app.dtos.chat_messages import ChatMessageDTO, ChatMessageBaseDTO
from app.dtos.users import UserDTO
from app.security.validation import get_current_active_auth_user
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, status, Depends


router = APIRouter(route_class=DishkaRoute)


@router.post(
    "/test",
    status_code=status.HTTP_201_CREATED,
    summary="Создать chat message",
    description="Создает сообщение по текущему user, временное решение",
    response_model=ChatMessageDTO
)
async def create_chat_message(
    payload: ChatMessageBaseDTO,
    chat_message_service: FromDishka[ChatMessageService],
    user: UserDTO = Depends(get_current_active_auth_user),
) -> ChatMessageDTO:
    return await chat_message_service.save_message(user_id=user.id, message=payload)


@router.get(
    "/history",
    status_code=status.HTTP_200_OK,
    summary="Получить chat history",
    description="Возвращает историю chat messages по текущему user",
    response_model=list[ChatMessageDTO]
)
async def get_chat_history(
    chat_message_service: FromDishka[ChatMessageService],
    user: UserDTO = Depends(get_current_active_auth_user),
) -> list[ChatMessageDTO]:
    return await chat_message_service.get_all_chat_messages(
        user_id=user.id
    )


@router.delete(
    "/history",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить chat history",
    description="Чистит историю chat messages по текущему user",
)
async def delete_chat_history(
    chat_message_service: FromDishka[ChatMessageService],
    user: UserDTO = Depends(get_current_active_auth_user),
) -> None:
    await chat_message_service.clear_chat_history(user_id=user.id)