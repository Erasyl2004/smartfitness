from abc import ABC, abstractmethod
from dataclasses import dataclass
from fastapi import UploadFile

@dataclass
class S3Service(ABC):

    @abstractmethod
    def upload_image(self, file: UploadFile) -> dict[str, str]:
        ...

    @abstractmethod
    def _build_public_url(self, object_key: str) -> str:
        ...

    @abstractmethod
    def _get_extension(self, filename: str, content_type: str) -> str:
        ...