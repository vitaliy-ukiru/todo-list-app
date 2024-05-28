__all__ = (
    'Base',
)

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column()
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class TaskList(BaseModel):
    __tablename__ = "task_lists"
    name: Mapped[str] = mapped_column()
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

class Task(BaseModel):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column()
    desc: Mapped[str | None] = mapped_column()
    done_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    list_id: Mapped[str | None] = mapped_column(ForeignKey("task_lists.id"))

