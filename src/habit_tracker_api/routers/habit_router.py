from fastapi import APIRouter, HTTPException, Depends, status

from datetime import datetime, timezone

# For pydantic validation
from ..schemas.schemas import (
    HabitCreate,
    HabitUpdate,
    HabitResponse,
)

# For database
from ..models.models import User, Habit
from ..database.database import get_db

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.get("/", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    """Return all created habits"""

    habit_table = db.query(Habit).all()

    return habit_table


@router.get("/{user_id}", response_model=List[HabitResponse])
def get_user_habits(user_id: int, db: Session = Depends(get_db)):
    found_user = db.query(User).filter(User.user_id == user_id).first()

    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with user_id {user_id} exists",
        )

    found_user_habits = db.query(Habit).filter(Habit.user_id == user_id).all()

    if not found_user_habits:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No habits for user with user_id {user_id} exist",
        )

    return found_user_habits


@router.post("/", response_model=HabitResponse)
def create_habit(habit_create: HabitCreate, db: Session = Depends(get_db)):
    new_habit = Habit(**habit_create.model_dump())

    found_user = db.query(User).filter(User.user_id == new_habit.user_id).first()

    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with user_id {new_habit.user_id} exists",
        )

    new_habit.name = new_habit.name[:1].upper() + new_habit.name[1:]
    new_habit.des = new_habit.des[:1].upper() + new_habit.des[1:]

    utc_now = datetime.now(timezone.utc)
    year = utc_now.year
    month = utc_now.month
    day = utc_now.day

    new_habit.started_at = f"{year}-{month:02}-{day}"

    db.add(new_habit)

    try:
        db.commit()
        db.refresh(new_habit)

        return new_habit

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error",
        )


@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(
    habit_id: int, habit_update: HabitUpdate, db: Session = Depends(get_db)
):
    updated_habit = db.query(Habit).filter(Habit.habit_id == habit_id).first()

    if not updated_habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No habit with habit_id {habit_id} exists",
        )

    for key, value in habit_update.model_dump(exclude_unset=True).items():
        setattr(updated_habit, key, value)

    db.commit()
    db.refresh(updated_habit)

    return updated_habit


@router.patch("/{habit_id}", response_model=HabitResponse)
def complete_habit(habit_id: int, db: Session = Depends(get_db)):
    completed_habit = db.query(Habit).filter(Habit.habit_id == habit_id).first()

    if not completed_habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No habit with habit_id {habit_id} exists",
        )

    utc_now = datetime.now(timezone.utc)
    year = utc_now.year
    month = utc_now.month
    day = utc_now.day

    completed_habit.status = "COMPLETED"
    completed_habit.completed_at = f"{year}-{month:02}-{day}"

    db.commit()
    db.refresh(completed_habit)

    return completed_habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    deleted_habit = db.query(Habit).filter(Habit.habit_id == habit_id).first()

    if not deleted_habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No habit with habit_id {habit_id} exists",
        )

    db.delete(deleted_habit)
    db.commit()
