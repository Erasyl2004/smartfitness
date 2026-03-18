from app.interfaces.services.s3 import S3Service
from app.services.s3_service import S3ServiceImpl
from app.web.settings import S3Settings
from dishka import Provider, Scope, provide
from botocore.client import BaseClient
import boto3

class S3Provider(Provider):
    s3_settings = provide(S3Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_s3_client(self, config: S3Settings) -> BaseClient:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            region_name=config.region_name
        )

        return s3_client

    service = provide(
        source=S3ServiceImpl,
        scope=Scope.REQUEST,
        provides=S3Service
    )