from enum import StrEnum, auto

class UserStatusEnum(StrEnum):
    ACTIVE = auto()
    INACTIVE = auto()
    PENDING_VERIFICATION = auto()