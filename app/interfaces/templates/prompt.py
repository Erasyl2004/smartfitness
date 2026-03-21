from app.dtos.profile import UserProfileDTO
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class PromptTemplate(ABC):

    @abstractmethod
    def from_template(self, profile: Optional[UserProfileDTO]) -> str:
        ...

    @abstractmethod
    def from_template_calories(self) -> str:
        ...