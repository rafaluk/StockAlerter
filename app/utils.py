import datetime


def convert_epoch(epoch_time):
    int_time = int(epoch_time)/1000
    # todo: change format to something prettier
    return datetime.datetime.fromtimestamp(int_time).strftime('%c')

