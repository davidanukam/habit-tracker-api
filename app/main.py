from fastapi import FastAPI
from fastapi import Request
import logging
import time

from routers import habit_router, user_router

app = FastAPI()
app.title = "Habit Tracker API"
app.version = "0.1.0"
app.description = "An API that keeps track of your habits"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Routers
app.include_router(user_router.router)
app.include_router(habit_router.router)


@app.middleware("http")
async def my_custom_middleware(request: Request, call_next):
    start_time = time.time()

    # 1. Do something BEFORE the request hits your route (e.g., start a timer, inspect headers)
    # print("Request is coming in!")

    # 2. Pass the request along to the actual route handler
    response = await call_next(request)

    # 3. Do something AFTER the route finishes, but BEFORE sending it to the user
    process_time = time.time() - start_time
    logger.info(
        f" | Method {request.method} | URL: {request.base_url} | Path: {request.url.path} | Time: {process_time:.4f}s | Status: {response.status_code}"
    )
    # print("Response is going out!")

    # 4. You MUST return the response
    response.headers["X-Process-Time"] = str(process_time)
    return response
