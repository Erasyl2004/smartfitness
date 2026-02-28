from app.providers.connection import ConnectionProvider
from app.providers.body_area import BodyAreaProvider
from app.providers.exercise import ExerciseProvider
from app.providers.user import UserProvider
from app.providers.ai import AiProvider
from dishka import Provider

def get_providers() -> list[Provider]:
    return [
        UserProvider(),
        ConnectionProvider(),
        BodyAreaProvider(),
        ExerciseProvider(),
        AiProvider()
    ]