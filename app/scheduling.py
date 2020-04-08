from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from app.stock_value import StockValue
from app import utils
from app.history_manager import HistoryManager
from app.email_sender import compare_and_send


def run_extreme_scheduler():
    """Check current prices and compare it with global minimum/maximum.
    If the price exceeds one of extremes, the mail is sent."""

    scheduler = BackgroundScheduler()
    # todo: change hours. GPW works 9-17.
    scheduler.add_job(func=scheduled_function, trigger="interval",
                      seconds=10)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


def run_regular_scheduler():
    """Send regular mail with current prices."""
    pass


def scheduled_function():
    # todo: call this function for all recipients/stocks in config
    print('\n' + '-'*50 + '\n')

    sv = StockValue()
    bankier = sv.get_bankier()
    current_value, bankier_time = sv.get_values(bankier)

    hm = HistoryManager()
    history = hm.get_history()

    global_min = float(history['min'])
    global_max = float(history['max'])

    compare_and_send(current_value, global_min, global_max)
    hm.save_new_values(current_value, bankier_time, utils.now())
