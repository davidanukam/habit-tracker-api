from fastapi import APIRouter, HTTPException
from models.completion_model import CompletionCreate

# import routers.habit_router

router = APIRouter(prefix="/completions", tags=["completions"])

completions: list[CompletionCreate] = []


@router.get("/")
def get_all_completions():
    """Return all currently made completions"""

    return completions


@router.get("/{completion_id}")
def get_completion(completion_id: int):
    """Return a specific completion"""

    for completion in completions:
        if completion.completion_id == completion_id:
            return completion

    raise HTTPException(
        status_code=404, detail=f"No completion with id {completion_id} exists"
    )


# @router.post("/{habit_id}")
# def create_completion(habit_id: int):
#     if habit_id not in [habit.habit_id for habit in routers.habit_router.habits]:
#         raise HTTPException(
#             status_code=404, detail=f"No habit with id {habit_id} exists"
#         )

#     new_completion = CompletionCreate()

#     new_completion_id = 1 if not len(completions) else completions[-1].completion_id + 1
#     new_completion.completion_id = new_completion_id

#     new_completion.habit_id = habit_id

#     completions.append(new_completion)

#     return new_completion
