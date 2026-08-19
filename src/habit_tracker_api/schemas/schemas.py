from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional

# Incoming Schemas (UserCreate, UserUpdate): Parse JSON dicts -> No ConfigDict needed.
# Outgoing Schemas (UserResponse): Read SQLAlchemy ORM objects -> from_attributes=True required.


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    password: Optional[str] = Field(default=None, min_length=8)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)
