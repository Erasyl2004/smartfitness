from app.enums.user_status import UserStatusEnum
from app.interfaces.services.user import UserService
from app.security.crypto import decode_jwt, validate_cred
from app.dtos.users import CredentialsDTO, UserDTO
from app.dtos.tokens import RefreshTokenInDTO
from app.security.tokens import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dishka.integrations.fastapi import inject, FromDishka
from jwt import InvalidTokenError
from starlette import status

bearer_scheme = HTTPBearer(auto_error=False)

def get_token_payload(token: str) -> dict:
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'error': f"invalid token error: {e}"}
        )
    return payload

def get_token_payload_from_header(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    return get_token_payload(token=token.credentials if token else None)


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={'error': f"invalid token type {current_token_type!r} expected {token_type!r}"},
    )


class UserGetterFromAccessToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    @inject
    async def __call__(
        self,
        user_service: FromDishka[UserService],
        payload: dict = Depends(get_token_payload_from_header)
    ) -> UserDTO:
        validate_token_type(payload=payload, token_type=self.token_type)

        email: str | None = payload.get("sub")
        if email:
            user = await user_service.get_user_by_email(email=email)

            if user:
                return user

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'error': "token invalid (user not found)"},
        )

class UserGetterFromRefreshToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    @inject
    async def __call__(
        self,
        user_service: FromDishka[UserService],
        refresh_in: RefreshTokenInDTO
    ) -> UserDTO:
        payload = get_token_payload(token=refresh_in.refresh_token)
        validate_token_type(payload=payload, token_type=self.token_type)

        email: str | None = payload.get("sub")
        if email:
            user = await user_service.get_user_by_email(email=email)

            if user:
                if user.status == UserStatusEnum.ACTIVE:
                    return user
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={'error':"user inactive" if user.status == UserStatusEnum.INACTIVE else "need otp verification"}
                )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'error':"token invalid (user not found)"}
        )

get_current_auth_user = UserGetterFromAccessToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromRefreshToken(REFRESH_TOKEN_TYPE)


def get_current_active_auth_user(
    user: UserDTO = Depends(get_current_auth_user),
):
    if user.status == UserStatusEnum.ACTIVE:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={'error':"user inactive" if user.status == UserStatusEnum.INACTIVE else "need otp verification"}
    )

@inject
async def validate_auth_user(
    user_service: FromDishka[UserService],
    payload: CredentialsDTO
) -> UserDTO:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={'error':"invalid email or password"}
    )

    user = await user_service.get_user_by_email(email=str(payload.email))

    if not user:
        raise unauthed_exc

    if not validate_cred(
        cred=payload.password,
        hashed_cred=user.password,
    ):
        raise unauthed_exc

    if user.status != UserStatusEnum.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'error':"user inactive" if user.status == UserStatusEnum.INACTIVE else "need otp verification"}
        )

    return user