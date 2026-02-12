from app.interfaces.templates.otp import OtpTemplate
from aiosmtplib import SMTP
from email.message import EmailMessage
from email.utils import formataddr
from dataclasses import dataclass
from typing import ClassVar

@dataclass(eq=False)
class OtpService:
    otp_template: OtpTemplate
    smtp_client: SMTP

    DEFAULT_TTL_MINUTES: ClassVar[int] = 5
    DEFAULT_OTP_SUBJECT: ClassVar[str] = "Your verification code"

    async def send_otp(self, receiver: str, code: str):
        msg = EmailMessage()
        # msg["From"] = formataddr((self.cfg.from_name, self.cfg.from_email))
        msg["To"] = receiver
        msg["Subject"] = self.DEFAULT_OTP_SUBJECT

        otp_html = self.otp_template.from_template(otp_code=code)
        msg.add_alternative(otp_html, subtype="html")