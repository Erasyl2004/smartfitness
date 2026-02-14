from app.interfaces.repositories.otp_code import OtpCodeRepository
from app.database.entities.otp_codes import OtpCodeEntity
from app.kernel.repository import CrudSQLRepository
from typing import Type
from dataclasses import dataclass

dataclass(eq=False)
class OtpCodeRepositoryImpl(
    CrudSQLRepository[OtpCodeEntity],
    OtpCodeRepository
):
    entity: Type[OtpCodeEntity] = OtpCodeEntity