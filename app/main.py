from app.stock_value import StockValue
from app.history_manager import HistoryManager
from app.email_sender import compare_and_send
from app import utils


def scheduled_function():
    print('\n' + '-'*50 + '\n')
    current_value, bankier_time = get_current_stock()
    hm = HistoryManager()
    history = hm.get_history()

    global_min = float(history['min'])
    global_max = float(history['max'])

    compare_and_send(current_value, global_min, global_max)
    hm.save_new_values(current_value, bankier_time, utils.now())


def get_current_stock():
    sv = StockValue()
    bankier = sv.get_bankier()
    value, time = sv.get_values(bankier)
    return value, time
