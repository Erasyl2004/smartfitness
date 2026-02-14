from app.kernel.entity import BaseEntity
from app.enums.otp_purpose import OtpPurposeEnum
from sqlalchemy import BigInteger, ForeignKey, LargeBinary, Enum, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class OtpCodeEntity(BaseEntity):
    __tablename__ = "otp_codes"

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    purpose: Mapped[OtpPurposeEnum] = mapped_column(Enum(OtpPurposeEnum, name="otp_purpose_enum"), nullable=False)
    code_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    resend_available_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)