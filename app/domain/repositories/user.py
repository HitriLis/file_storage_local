from typing import Optional, Tuple, List, Dict
from uuid import UUID
from abc import ABC, abstractmethod
from ..models.users import User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def get_by_uid(self, uid: UUID) -> Optional[User]: ...

    @abstractmethod
    async def exist_username(self, username: str) -> bool: ...

    @abstractmethod
    async def get_list_user(self) -> List[User]: ...

    @abstractmethod
    async def get_or_create(self, defaults: Dict = None) -> Tuple[User, bool]: ...

    @abstractmethod
    async def delete_user(self, uid: UUID) -> None: ...

    @abstractmethod
    async def update_user(self, uid: UUID, data: Dict) -> Optional[User]: ...
