from typing import Optional, Tuple, List, Dict
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.sql import exists
from sqlalchemy import delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models.users import User
from domain.repositories.user import IUserRepository
from ..models.users import Users as UserModel


class SQLAlchemyUserRepository(IUserRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self._session as session:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()
            if user_model:
                return User(
                    uid=user_model.uid,
                    username=user_model.username,
                    email=user_model.email,
                    first_name=user_model.first_name,
                    last_name=user_model.last_name,
                )
            return None

    async def get_by_uid(self, uid: UUID) -> Optional[User]:
        async with self._session as session:
            stmt = select(UserModel).where(UserModel.uid == uid)
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()
            if user_model:
                return User(
                    uid=user_model.uid,
                    username=user_model.username,
                    email=user_model.email,
                    first_name=user_model.first_name,
                    last_name=user_model.last_name,
                )
            return None

    async def exist_username(self, username: str) -> bool:
        async with self._session as session:
            result = await session.execute(
                select(exists().where(UserModel.username == username))
            )
            return result.scalar()

    async def get_list_user(self) -> List[User]:
        """Получает список всех пользователей."""
        async with self._session as session:
            stmt = select(UserModel)
            result = await session.execute(stmt)
            users = result.scalars().all()
            return [
                User(
                    uid=user.uid,
                    username=user.username,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                ) for user in users
            ]

    async def get_or_create(self, defaults: Dict = None) -> Tuple[User, bool]:
        async with self._session as session:
            if defaults is None:
                defaults = {}
            email = defaults.get("email")
            if not email:
                raise ValueError("Email is required for get_or_create")

            user = await self.get_by_email(email)
            if user:
                return user, False

            stmt = insert(UserModel).values(**defaults).returning(UserModel)
            result = await session.execute(stmt)
            user_model = result.scalar_one()
            user = User(
                uid=user_model.uid,
                username=user_model.username,
                email=user_model.email,
                first_name=user_model.first_name,
                last_name=user_model.last_name,
            )
            await session.commit()
            return user, True

    async def delete_user(self, uid: UUID) -> None:
        async with self._session as session:
            stmt = delete(UserModel).where(UserModel.uid == uid.bytes)
            await session.execute(stmt)
            await session.commit()

    async def update_user(self, uid: UUID, update_data: Dict) -> Optional[User]:
        async with self._session as session:
            stmt = update(UserModel).where(UserModel.uid == uid).values(**update_data).returning(UserModel)
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()
            response = User(
                uid=user_model.uid,
                username=user_model.username,
                email=user_model.email,
                first_name=user_model.first_name,
                last_name=user_model.last_name
            ) if user_model else None
            await session.commit()
            return response
