from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from app.stock_value import StockValue
from app.utils import now, get_config
from app.history_manager import HistoryManager
from app.email_sender import prepare_min_max_email, prepare_daily_email
from app.calculator import Calculator


def run_min_max_scheduler():
    """Check current prices and compare it with global minimum/maximum.
    If the price exceeds one of extremes, the mail is sent."""

    scheduler = BackgroundScheduler()
    # todo: change hours. GPW works 9-17, mon-fri
    scheduler.add_job(func=min_max_for_all, trigger="interval",
                      seconds=10)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


def run_regular_scheduler():
    """Send regular mail with current prices."""
    # todo: schedule for 18:00 every day
    # todo: daily min, max, open, close
    # todo: attach a chart
    # todo: one mail for one recipient with different stocks
    scheduler = BackgroundScheduler()
    # todo: change hours. GPW works 9-17.
    scheduler.add_job(func=regular_for_all, trigger="cron",
                      hour=18, day_of_week='mon-fri')
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


def min_max_for_all():
    config = get_config()

    for recipient in config['recipients']:
        for transaction in recipient['transactions']:

            print('\n' + '-'*50 + '\n')

            symbol = transaction['symbol']
            # todo: this should be extracted to prepare_mail (chyba)
            sv = StockValue(symbol=symbol, config=config)
            bankier = sv.get_bankier()
            current_value, bankier_time = sv.get_values(bankier)

            # todo: refactor history (add: mail, stock)
            hm = HistoryManager()

            global_min = hm.get_min()
            global_max = hm.get_max()

            calculator = Calculator(transaction['buy_quantity'],
                                    transaction['buy_price'],
                                    transaction['buy_quantity'],
                                    current_value)

            prepare_min_max_email(symbol, current_value, global_min,
                                  global_max, config, calculator)
            hm.update_history(current_value, symbol, recipient['address'], bankier_time, now())


