from fastapi import APIRouter, HTTPException, status
from ..schemas.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter()

users: list[UserResponse] = []


@router.get("/users", response_model=list[UserResponse])
def get_users():
    return users


@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int):
    for user in users:
        if user.user_id == id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
    )


@router.post("/users", response_model=UserResponse)
def create_user(new_user: UserCreate):
    id = max([users[i].user_id for i in range(len(users))]) + 1 if len(users) else 1

    new_user_response = UserResponse(
        user_id=id,
        username=new_user.username,
        password=new_user.password,
        email=new_user.email,
    )

    users.append(new_user_response)

    return new_user_response


@router.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, updated_user: UserUpdate):
    user = next((u for u in users if u.user_id == id), None)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    update_data = updated_user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    return user


@router.delete("/users/{id}", response_model=UserResponse)
def delete_user(id: int):
    for user in users:
        if user.user_id == id:
            users.remove(user)
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
    )
