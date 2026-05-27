from fastapi import APIRouter, HTTPException
from models.completion_model import CompletionCreate

import utils.refresh_completions

router = APIRouter(prefix="/completions", tags=["completions"])

completions: list[CompletionCreate] = []


@router.get("/")
def get_all_completions():
    """Return all currently made completions"""

    utils.refresh_completions.refresh_completed_today_status()
    return completions


@router.get("/{completion_id}")
def get_completion(completion_id: int):
    """Return a specific completion"""

    utils.refresh_completions.refresh_completed_today_status()
    for completion in completions:
        if completion.completion_id == completion_id:
            return completion

    raise HTTPException(
        status_code=404, detail=f"No completion with id {completion_id} exists"
    )
