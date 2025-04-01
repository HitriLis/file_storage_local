from typing import Optional, Tuple, List, Dict
from uuid import UUID
from abc import ABC, abstractmethod
from ..models.files import File


class IFilesRepository(ABC):

    @abstractmethod
    async def get_by_uid(self, user_id: UUID, uid: UUID) -> Optional[File]: ...

    @abstractmethod
    async def exist_file(self, uid: UUID) -> Optional[File]: ...

    @abstractmethod
    async def create_file(self, defaults: Dict = None) -> File: ...

    @abstractmethod
    async def delete_file(self, user_id: UUID, uid: UUID) -> None: ...

    @abstractmethod
    async def update_file(self, user_id: UUID, uid: UUID, data: Dict) -> Optional[File]: ...

    @abstractmethod
    async def file_list(self, user_id: UUID, offset: int, limit: int) -> Tuple[int, List[File]]: ...
