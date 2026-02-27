from app.interfaces.repositories.user import UserRepository
from app.interfaces.repositories.otp_code import OtpCodeRepository
from app.interfaces.repositories.chat_message import ChatMessageRepository
from app.interfaces.services.user import UserService
from app.interfaces.services.otp import OtpService
from app.interfaces.services.chat import ChatMessageService
from app.interfaces.templates.otp import OtpTemplate
from app.web.settings import OtpSettings
from app.repositories.user_repository import UserRepositoryImpl
from app.repositories.otp_code_repository import OtpCodeRepositoryImpl
from app.repositories.message_repository import ChatMessageRepositoryImpl
from app.services.user_service import UserServiceImpl
from app.services.otp_service import OtpServiceImpl
from app.services.chat_service import ChatMessageServiceImpl
from app.templates.otp_template import OtpTemplateImpl
from dishka import Provider, Scope, provide
from ssl import SSLContext, create_default_context
import certifi


class UserProvider(Provider):
    otp_config = provide(OtpSettings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_otp_ssl_context(self) -> SSLContext:
        return create_default_context(cafile=certifi.where())

    repository = provide(
        source=UserRepositoryImpl,
        scope=Scope.REQUEST,
        provides=UserRepository
    )

    service = provide(
        source=UserServiceImpl,
        scope=Scope.REQUEST,
        provides=UserService
    )

    otp_repository = provide(
        source=OtpCodeRepositoryImpl,
        scope=Scope.REQUEST,
        provides=OtpCodeRepository
    )

    otp_service = provide(
        source=OtpServiceImpl,
        scope=Scope.REQUEST,
        provides=OtpService
    )

    otp_template = provide(
        source=OtpTemplateImpl,
        scope=Scope.REQUEST,
        provides=OtpTemplate
    )

    message_repository = provide(
        source=ChatMessageRepositoryImpl,
        scope=Scope.REQUEST,
        provides=ChatMessageRepository
    )

    message_service = provide(
        source=ChatMessageServiceImpl,
        scope=Scope.REQUEST,
        provides=ChatMessageService
    )