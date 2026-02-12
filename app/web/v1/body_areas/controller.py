from app.dtos.body_areas import BodyAreaBaseDTO, BodyAreaDTO
from app.dtos.exercises import ExerciseDTO
from app.interfaces.services.body_area import BodyAreaService
from app.interfaces.services.exercise import ExerciseService
from app.exceptions.body_area import BodyAreaNotFoundException
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, status, HTTPException

router = APIRouter(route_class=DishkaRoute)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать body area",
    description="Создает новую body area, принимает данные, возвращает созданную сущность.",
    response_model=BodyAreaDTO
)
async def create_body_area(
    payload: BodyAreaBaseDTO,
    body_area_service: FromDishka[BodyAreaService],
) -> BodyAreaDTO:
    return await body_area_service.save_body_area(body_area=payload)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Получить список body area",
    description="Возвращает список всех body area.",
    response_model=list[BodyAreaDTO]
)
async def get_all_body_areas(
    body_area_service: FromDishka[BodyAreaService],
) -> list[BodyAreaDTO]:
    return await body_area_service.get_all_body_areas()


@router.get(
    "/{body_area_id}/exercises",
    status_code=status.HTTP_200_OK,
    summary="Получить exercises по body area",
    description="Возвращает список всех exercises по ID body area.",
    response_model=list[ExerciseDTO]
)
async def get_all_body_areas(
    body_area_id: int,
    exercise_service: FromDishka[ExerciseService],
) -> list[ExerciseDTO]:
    return await exercise_service.get_all_body_area_exercises(
        body_area_id=body_area_id
    )


@router.put(
    "/{body_area_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить body area",
    description="Полностью обновляет данные body area по ID.",
    response_model=BodyAreaDTO
)
async def update_body_area(
    body_area_id: int,
    payload: BodyAreaBaseDTO,
    body_area_service: FromDishka[BodyAreaService],
) -> BodyAreaDTO:
    try:
        return await body_area_service.update_body_area(
            body_area_id=body_area_id,
            update_data=payload,
        )
    except BodyAreaNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'error': str(exception)},
        )

@router.delete(
    "/{body_area_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить body area",
    description="Удаляет body area по ID. Если сущность не найдена - 404. При успешном удалении возвращает HTTP 204 без тела ответа."
)
async def delete_body_area(
    body_area_id: int,
    body_area_service: FromDishka[BodyAreaService],
) -> None:
    try:
        await body_area_service.delete_body_area(body_area_id=body_area_id)
    except BodyAreaNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'error': str(exception)},
        )