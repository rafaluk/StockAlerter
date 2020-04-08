import pandas as pd
import os


class HistoryManager:
    def __init__(self, filename='history.csv'):
        self.filename = filename
        self.global_min = None
        self.global_max = None
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write(',value,bankier_time,server_time')
        self.history = pd.read_csv(filename, delimiter=',', index_col=0)

    def get_history(self):
        self.global_min = self.history['value'].min()
        self.global_max = self.history['value'].max()

        return {'min': self.global_min,
                'max': self.global_max}

    def save_new_values(self, value, bankier_time, server_time):
        self.history.loc[len(self.history)] = {'value': value,
                                               'bankier_time': bankier_time,
                                               'server_time': server_time}
        self.history.to_csv(self.filename)

        print(f"New data added to history:"
              f"\n\tValue: {value}"
              f"\n\tBankier time: {bankier_time}"
              f"\n\tServer time: {server_time}")

        return self.history

