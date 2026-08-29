from sqlalchemy.orm import Mapped, mapped_column
from ..database.database import Base


class User(Base):
    __tablename__ = "users"

    # primary key: Unique identifier for each row that auto-increments and automatically indexed by default
    # index: Creates a lookup table to speed up SELECT/FILTER queries on this column at the cost of slightly slower writes
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)


class Habit(Base):
    __tablename__ = "habits"

    habit_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    des: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    started_at: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[str] = mapped_column(nullable=True)
