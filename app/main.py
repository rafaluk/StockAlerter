from app.stock_value import StockValue
from app.history_manager import HistoryManager
from app.email_sender import send_email
from app import utils
import os

LOGIN = os.environ.get('STOCK_ALERTER_LOGIN')
PASSWORD = os.environ.get('STOCK_ALERTER_PASSWORD')
MY_EMAIL = os.environ.get('MY_GMAIL')


def scheduled_function():
    current_value, bankier_time = get_current_stock()
    mmm = HistoryManager()
    history = mmm.get_history()

    global_min = float(history['min'])
    global_max = float(history['max'])

    if current_value > global_max:
        subject = 'New global maximum'
        message = f'Current_value: {current_value} > {global_max} (global_max)'
        print(message)
        send_email(login=LOGIN, password=PASSWORD, recipient=MY_EMAIL,
                   subject=subject, message=message)

    elif current_value < global_min:
        subject = 'New global minimum'
        message = f'Current_value: {current_value} < {global_min} (global_max)'
        print(message)
        send_email(login=LOGIN, password=PASSWORD, recipient=MY_EMAIL,
                   subject=subject, message=message)

    else:
        message = f'Current_value: {current_value}.'
        print(message + "; email not sent.")

    mmm.save_new_values(current_value, bankier_time, utils.now())


def get_current_stock():
    sv = StockValue()
    bankier = sv.get_bankier()
    value, time = sv.get_values(bankier)
    return value, time
