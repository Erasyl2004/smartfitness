from app.database.core.settings import DatabaseSettings
from app.database.core.base import new_session_maker
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncIterable

class ConnectionProvider(Provider):
    database_settings = provide(DatabaseSettings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: DatabaseSettings) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.database_url)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        session = session_maker()
        try:
            yield session

            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()