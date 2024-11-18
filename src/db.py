import enum
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Callable

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.conf import settings


class DB(enum.IntEnum):
    APP = 0
    OTEHR_APP = 1


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self.__engine = create_async_engine(host, **engine_kwargs)
        self.__sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.__engine, expire_on_commit=False
        )

    @property
    def is_closed(self) -> bool:
        return self.__engine is None

    async def close(self):
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.__engine.dispose()

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self.__engine.begin() as connection:
            try:
                yield connection
            except Exception as exc:
                await connection.rollback()
                raise exc

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.__sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self.__sessionmaker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            session.expunge_all()
            await session.close()


sessionmanager = DatabaseSessionManager(
    host=settings.database_conn_uri, engine_kwargs={"future": True, "pool_pre_ping": True}
)

def get_db(db: DB) -> Callable[[], AsyncIterator[AsyncSession]]:
    async def get() -> AsyncIterator[AsyncSession]:
        if db == DB.APP:
            async with sessionmanager.session() as session:
                yield session
        elif db == DB.OTEHR_APP:
            async with sessionmanager.session() as session:
                yield session
    return get
