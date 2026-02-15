from app.dtos.otp_codes import OtpValidateDTO, OtpSuccessDTO, OtpDTO
from app.dtos.users import UserDTO
from dataclasses import dataclass
from abc import abstractmethod, ABC
from typing import Optional
from datetime import datetime

@dataclass
class OtpService(ABC):

    @abstractmethod
    def is_otp_resend_available(self, otp: OtpDTO, now: datetime) -> bool:
        ...

    @abstractmethod
    async def get_or_otp_by_id(self, verification_id: int) -> OtpDTO:
        ...

    @abstractmethod
    async def get_otp_by_user_id(self, user_id: int) -> Optional[OtpDTO]:
        ...

    @abstractmethod
    async def save_registration_otp(self, user_id: int, code: str) -> OtpDTO:
        ...

    @abstractmethod
    async def update_registration_otp_code(self, verification_id: int, code: str) -> OtpDTO:
        ...

    @abstractmethod
    async def send_otp_code(self, receiver_email: str, code: str):
        ...

    @abstractmethod
    async def send_otp_code_by_api(self, receiver_email: str, code: str):
        ...

    @abstractmethod
    async def resend_otp_code(self, user: UserDTO, otp: OtpDTO) -> OtpSuccessDTO:
        ...

    @abstractmethod
    async def process_registration_otp(self, user: UserDTO) -> OtpSuccessDTO:
        ...

    @abstractmethod
    async def validate_and_resend_otp_code(self, user: UserDTO, otp: OtpDTO) -> OtpSuccessDTO:
        ...

    @abstractmethod
    async def confirm_registration_otp(self, request: OtpValidateDTO) -> OtpDTO:
        ...