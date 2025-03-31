from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from infrastructure.database.repositories.uow import UnitOfWork


async def async_session_generator(session_factory):
    async with session_factory() as session:
        yield session


class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    engine = providers.Singleton(
        create_async_engine,
        url=config.db_url,
        pool_size=config.POOL_SIZE,
        echo=config.ECHO_SQL
    )
    session_factory = providers.Factory(
        async_sessionmaker,
        bind=engine
    )

    session = providers.Resource(
        async_session_generator,
        session_factory=session_factory
    )
