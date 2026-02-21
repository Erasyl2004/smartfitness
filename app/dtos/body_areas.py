from app.kernel.dto import FromOrmDTO
from pydantic import BaseModel, AnyUrl


class BodyAreaBaseDTO(BaseModel):
    name: str
    image_url: AnyUrl


class BodyAreaDTO(FromOrmDTO, BodyAreaBaseDTO):
    ...
