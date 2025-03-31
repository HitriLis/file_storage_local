import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Users(Base):
    __tablename__ = 'users'

    uid: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    username: Mapped[str] = mapped_column(sa.String, nullable=True)
    email: Mapped[str] = mapped_column(sa.String, unique=True,   nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(sa.String, nullable=True)
    last_name: Mapped[str] = mapped_column(sa.String, nullable=True)
    is_admin: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), default=datetime.utcnow, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"User:[{self.email!r}]"
