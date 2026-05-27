from fastapi import APIRouter, HTTPException
from models.habit_model import HabitCreate
from models.completion_model import CompletionCreate

import routers.user_router

from datetime import datetime

router = APIRouter(prefix="/habits", tags=["habits"])

habits: list[HabitCreate] = []


@router.get("/")
def get_all_habits():
    """Return all currently made habits"""

    return habits


@router.get("/{habit_id}")
def get_habit(habit_id: int):
    """Return a specific habit"""

    for habit in habits:
        if habit.habit_id == habit_id:
            return habit

    raise HTTPException(status_code=404, detail=f"No habit with id {habit_id} exists")


@router.post("/")
def create_habit(new_habit: HabitCreate):
    """Add a new habit"""
    if new_habit.user_id not in [user.user_id for user in routers.user_router.users]:
        raise HTTPException(
            status_code=404, detail=f"No user with id {new_habit.user_id} exists"
        )

    if new_habit.habit_id in [habit.habit_id for habit in habits]:
        raise HTTPException(
            status_code=409,
            detail=f"A habit with id {new_habit.habit_id} already exists",
        )

    new_habit_id = 1 if not len(habits) else habits[-1].habit_id + 1
    new_habit.habit_id = new_habit_id

    habits.append(new_habit)

    return new_habit


@router.put("/")
def replace_habit(new_habit: HabitCreate):
    """Replace an entire habit"""

    index = -1
    for i, habit in enumerate(habits):
        if habit.habit_id == new_habit.habit_id:
            index = i
            break

    if index != -1:
        habits[index] = new_habit
        return new_habit

    raise HTTPException(
        status_code=404, detail=f"No habit with id {new_habit.habit_id} exists"
    )


@router.patch("/{habit_id}")
def mark_habit(habit_id: int):
    """Mark a habit as completed"""

    for habit in habits:
        if habit.habit_id == habit_id:
            completion = CompletionCreate()
            completion.completed_today = True
            completion.streak += 1
            now = datetime.now()
            completion.dates_completed.append(f"{now.day}/{now.month}/{now.year}")
            return habit

    raise HTTPException(status_code=404, detail=f"No habit with id {habit_id} exists")


@router.delete("/{habit_id}")
def delete_habit(habit_id: int):
    """Delete a specific habit"""

    for habit in habits:
        if habit.habit_id == habit_id:
            habits.remove(habit)
            return habit

    raise HTTPException(status_code=404, detail=f"No habit with id {habit_id} exists")
