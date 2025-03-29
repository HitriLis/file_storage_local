from sqlalchemy.ext.asyncio import AsyncSession
from domain.repositories.uow import IUnitOfWork


class UnitOfWork(IUnitOfWork):
    """Реализация UnitOfWork для SQLAlchemy"""

    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session = None

    async def __aenter__(self) -> AsyncSession:
        """Создаёт сессию и возвращает её"""
        self._session = self.session_factory()
        return self._session

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Коммит или откат и закрытие сессии"""
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
        self._session = None
