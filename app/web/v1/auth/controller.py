from app.interfaces.services.user import UserService
from app.interfaces.services.otp import OtpService
from app.security.tokens import create_access_token, create_refresh_token
from app.dtos.users import CredentialsDTO, UserDTO
from app.dtos.otp_codes import OtpSuccessDTO, OtpValidateDTO, OtpRequestDTO
from app.exceptions.otp import OtpResendTooSoonException, OtpNotFoundException, OtpCodeIsNotValidException
from app.dtos.tokens import TokenDTO
from app.security.validation import (
    get_token_payload_from_header,
    get_current_auth_user_for_refresh,
    get_current_active_auth_user,
    validate_auth_user
)
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Depends, status, HTTPException


router = APIRouter(route_class=DishkaRoute)


@router.post(
    "/register",
    summary="создать user",
    description="создает user-a, отдает otp verification",
    response_model=OtpSuccessDTO,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    payload: CredentialsDTO,
    user_service: FromDishka[UserService],
    otp_service: FromDishka[OtpService]
) -> OtpSuccessDTO:
    user = await user_service.create_user(payload)
    return await otp_service.process_registration_otp(user=user)


@router.post(
    "/register/otp/resend",
    summary="пере отправить новый otp",
    description="по verification_id отправляет новый otp user-у",
    response_model=OtpSuccessDTO,
    status_code=status.HTTP_200_OK
)
async def resend_otp(
    payload: OtpRequestDTO,
    user_service: FromDishka[UserService],
    otp_service: FromDishka[OtpService]
) -> OtpSuccessDTO:
    try:
        otp = await otp_service.get_or_otp_by_id(verification_id=payload.verification_id)
        user = await user_service.get_user_by_id(user_id=otp.user_id)

        return await otp_service.resend_otp_code(user=user, otp=otp)
    except OtpNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'error': str(e)},
        )
    except OtpResendTooSoonException as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={'error': str(e)}
        )


@router.post(
    "/register/otp/confirm",
    summary="подтвердить otp регистраций",
    description="подтверждает otp после регистраций, меняет статус user-a на active, отдает access + refresh",
    response_model=TokenDTO,
    status_code=status.HTTP_200_OK
)
async def confirm_otp(
    payload: OtpValidateDTO,
    user_service: FromDishka[UserService],
    otp_service: FromDishka[OtpService]
) -> TokenDTO:
    try:
        otp = await otp_service.confirm_registration_otp(request=payload)
        activated_user = await user_service.activate_user(user_id=otp.user_id)
    except OtpNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'error': str(e)},
        )
    except OtpCodeIsNotValidException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': str(e)}
        )

    return TokenDTO(
        access_token=create_access_token(activated_user),
        refresh_token=create_refresh_token(activated_user),
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