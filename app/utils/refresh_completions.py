from datetime import date
import routers.completion_router

def refresh_completed_today_status():
    for completion in routers.completion_router.completions:
        if (
            completion.date_completed != date.today()
            and completion.completed_today == True
        ):
            completion.completed_today = False
