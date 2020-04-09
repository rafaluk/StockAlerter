import pandas as pd
import os


class HistoryManager:
    def __init__(self, filename='history.csv'):
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                # todo: add mail and stock
                file.write(',value,symbol,user,bankier_time,server_time')
        self.history = pd.read_csv(filename, delimiter=',', index_col=0)

    # todo: what if there are few different transactions for 1 company?
    # there must be something, which identifies particular transaction
    def get_min(self, symbol, user):
        filtered_history = self.history[(self.history['symbol'] == symbol) &
                                        (self.history['user'] == user)]
        return float(filtered_history['value'].min())

    def get_max(self, symbol, user):
        filtered_history = self.history[(self.history['symbol'] == symbol) &
                                        (self.history['user'] == user)]
        return float(filtered_history['value'].max())

    def update_history(self, value, symbol, user, bankier_time, server_time):
        update_data = {'value': value,
                       'symbol': symbol,
                       'user': user,
                       'bankier_time': bankier_time,
                       'server_time': server_time}

        self.history.loc[len(self.history)] = update_data
        self.history.to_csv(self.filename)

        print(f"History updated with: {update_data}")

        return self.history

