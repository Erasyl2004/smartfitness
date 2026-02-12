from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, ClassVar, Any

class FromOrmDTO(BaseModel):
    id: int

    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class HashableDto(BaseModel):
    __hash_fields__: ClassVar[tuple[str, ...]] = ()

    model_config = ConfigDict(frozen=True)

    def __hash_key__(self) -> tuple[Any, ...]:
        return tuple(getattr(self, name) for name in self.__hash_fields__)

    def __hash__(self) -> int:
        return hash((self.__class__, self.__hash_key__()))

    def __eq__(self, other: Any) -> bool:
        return self.__hash_key__() == other.__hash_key__()