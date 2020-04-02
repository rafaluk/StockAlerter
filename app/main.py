from app.stock_value import StockValue
from app.min_max_manager import MinMaxManager
from app import utils


def scheduled_function():
    current_value, bankier_time = get_current_stock()
    mmm = MinMaxManager()
    history = mmm.get_history()

    global_min = float(history['min'])
    global_max = float(history['max'])

    if current_value > global_max:
        print("O KURWA")
        # todo: send email
    elif current_value < global_min:
        print("O KURCZE")
        # todo: send email
    mmm.save_new_values(current_value, bankier_time, utils.now())


def get_current_stock():
    sv = StockValue()
    bankier = sv.get_bankier()
    value, time = sv.get_values(bankier)
    return value, time
