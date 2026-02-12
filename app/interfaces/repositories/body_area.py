from app.interfaces.repositories.crud import BaseRepository
from app.database.entities.body_areas import BodyAreaEntity
from dataclasses import dataclass
from abc import ABC

@dataclass
class BodyAreaRepository(BaseRepository[BodyAreaEntity], ABC):
    ...