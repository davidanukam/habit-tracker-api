from fastapi import APIRouter, HTTPException, Depends, status

# For pydantic validation
from ..schemas.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
)

# For database
from ..models.models import User
from ..database.database import get_db

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    """Return all currently registered users"""

    user_table = db.query(User).all()

    return user_table


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    found_user = db.query(User).filter(User.user_id == user_id).first()

    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with user_id {user_id} exists",
        )

    return found_user


@router.post("/", response_model=UserResponse)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    """Add a new user"""
    new_user = User(**user_create.model_dump())
    db.add(new_user)

    try:
        db.commit()

        # call refresh because I need Python to fetch the latest, updated state of an object directly from the database
        db.refresh(new_user)

        return new_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email or username already exists.",
        )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Update some user data"""

    updated_user = db.query(User).filter(User.user_id == user_id).first()

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with user_id {user_id} exists",
        )

    # Apply changes to the python object
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(updated_user, key, value)

    db.commit()

    # call refresh because I need Python to fetch the latest, updated state of an object directly from the database
    db.refresh(updated_user)

    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a specific user"""

    deleted_user = db.query(User).filter(User.user_id == user_id).first()

    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with user_id {user_id} exists",
        )

    db.delete(deleted_user)
    db.commit()
