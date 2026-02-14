from app.interfaces.services.otp import OtpService
from app.interfaces.repositories.otp_code import OtpCodeRepository
from app.interfaces.templates.otp import OtpTemplate
from app.enums.otp_purpose import OtpPurposeEnum
from app.security.crypto import hash_cred, validate_cred
from app.utils.otp import generate_code
from app.web.settings import OtpSettings
from app.dtos.otp_codes import OtpValidateDTO, OtpSuccessDTO, OtpCodeBaseDTO, OtpDTO
from app.dtos.users import UserDTO
from app.exceptions.otp import (
    OtpNotFoundException,
    OtpResendTooSoonException,
    OtpCodeIsNotValidException
)
from email.message import EmailMessage
from dataclasses import dataclass
from datetime import datetime, timedelta
from ssl import SSLContext
from typing import ClassVar
import aiosmtplib
import httpx


@dataclass(eq=False)
class OtpServiceImpl(OtpService):
    repo: OtpCodeRepository
    otp_template: OtpTemplate
    otp_settings: OtpSettings
    tls_context: SSLContext

    BREVO_URL: ClassVar[str] = "https://api.brevo.com/v3/smtp/email"
    DEFAULT_BREVO_TIMEOUT: ClassVar[int] = 60
    DEFAULT_TTL_MINUTES: ClassVar[int] = 5
    DEFAULT_OTP_SUBJECT: ClassVar[str] = "Your verification code"
    GMAIL_HOST: ClassVar[str] = "smtp.gmail.com"
    PORT: ClassVar[int] = 587
    TIMEOUT: ClassVar[int] = 30
    DEFAULT_RESEND_DURATION: ClassVar[timedelta] = timedelta(minutes=2)

    async def get_or_otp_by_id(self, verification_id: int) -> OtpDTO:
        otp_entity = await self.repo.get_by_id(entity_id=verification_id)

        if not otp_entity:
            raise OtpNotFoundException(verification_id=verification_id)

        return OtpDTO.model_validate(otp_entity)

    async def save_registration_otp(self, user_id: int, code: str) -> OtpDTO:
        base = OtpCodeBaseDTO(
            user_id=user_id,
            purpose=OtpPurposeEnum.REGISTER,
            code_hash=hash_cred(cred=code),
            resend_available_at=datetime.now() + self.DEFAULT_RESEND_DURATION
        )

        otp_entity = await self.repo.create(entity_data=base.model_dump())
        return OtpDTO.model_validate(otp_entity)

    async def update_registration_otp_code(self, verification_id: int, code: str) -> OtpDTO:
        otp_entity = await self.repo.update(
            entity_id=verification_id,
            entity_data={
                "code_hash": hash_cred(cred=code),
                "resend_available_at": datetime.now() + self.DEFAULT_RESEND_DURATION
            }
        )

        return OtpDTO.model_validate(otp_entity)

    async def send_otp_code(self, receiver_email: str, code: str):
        msg = EmailMessage()
        msg["From"] = self.otp_settings.gmail_user
        msg["To"] = receiver_email
        msg["Subject"] = self.DEFAULT_OTP_SUBJECT

        otp_html = self.otp_template.from_template(otp_code=code)
        msg.add_alternative(otp_html, subtype="html")

        await aiosmtplib.send(
            msg,
            hostname=self.GMAIL_HOST,
            port=self.PORT,
            start_tls=True,
            username=self.otp_settings.gmail_user,
            password=self.otp_settings.gmail_app_password,
            timeout=self.TIMEOUT,
            tls_context=self.tls_context
        )

    async def send_otp_code_by_api(self, receiver_email: str, code: str):
        otp_html = self.otp_template.from_template(otp_code=code)

        payload = {
            "sender": {"name": self.otp_settings.gmail_name, "email": self.otp_settings.gmail_user},
            "to": [{"email": receiver_email}],
            "subject": self.DEFAULT_OTP_SUBJECT,
            "htmlContent": otp_html
        }
        headers = {
            "accept": "application/json",
            "api-key": self.otp_settings.brevo_api_key,
            "content-type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.DEFAULT_BREVO_TIMEOUT) as client:
            await client.post(self.BREVO_URL, json=payload, headers=headers)

    async def process_registration_otp(self, user: UserDTO) -> OtpSuccessDTO:
        code = generate_code()

        otp = await self.save_registration_otp(
            user_id=user.id,
            code=code
        )
        await self.send_otp_code_by_api(
            receiver_email=str(user.email),
            code=code
        )

        return OtpSuccessDTO(
            verification_id=otp.id
        )

    async def resend_otp_code(self, user: UserDTO, otp: OtpDTO) -> OtpSuccessDTO:
        now = datetime.now()

        if otp.resend_available_at > now:
            retry_after = int((otp.resend_available_at - now).total_seconds())
            raise OtpResendTooSoonException(retry_after=retry_after)

        new_code = generate_code()
        otp = await self.update_registration_otp_code(
            verification_id=otp.id,
            code=new_code
        )

        await self.send_otp_code_by_api(
            receiver_email=str(user.email),
            code=new_code
        )

        return OtpSuccessDTO(
            verification_id=otp.id
        )

    async def confirm_registration_otp(self, request: OtpValidateDTO) -> OtpDTO:
        otp = await self.get_or_otp_by_id(verification_id=request.verification_id)

        if not validate_cred(cred=request.code, hashed_cred=otp.code_hash):
            raise OtpCodeIsNotValidException(
                otp_code=request.code
            )

        return otp