from app.web.v1.auth.controller import router as auth_router
from app.web.v1.body_areas.controller import router as body_areas_router
from app.web.v1.exercises.controller import router as exercises_router
from app.providers.application import get_providers
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka
from dishka import make_async_container
from fastapi import FastAPI

def app_factory() -> FastAPI:
    container = make_async_container(*get_providers())

    app = FastAPI(docs_url="/docs", title="FastAPI smart fitness service")
    setup_fastapi_dishka(container=container, app=app)

    app.include_router(
        router=auth_router,
        prefix="/api/v1/auth",
        tags=["Auth"]
    )
    app.include_router(
        router=body_areas_router,
        prefix="/api/v1/body-areas",
        tags=["Body areas"]
    )
    app.include_router(
        router=exercises_router,
        prefix="/api/v1/exercises",
        tags=["Exercises"]
    )

    return app