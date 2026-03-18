from app.interfaces.services.s3 import S3Service
from app.web.settings import S3Settings
from botocore.client import BaseClient
from fastapi import UploadFile
from dataclasses import dataclass
import mimetypes
import uuid


@dataclass(eq=False)
class S3ServiceImpl(S3Service):
    client: BaseClient
    config: S3Settings

    def upload_image(self, file: UploadFile) -> dict[str, str]:
        file_id = str(uuid.uuid4())

        ext = self._get_extension(filename=file.filename, content_type=file.content_type)
        object_key = f"food-images/{file_id}{ext}"

        extra_args = {
            "ACL": "public-read",
        }

        file.file.seek(0)
        self.client.upload_fileobj(
            Fileobj=file.file,
            Bucket=self.config.bucket_name,
            Key=object_key,
            ExtraArgs=extra_args
        )

        file_url = self._build_public_url(object_key)

        return {
            "file_id": file_id,
            "file_url": file_url,
            "object_key": object_key,
        }

    def _build_public_url(self, object_key: str) -> str:
        return f"https://{self.config.bucket_name}.s3.{self.config.region_name}.amazonaws.com/{object_key}"

    def _get_extension(self, filename: str, content_type: str) -> str:
        if filename and "." in filename:
            return "." + filename.rsplit(".", 1)[-1].lower()

        guessed = mimetypes.guess_extension(content_type or "")
        return guessed or ".jpg"