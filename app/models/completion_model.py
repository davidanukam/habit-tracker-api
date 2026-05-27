from pydantic import BaseModel


class CompletionCreate(BaseModel):
    completion_id: int = 0
    habit_id: int = 0
    completed_today: bool = False
    dates_completed: list[str] = []
    streak: int = 0
