from app.interfaces.repositories.otp_code import OtpCodeRepository
from app.database.entities.otp_codes import OtpCodeEntity
from app.kernel.repository import CrudSQLRepository
from sqlalchemy import select
from typing import Type, Optional
from dataclasses import dataclass

dataclass(eq=False)
class OtpCodeRepositoryImpl(
    CrudSQLRepository[OtpCodeEntity],
    OtpCodeRepository
):
    entity: Type[OtpCodeEntity] = OtpCodeEntity

    async def get_by_user_id(self, user_id: int) -> Optional[OtpCodeEntity]:
        query = (
            select(self.entity).where(self.entity.user_id == user_id)
        )

        result = await self.session.execute(query)
        record = result.scalar_one_or_none()

        return record