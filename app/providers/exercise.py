from app.interfaces.repositories.exercise import ExerciseRepository
from app.interfaces.repositories.benefit import BenefitRepository
from app.interfaces.services.exercise import ExerciseService
from app.interfaces.services.benefit import BenefitService
from app.repositories.exercise_repository import ExerciseRepositoryImpl
from app.repositories.benefit_repository import BenefitRepositoryImpl
from app.services.exercise_service import ExerciseServiceImpl
from app.services.benefit_service import BenefitServiceImpl
from dishka import Provider, Scope, provide


class ExerciseProvider(Provider):
    repository = provide(
        source=ExerciseRepositoryImpl,
        scope=Scope.REQUEST,
        provides=ExerciseRepository
    )

    benefit_repository = provide(
        source=BenefitRepositoryImpl,
        scope=Scope.REQUEST,
        provides=BenefitRepository
    )

    service = provide(
        source=ExerciseServiceImpl,
        scope=Scope.REQUEST,
        provides=ExerciseService
    )

    benefit_service = provide(
        source=BenefitServiceImpl,
        scope=Scope.REQUEST,
        provides=BenefitService
    )