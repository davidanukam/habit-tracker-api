from pydantic import BaseModel


class CompletionCreate(BaseModel):
    completion_id: int
    habit_id: int
    completed_today: bool = False
    dates_completed: list[str] = []
    streak: int = 0
