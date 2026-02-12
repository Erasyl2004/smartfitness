from app.security.tokens import create_access_token, create_refresh_token
from app.interfaces.services.user import UserService
from app.dtos.users import CredentialsDTO, UserDTO
from app.dtos.tokens import TokenDTO
from app.security.validation import (
    get_token_payload_from_header,
    get_current_auth_user_for_refresh,
    get_current_active_auth_user,
    validate_auth_user
)
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Depends, status


router = APIRouter(route_class=DishkaRoute)


@router.post(
    "/register",
    summary="создать user",
    description="создает user-a, возвращает access + refresh",
    response_model=TokenDTO,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    payload: CredentialsDTO,
    user_service: FromDishka[UserService],
) -> TokenDTO:
    user = await user_service.create_user(payload)

    return TokenDTO(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
    )


@router.post(
    "/login",
    summary="аутентификация user",
    description="аутентифицирует user-a, возвращает access + refresh",
    response_model=TokenDTO
)
def login_user(
    user: UserDTO = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenDTO(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/refresh",
    summary="рефреш access token",
    description="по refresh, дает новый access",
    response_model=TokenDTO,
    response_model_exclude_none=True,
)
def refresh_user(
    user: UserDTO = Depends(get_current_auth_user_for_refresh)
):
    access_token = create_access_token(user)
    return TokenDTO(
        access_token=access_token,
    )


@router.get(
    "/me",
    summary="получить current user",
    description="по access из bearer, дает current user",
)
def get_me(
    payload: dict = Depends(get_token_payload_from_header),
    user: UserDTO = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "email": user.email,
        "logged_in_at": iat
    }