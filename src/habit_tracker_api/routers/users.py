from fastapi import APIRouter, HTTPException, status

router = APIRouter()

users: list[dict] = []


@router.get("/users")
def get_users():
    return users


@router.get("/users/{id}")
def get_user(id: int):
    for user in users:
        if user["id"] == id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
    )


@router.post("/users")
def create_user(username: str, password: str, email: str):
    id = max([users[i]["id"] for i in range(len(users))]) + 1 if len(users) else 1
    new_user = {"id": id, "username": username, "password": password, "email": email}
    users.append(new_user)
    return new_user


@router.put("/users/{id}")
def update_user(
    id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
):
    for user in users:
        if user["id"] == id:
            user["username"] = username if username else user["username"]
            user["password"] = password if password else user["password"]
            user["email"] = email if email else user["email"]
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
    )


@router.delete("/users/{id}")
def delete_user(id: int):
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
    )
