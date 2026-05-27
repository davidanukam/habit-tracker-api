from fastapi import APIRouter, HTTPException
from models.habit_model import HabitCreate
from models.completion_model import CompletionCreate

from datetime import date, timedelta

import routers.user_router
import routers.completion_router

import utils.refresh_completions

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
            # Check if a completion was already made today for this habit
            todays_date = date.today()

            curr_habit_completions: list[CompletionCreate] = []
            for completion in routers.completion_router.completions:
                if completion.habit_id == habit_id:
                    curr_habit_completions.append(completion)

            if curr_habit_completions:
                for completion in curr_habit_completions:
                    if completion.date_completed == todays_date:
                        raise HTTPException(
                            status_code=409,
                            detail="This habit was already completed today",
                        )

            # Create a new Completion record
            new_completion = CompletionCreate()
            new_completion_id = (
                1
                if not len(routers.completion_router.completions)
                else routers.completion_router.completions[-1].completion_id + 1
            )
            new_completion.completion_id = new_completion_id
            new_completion.habit_id = habit_id
            new_completion.date_completed = todays_date

            utils.refresh_completions.refresh_completed_today_status()

            new_completion.completed_today = True

            if curr_habit_completions:
                yesterday_date = todays_date - timedelta(days=1)

                r_sorted_completions = list(
                    sorted(
                        curr_habit_completions,
                        key=lambda c: c.completion_id,
                        reverse=True,
                    )
                )

                if r_sorted_completions[0].completed_today == False:
                    if r_sorted_completions[0].date_completed == yesterday_date:
                        habit.streak += 1
                    else:
                        habit.streak = 0
            else:
                habit.streak += 1

            routers.completion_router.completions.append(new_completion)
            return habit

    raise HTTPException(status_code=404, detail=f"No habit with id {habit_id} exists")


@router.delete("/{habit_id}")
def delete_habit(habit_id: int):
    """Delete a specific habit"""

    for habit in habits:
        if habit.habit_id == habit_id:
            habits.remove(habit)
            for completion in routers.completion_router.completions:
                if completion.habit_id == habit_id:
                    routers.completion_router.completions.remove(completion)
            return habit

    raise HTTPException(status_code=404, detail=f"No habit with id {habit_id} exists")
