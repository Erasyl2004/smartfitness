from app.kernel.dto import FromOrmDTO
from pydantic import BaseModel


class BenefitCreateDTO(BaseModel):
    content: str


class BenefitBaseDTO(BenefitCreateDTO):
    exercise_id: int


class BenefitDTO(FromOrmDTO, BenefitBaseDTO):
    ...