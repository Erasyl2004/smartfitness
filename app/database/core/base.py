from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

def new_session_maker(database_url: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        url=database_url,
        future=True,
        pool_size=10,
        max_overflow=15,
        echo=False
    )

    return async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )