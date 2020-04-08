from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from app.stock_value import StockValue
from app.utils import now, get_config
from app.history_manager import HistoryManager
from app.email_sender import prepare_min_max_email, prepare_daily_email


def run_extreme_scheduler():
    """Check current prices and compare it with global minimum/maximum.
    If the price exceeds one of extremes, the mail is sent."""

    scheduler = BackgroundScheduler()
    # todo: change hours. GPW works 9-17.
    scheduler.add_job(func=run_for_all, trigger="interval",
                      seconds=10)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


def run_regular_scheduler():
    """Send regular mail with current prices."""
    # todo: schedule for 18:00 every day
    # todo: daily min, max, open, close
    # todo: attach a chart
    # todo: one mail for one recipient with different stocks
    pass


def run_for_all():
    config = get_config()
    for recipient in config['recipients']:
        for stock in recipient['stocks']:
            print(recipient['address'], stock['symbol'])

            print('\n' + '-'*50 + '\n')

            sv = StockValue(stock['symbol'])
            bankier = sv.get_bankier()
            current_value, bankier_time = sv.get_values(bankier)

            # todo: refactor history (add: mail, stock)
            hm = HistoryManager()

            global_min = hm.get_min()
            global_max = hm.get_max()

            prepare_min_max_email(current_value, global_min, global_max, config)
            hm.update_history(current_value, bankier_time, now())
