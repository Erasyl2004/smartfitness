from app.interfaces.services.exercise import ExerciseService
from app.interfaces.services.benefit import BenefitService
from app.dtos.exercises import ExerciseDTO, ExerciseBaseDTO, ExerciseDetailDTO
from app.dtos.benefits import BenefitCreateDTO, BenefitDTO
from app.exceptions.exercise import ExerciseNotFoundException
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, status, HTTPException

router = APIRouter(route_class=DishkaRoute)

@router.get(
    "/{exercise_id}/details",
    status_code=status.HTTP_200_OK,
    summary="Получить exercise-details",
    description="Возвращает детальную информацию exercise по ID.",
    response_model=ExerciseDetailDTO
)
async def get_exercise_details_by_id(
    exercise_id: int,
    exercise_service: FromDishka[ExerciseService],
) -> ExerciseDetailDTO:
    exercise_details = await exercise_service.get_exercise_details_by_id(exercise_id=exercise_id)

    if not exercise_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'error': str(ExerciseNotFoundException(exercise_id=exercise_id))},
        )

    return exercise_details

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать exercise",
    description="Создает новую exercise, принимает данные, возвращает созданную сущность.",
    response_model=ExerciseDTO
)
async def create_exercise(
    payload: ExerciseBaseDTO,
    exercise_service: FromDishka[ExerciseService]
) -> ExerciseDTO:
    return await exercise_service.save_exercise(exercise=payload)

@router.post(
    "/{exercise_id}/benefits",
    status_code=status.HTTP_201_CREATED,
    summary="Создать exercise benefit",
    description="Создает новую exercise benefit, принимает данные, возвращает созданную сущность.",
    response_model=BenefitDTO
)
async def create_benefit(
    exercise_id: int,
    payload: BenefitCreateDTO,
    benefit_service: FromDishka[BenefitService]
) -> BenefitDTO:
    return await benefit_service.save_benefit(exercise_id=exercise_id, benefit_create=payload)

@router.put(
    "/{exercise_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить exercise",
    description="Полностью обновляет данные exercise по ID.",
    response_model=ExerciseDTO
)
async def update_exercise(
    exercise_id: int,
    payload: ExerciseBaseDTO,
    exercise_service: FromDishka[ExerciseService]
) -> ExerciseDTO:
    try:
        return await exercise_service.update_exercise(
            exercise_id=exercise_id,
            update_data=payload,
        )
    except ExerciseNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'error': str(exception)},
        )

@router.delete(
    "/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить exercise",
    description="Удаляет exercise по ID. Если сущность не найдена - 404. При успешном удалении возвращает HTTP 204 без тела ответа."
)
async def delete_exercise(
    exercise_id: int,
    exercise_service: FromDishka[ExerciseService]
) -> None:
    try:
        await exercise_service.delete_exercise(exercise_id=exercise_id)
    except ExerciseNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'error': str(exception)},
        )