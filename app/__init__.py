from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from app.stock_value import StockValue
from app.min_max_manager import MinMaxManager
from app.main import scheduled_function

app = Flask(__name__)

# todo: change hours. GPW works 9-17.
scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_function, trigger="interval", seconds=3)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def hello():
    return "Server is running."
