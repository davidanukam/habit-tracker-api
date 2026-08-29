from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user_router, habit_router

app = FastAPI(
    title="Habit Tracker API",
    description="An API to track all of my daily habits",
    version="0.1.0",
)


# For development: allow all origins. Lock this down later.
origins = ["*", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .database.database import Base, engine

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
def root():
    return {
        "Habit Tracker API": "An API to track all of my daily habits",
    }


app.include_router(user_router.router)
app.include_router(habit_router.router)
