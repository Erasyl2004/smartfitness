from app.interfaces.services.nutrition import NutritionService
from app.security.validation import get_current_active_auth_user
from app.dtos.nutritions import CalculateNutritionDTO, NutritionDTO
from app.dtos.users import UserDTO
from app.exceptions.nutrition import UnprocessableNutritionException
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException


router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/",
    status_code = status.HTTP_200_OK,
    summary = "Получить nutrition по user",
    description = "Возвращает статистику nutrition по user в разрезе недели",
    response_model = list[CalculateNutritionDTO]
)
async def get_nutrition(
    nutrition_service: FromDishka[NutritionService],
    user: UserDTO = Depends(get_current_active_auth_user),
) -> list[CalculateNutritionDTO]:
    return await nutrition_service.calculate_user_nutrition(
        user_id=user.id
    )

@router.post(
    "/",
    status_code = status.HTTP_201_CREATED,
    summary = "Рассчитать nutrition по фото",
    description = "Рассчитывает статистику nutrition по фото еды",
    response_model = NutritionDTO
)
async def process_nutrition(
    nutrition_service: FromDishka[NutritionService],
    photo: UploadFile = File(...),
    user: UserDTO = Depends(get_current_active_auth_user)
) -> NutritionDTO:
    allowed_types = {"image/jpeg", "image/png", "image/webp", "image/heic"}

    if photo.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail={"error": "Only image files are allowed"})

    try:
        return await nutrition_service.recognize_nutrition_by_photo(
            user_id=user.id,
            photo=photo
        )
    except UnprocessableNutritionException as exception:
        raise HTTPException(status_code=422, detail={'error': str(exception)})