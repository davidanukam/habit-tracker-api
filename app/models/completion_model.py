from pydantic import BaseModel


class CompletionCreate(BaseModel):
    completion_id: int = 0
    habit_id: int = 0
    completed_today: bool = False
    date_completed: str = "00/00/0000"
