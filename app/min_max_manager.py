import pandas as pd


class MinMaxManager:
    def __init__(self, filename='globals.csv'):
        self.filename = filename
        self.global_min = None
        self.global_max = None
        self.history = pd.read_csv(filename, delimiter=',', index_col=0)

    def get_globals(self):
        self.global_min = self.history['value'].min()
        self.global_max = self.history['value'].max()

        print(f"global_min: {self.global_min}")
        print(f"global_max: {self.global_max}")

        return {'min': self.global_min,
                'max': self.global_max}

    def save_new_values(self, value, time):
        self.history.loc[len(self.history)] = {'value': value, 'time': time}
        self.history.to_csv(self.filename)

        return self.history

