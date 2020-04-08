import pandas as pd
import os


class HistoryManager:
    def __init__(self, filename='history.csv'):
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                # todo: add mail and stock
                file.write(',value,bankier_time,server_time')
        self.history = pd.read_csv(filename, delimiter=',', index_col=0)

    def get_min(self):
        return float(self.history['value'].min())

    def get_max(self):
        return float(self.history['value'].max())

    def update_history(self, value, bankier_time, server_time):
        self.history.loc[len(self.history)] = {'value': value,
                                               'bankier_time': bankier_time,
                                               'server_time': server_time}
        self.history.to_csv(self.filename)

        print(f"History updated with new data:"
              f"\n\tValue: {value}"
              f"\n\tBankier time: {bankier_time}"
              f"\n\tServer time: {server_time}")

        return self.history

