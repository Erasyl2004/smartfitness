from app.interfaces.repositories.user import UserRepository
from app.interfaces.services.user import UserService
from app.repositories.user_repository import UserRepositoryImpl
from app.services.user_service import UserServiceImpl
from dishka import Provider, Scope, provide


class UserProvider(Provider):
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