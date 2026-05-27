from pydantic import BaseModel


class HabitCreate(BaseModel):
    habit_id: int = 0
    user_id: int = 0
    name: str
