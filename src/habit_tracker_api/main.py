from fastapi import FastAPI
from .routers import user_router

app = FastAPI(
    title="Habit Tracker API",
    description="An API to track all of my daily habits",
    version="0.1.0",
)

from .database.database import Base, engine

Base.metadata.create_all(bind=engine)


# @app.get("/", tags=["Main"])
# def main():
#     return {
#         "Habit Tracker API": "An API to track all of my daily habits",
#     }


app.include_router(user_router.router)
