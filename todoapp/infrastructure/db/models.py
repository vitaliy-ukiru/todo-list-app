__all__ = (
    'Base',
    'User',
    'Task',
    'TaskList',
)

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from uuid6 import uuid7


class Base(DeclarativeBase):
    pass


class EntityBaseModel(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid7,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class User(EntityBaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column()
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class TaskList(EntityBaseModel):
    __tablename__ = "task_lists"
    name: Mapped[str] = mapped_column()
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))


class Task(EntityBaseModel):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column()
    desc: Mapped[str | None] = mapped_column()
    done_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    list_id: Mapped[UUID | None] = mapped_column(ForeignKey("task_lists.id", ondelete="cascade"))
