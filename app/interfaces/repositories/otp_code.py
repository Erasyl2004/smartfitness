from app.interfaces.repositories.crud import BaseRepository
from app.database.entities.otp_codes import OtpCodeEntity
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

@dataclass
class OtpCodeRepository(BaseRepository[OtpCodeEntity], ABC):

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Optional[OtpCodeEntity]:
        ...