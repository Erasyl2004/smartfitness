from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class OtpTemplate(ABC):

    @abstractmethod
    def from_template(self, otp_code: str) -> str:
        ...