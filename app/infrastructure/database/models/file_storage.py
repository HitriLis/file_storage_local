import uuid
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Files(Base):
    __tablename__ = 'files'

    uid: Mapped[str] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    filename: Mapped[str] = mapped_column(sa.String, nullable=False)
    path: Mapped[str] = mapped_column(sa.String, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.uid", ondelete="CASCADE"), nullable=False)
    user: Mapped["Users"] = relationship("Users", back_populates="files_list")
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    def __repr__(self) -> str:
        return f"File:[{self.title!r}], UUID:[{self.uid!r}]"
