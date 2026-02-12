from app.interfaces.repositories.body_area import BodyAreaRepository
from app.interfaces.services.body_area import BodyAreaService
from app.repositories.body_area_repository import BodyAreaRepositoryImpl
from app.services.body_area_service import BodyAreaServiceImpl
from dishka import Provider, Scope, provide


class BodyAreaProvider(Provider):
    repository = provide(
        source=BodyAreaRepositoryImpl,
        scope=Scope.REQUEST,
        provides=BodyAreaRepository
    )

    service = provide(
        source=BodyAreaServiceImpl,
        scope=Scope.REQUEST,
        provides=BodyAreaService
    )