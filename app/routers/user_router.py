from fastapi import APIRouter, HTTPException
from models.user_model import UserCreate, UserUpdate
from models.habit_model import HabitCreate

import routers.habit_router

router = APIRouter(prefix="/users", tags=["users"])

users: list[UserCreate] = []

@router.get("/")
def get_all_users():
    """Return all currently registered users"""

    return users


@router.get("/{user_id}")
def get_user(user_id: int):
    """Return a specific user"""

    for user in users:
        if user.user_id == user_id:
            return user

    raise HTTPException(status_code=404, detail=f"No user with id {user_id} exists")


@router.get("/{user_id}/habits")
def get_all_user_habits(user_id: int):
    """Return all habits of a specific user"""

    found: bool = False
    for user in users:
        if user.user_id == user_id:
            found = True

    if not found:
        raise HTTPException(status_code=404, detail=f"No user with id {user_id} exists")

    user_habits: list[HabitCreate] = []
    for habit in routers.habit_router.habits:
        if habit.user_id == user_id:
            user_habits.append(habit)

    return user_habits


@router.get("/{user_id}/habits/{habit_id}")
def get_user_habit(user_id: int, habit_id: int):
    """Return a specific habit of specific user"""

    for user in users:
        if user.user_id == user_id:
            for habit in routers.habit_router.habits:
                if habit.user_id == user_id:
                    if habit.habit_id == habit_id:
                        return habit
            raise HTTPException(
                status_code=404, detail=f"No habit with id {habit_id} exists"
            )

    raise HTTPException(status_code=404, detail=f"No user with id {user_id} exists")


@router.post("/")
def create_user(new_user: UserCreate):
    """Add a new user"""

    if new_user.user_id in [user.user_id for user in users]:
        raise HTTPException(
            status_code=409, detail=f"A user with id {new_user.user_id} already exists"
        )

    new_user_id: int = 1 if not len(users) else users[-1].user_id + 1
    new_user.user_id = new_user_id
    users.append(new_user)
    return new_user


@router.put("/{user_id}")
def update_user(new_user: UserUpdate):
    """Update some user data"""

    index: int = -1
    for i, user in enumerate(users):
        if user.user_id == new_user.user_id:
            index = i
            break

    if index != -1:
        users[index].username = new_user.new_username if new_user.new_username else None
        users[index].password = new_user.new_password if new_user.new_password else None
        users[index].email = new_user.new_email if new_user.new_email else None
        return users[index]

    raise HTTPException(
        status_code=404, detail=f"No user with id {new_user.user_id} exists"
    )


@router.delete("/{user_id}")
def delete_user(user_id: int):
    """Delete a specific user"""

    for user in users:
        if user.user_id == user_id:
            users.remove(user)
            return user

    raise HTTPException(status_code=404, detail=f"No user with id {user_id} exists")
