from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    user_id: int = 0
    username: str
    password: str
    email: EmailStr


class UserUpdate(BaseModel):
    user_id: int
    new_username: str
    new_password: str
    new_email: str


class HabitCreate(BaseModel):
    habit_id: int = 0
    user_id: int = 0
    name: str
    streak: int = 0


class CompletionCreate(BaseModel):
    completion_id: int = 0
    habit_id: int = 0
    completed_today: bool = False
    date_completed: str = "00/00/0000"
