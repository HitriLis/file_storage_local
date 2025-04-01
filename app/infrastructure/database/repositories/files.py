from typing import Optional, Tuple, List, Dict
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.sql import exists
from sqlalchemy import delete, update, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.files import File
from domain.repositories.files import IFilesRepository
from ..models.file_storage import Files as FilesModel


class SQLAlchemyFileRepository(IFilesRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exist_file(self, uid: UUID) -> bool:
        async with self._session as session:
            result = await session.execute(
                select(exists().where(FilesModel.uid == uid))
            )
            return result.scalar()

    async def get_by_uid(self, user_id: UUID, uid: UUID) -> Optional[File]:
        async with self._session as session:
            stmt = select(FilesModel).where(
                FilesModel.uid == uid,
                FilesModel.user_id == user_id
            )
            result = await session.execute(stmt)
            file_model = result.scalar_one_or_none()
            if file_model:
                return File(
                    uid=file_model.uid,
                    path=file_model.path,
                    filename=file_model.filename,
                    created_at=file_model.created_at,
                    updated_at=file_model.updated_at
                )
            return None

    async def create_file(self, defaults: Dict = None) -> File:
        async with self._session as session:
            stmt = insert(FilesModel).values(**defaults).returning(FilesModel)
            result = await session.execute(stmt)
            file_model = result.scalar_one()
            file = File(
                    uid=file_model.uid,
                    path=file_model.path,
                    filename=file_model.filename,
                    created_at=file_model.created_at,
                    updated_at=file_model.updated_at
                )
            await session.commit()
            return file

    async def delete_file(self, user_id: UUID, uid: UUID) -> None:
        async with self._session as session:
            stmt = delete(FilesModel).where(
                FilesModel.uid == uid,
                FilesModel.user_id == user_id
            )
            await session.execute(stmt)
            await session.commit()

    async def update_file(self, user_id: UUID, uid: UUID, update_data: Dict) -> Optional[File]:
        async with self._session as session:
            stmt = update(FilesModel).where(
                FilesModel.uid == uid,
                FilesModel.user_id == user_id
            ).values(
                **update_data).returning(FilesModel)
            result = await session.execute(stmt)
            file_model = result.scalar_one_or_none()
            response = File(
                    uid=file_model.uid,
                    path=file_model.path,
                    filename=file_model.filename,
                    created_at=file_model.created_at,
                    updated_at=file_model.updated_at
                ) if file_model else None
            await session.commit()
            return response

    async def file_list(self, user_id: UUID, offset: int, limit: int) -> Tuple[int, List[File]]:
        async with self._session as session:
            stmt = select(FilesModel).where(FilesModel.user_id == user_id)
            count_result_query = select(func.count()).select_from(FilesModel)
            count_result = await session.execute(count_result_query)
            total_count = count_result.scalar()
            result = await session.execute(
                stmt.limit(limit).offset(offset)
            )
            files = result.scalars().all()
            return total_count, [
                File(
                    uid=file_model.uid,
                    path=file_model.path,
                    filename=file_model.filename,
                    created_at=file_model.created_at,
                    updated_at=file_model.updated_at
                ) for file_model in files]
