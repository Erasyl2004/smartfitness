from app.kernel.dto import FromOrmDTO
from pydantic import BaseModel

class BodyAreaBaseDTO(BaseModel):
    name: str
    image_url: str

class BodyAreaDTO(FromOrmDTO, BodyAreaBaseDTO):
    ...
