from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from app.stock_value import StockValue


app = Flask(__name__)


def print_date_time():
    print(get_current_stock())


def get_current_stock():
    sv = StockValue()
    print("getting bankier website")
    bankier = sv.get_bankier()
    print("parsing bankier website")
    value, time = sv.get_values(bankier)
    return value, time


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def hello():
    return "Server is running."
