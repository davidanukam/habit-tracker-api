from fastapi import FastAPI

app = FastAPI(
    title="Habit Tracker API",
    description="An API to track all of my daily habits",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Hello World"}
