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
    config = get_config()
    interval_in_minutes = config['min_max_interval_minutes']
    scheduler = BackgroundScheduler()
    # todo: change hours. GPW works 9-17, mon-fri
    scheduler.add_job(func=min_max_for_all, trigger="interval",
                      minutes=interval_in_minutes)
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

            sv = StockValue(symbol=transaction['symbol'], config=config)
            bankier = sv.get_bankier()
            current_value, bankier_time = sv.get_values(bankier)

            hm = HistoryManager()
            global_min = hm.get_min(transaction['symbol'], recipient['address'])
            global_max = hm.get_max(transaction['symbol'], recipient['address'])

            calculator = Calculator(transaction['buy_quantity'],
                                    transaction['buy_price'],
                                    transaction['buy_quantity'],
                                    current_value)
            if transaction['min_max_mail'] == 'yes':
                prepare_min_max_email(recipient['address'], transaction['symbol'], current_value,
                                      global_min, global_max, config, calculator)
            hm.update_history(current_value, transaction['symbol'], recipient['address'], bankier_time, now())


def regular_for_all():
    config = get_config()

    for recipient in config['recipients']:
        if recipient['daily_mail'].lower() == 'yes':
            stocks_to_send = {}
            for transaction in recipient['transactions']:
                sv = StockValue(symbol=transaction['symbol'], config=config)
                bankier = sv.get_bankier()
                current_value, bankier_time = sv.get_values(bankier)
                stocks_to_send[transaction['symbol']] = current_value
            prepare_daily_email(recipient, stocks_to_send, config)
