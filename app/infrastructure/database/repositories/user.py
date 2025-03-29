from decimal import Decimal
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Tuple

from domain.exceptions.base import NegativeBalanceError
from domain.models.users import User
from domain.repositories.user_repository import IUserRepository
from ..models.users import Users as UserModel


class SQLAlchemyUserRepository(IUserRepository):

    async def get_or_create(self, session: AsyncSession, chat_id: int, defaults: dict = None) -> Tuple[User, bool]:
        if defaults is None:
            defaults = {}
        user = await self.get_by_chat_id(session, chat_id=chat_id)
        create = False
        if not user:
            create = True
            user_model = UserModel(chat_id=chat_id, **defaults)
            session.add(user_model)
            await session.commit()
            await session.refresh(user_model)
            user = User(
                id=user_model.id,
                chat_id=user_model.chat_id,
                username=user_model.username,
                first_name=user_model.first_name,
                last_name=user_model.last_name,
                balance=user_model.balance,
                created_at=user_model.created_at,
            )
        return user, create

    async def get_by_chat_id(self, session: AsyncSession, chat_id: int) -> Optional[User]:
        result = await session.execute(
            select(UserModel).where(UserModel.chat_id == chat_id)
        )
        user_model = result.scalars().first()
        if user_model:
            return User(
                id=user_model.id,
                chat_id=user_model.chat_id,
                username=user_model.username,
                first_name=user_model.first_name,
                last_name=user_model.last_name,
                balance=user_model.balance,
                created_at=user_model.created_at
            )
        return None

    async def delete_user(self, session: AsyncSession, item_id: int) -> None:
        await session.execute(
            delete(UserModel)
            .where(UserModel.id == item_id)
        )
        await session.commit()

    async def update_balance_user(self, session: AsyncSession, user_id: int, value: Decimal) -> Optional[User]:
        result = await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalars().first()
        if user_model:
            new_balance = user_model.balance + value
            if new_balance < 0:
                await session.rollback()
                raise NegativeBalanceError("Недостаточно средств для списания.")
            user_model.balance = new_balance
            await session.commit()
            await session.refresh(user_model)
            return User(
                id=user_model.id,
                chat_id=user_model.chat_id,
                username=user_model.username,
                first_name=user_model.first_name,
                last_name=user_model.last_name,
                balance=user_model.balance,
                created_at=user_model.created_at
            )
        return None
