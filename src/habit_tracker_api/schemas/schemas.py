from pydantic import BaseModel, EmailStr, ConfigDict, Field

from typing import Optional, Literal
from enum import StrEnum, auto

# Incoming Schemas (Create, Update): Parse JSON dicts -> No ConfigDict needed.
# Outgoing Schemas (Response): Read SQLAlchemy ORM objects -> from_attributes=True required.

# --- User Schema --- #


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    password: Optional[str] = Field(default=None, min_length=8)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Habit Schema --- #


class HabitStatus(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class HabitBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    des: str = Field(..., min_length=3, max_length=50)


class HabitCreate(HabitBase):
    user_id: int = Field(...)
    status: Literal[HabitStatus.PENDING, HabitStatus.IN_PROGRESS] = Field(
        default=HabitStatus.PENDING,
        description="Initial state of the habit. Allowed: PENDING, IN_PROGRESS.",
    )


class HabitUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    des: Optional[str] = Field(default=None, min_length=3, max_length=50)
    status: Optional[Literal[HabitStatus.PENDING, HabitStatus.IN_PROGRESS]] = None


class HabitResponse(HabitBase):
    habit_id: int
    status: HabitStatus
    started_at: str
    completed_at: str | None

    model_config = ConfigDict(from_attributes=True)
