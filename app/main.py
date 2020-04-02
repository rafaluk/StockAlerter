from app.stock_value import StockValue
from app.min_max_manager import MinMaxManager
from app import utils


def scheduled_function():
    current_value, bankier_time = get_current_stock()
    mmm = MinMaxManager()
    mmm.save_new_values(current_value, bankier_time, utils.now())
    globals = mmm.get_globals()
    global_min = globals['min']
    global_max = globals['max']

    if current_value > global_max:
        print("O KURWA")
        # todo: send email
    elif current_value < global_min:
        print("O KURCZE")
        # todo: send email


def get_current_stock():
    sv = StockValue()
    print("getting bankier website")
    bankier = sv.get_bankier()
    print("parsing bankier website")
    value, time = sv.get_values(bankier)
    return value, time



# if __name__ == '__main__':
#     main()
