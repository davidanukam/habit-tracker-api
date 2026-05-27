from pydantic import BaseModel
from models.habit_model import HabitCreate


class UserCreate(BaseModel):
    user_id: int = 0
    username: str
    password: str
    email: str


class UserUpdate(BaseModel):
    user_id: int
    new_username: str
    new_password: str
    new_email: str
