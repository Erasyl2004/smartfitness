from app.enums.user_status import UserStatusEnum

class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        super().__init__(f'User with this email {email} already exists')


def get_user_status_error(status: UserStatusEnum) -> str:
    if status == UserStatusEnum.INACTIVE:
        return "user inactive"
    elif status == UserStatusEnum.PENDING_VERIFICATION:
        return "need otp verification"
    else:
        return "need onbording"