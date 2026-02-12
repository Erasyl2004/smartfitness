from app.interfaces.repositories.exercise import ExerciseRepository
from app.interfaces.services.exercise import ExerciseService
from app.repositories.exercise_repository import ExerciseRepositoryImpl
from app.services.exercise_service import ExerciseServiceImpl
from dishka import Provider, Scope, provide


class ExerciseProvider(Provider):
    repository = provide(
        source=ExerciseRepositoryImpl,
        scope=Scope.REQUEST,
        provides=ExerciseRepository
    )

    service = provide(
        source=ExerciseServiceImpl,
        scope=Scope.REQUEST,
        provides=ExerciseService
    )