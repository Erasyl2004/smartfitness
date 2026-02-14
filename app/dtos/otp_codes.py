from app.kernel.dto import FromOrmDTO
from app.enums.otp_purpose import OtpPurposeEnum
from pydantic import BaseModel
from datetime import datetime


class OtpRequestDTO(BaseModel):
    verification_id: int


class OtpValidateDTO(OtpRequestDTO):
    code: str


class OtpSuccessDTO(BaseModel):
    verification_id: int
    resend_in: int = 120


class OtpCodeBaseDTO(BaseModel):
    user_id: int
    purpose: OtpPurposeEnum
    code_hash: bytes
    resend_available_at: datetime


class OtpDTO(FromOrmDTO, OtpCodeBaseDTO):
    ...