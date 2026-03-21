from app.interfaces.repositories.profile import UserProfileRepository
from app.database.entities.profile import UserProfileEntity
from app.kernel.repository import CrudSQLRepository
from typing import Type, Optional
from dataclasses import dataclass
from sqlalchemy.future import select

dataclass(eq=False)
class UserProfileRepositoryImpl(
    CrudSQLRepository[UserProfileEntity],
    UserProfileRepository
):
    entity: Type[UserProfileEntity] = UserProfileEntity

    async def get_by_user_id(self, user_id: int) -> Optional[UserProfileEntity]:
        query = (
            select(UserProfileEntity).where(self.entity.user_id == user_id)
        )

        result = await self.session.execute(query)
        record = result.scalar_one_or_none()

        return record