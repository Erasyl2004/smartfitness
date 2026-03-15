from app.interfaces.services.nutrition import NutritionService
from app.security.validation import get_current_active_auth_user
from app.dtos.nutritions import CalculateNutritionDTO
from app.dtos.users import UserDTO
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, status, Depends


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