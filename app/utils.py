from datetime import datetime
from time import time


def convert_epoch(epoch_time):
    int_time = int(epoch_time)/1000
    # todo: change format to something prettier
    return datetime.fromtimestamp(int_time).strftime('%c')


def now():
    return datetime.now().strftime("%c")


def calc_time(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        elapsed_time = end_time - start_time
        print(f"Execution of {func.__name__!r} done in {round(elapsed_time, 2)} seconds.")
        return result
    return wrapper
