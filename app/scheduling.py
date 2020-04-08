from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from app.main import scheduled_function


def run_scheduler():
    scheduler = BackgroundScheduler()
    # todo: change hours. GPW works 9-17.
    scheduler.add_job(func=scheduled_function, trigger="interval",
                      seconds=10)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
