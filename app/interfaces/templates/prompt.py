from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PromptTemplate(ABC):

    @abstractmethod
    def from_template(self) -> str:
        ...