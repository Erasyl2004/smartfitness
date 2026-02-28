from app.interfaces.services.chat import ChatMessageService
from app.interfaces.services.user import UserService
from app.dtos.chat_messages import ChatMessageDTO, ChatMessageBaseDTO
from app.dtos.users import UserDTO
from app.security.validation import get_current_active_auth_user, get_current_active_auth_user_from_websocket
from dishka.integrations.fastapi import FromDishka, DishkaRoute, inject
from dishka import AsyncContainer
from fastapi import APIRouter, status, Depends, WebSocket, WebSocketDisconnect


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


@router.websocket("/ws/{token}")
@inject
async def chat_websocket(
    websocket: WebSocket,
    container: FromDishka[AsyncContainer],
    token: str
):
    await websocket.accept()
    async with container() as request_container:
        chat_message_service = await request_container.get(ChatMessageService)
        user_service = await request_container.get(UserService)

        user = await get_current_active_auth_user_from_websocket(
            user_service=user_service,
            websocket=websocket,
            token=token
        )

        try:
            while True:
                data = await websocket.receive_json()
                role = data.get("role")

                if role == "USER":
                    content = data.get("content")

                    fitness_assistant_message = await chat_message_service.process_user_message(
                        user_id=user.id,
                        content=content
                    )

                    await websocket.send_json({
                        "role": fitness_assistant_message.role.value,
                        "content": fitness_assistant_message.content
                    })
        except WebSocketDisconnect:
            await websocket.close()
            pass
        except Exception as e:
            await websocket.close()
            raise e