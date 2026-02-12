from app.interfaces.repositories.user import UserRepository
from app.database.entities.users import UserEntity
from app.kernel.repository import CrudSQLRepository
from sqlalchemy.future import select
from typing import Type, Optional
from dataclasses import dataclass

dataclass(eq=False)
class UserRepositoryImpl(
    CrudSQLRepository[UserEntity],
    UserRepository
):
    entity: Type[UserEntity] = UserEntity

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        query = select(UserEntity).where(UserEntity.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        return user