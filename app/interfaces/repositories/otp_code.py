from app.interfaces.repositories.crud import BaseRepository
from app.database.entities.otp_codes import OtpCodeEntity
from dataclasses import dataclass
from abc import ABC

@dataclass
class OtpCodeRepository(BaseRepository[OtpCodeEntity], ABC):
    ...