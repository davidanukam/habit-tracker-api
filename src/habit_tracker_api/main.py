from fastapi import FastAPI
from .routers import users

app = FastAPI(
    title="Habit Tracker API",
    description="An API to track all of my daily habits",
    version="0.1.0",
)

app.include_router(
    users.router,
    tags=["Users"],
)
