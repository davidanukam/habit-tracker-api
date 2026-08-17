from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
def get_users():
    return [{"username": "alice"}, {"username": "bob"}]


@router.post("/users")
def create_user():
    return {"message": "User created successfully"}
