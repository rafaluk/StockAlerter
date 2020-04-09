import requests
from bs4 import BeautifulSoup
from app.utils import convert_epoch, calc_time


class StockValue:
    def __init__(self, symbol, config):
        self.symbol = str(symbol)
        self.config = config

    @calc_time
    def get_bankier(self):
        """Gets bankier.pl website of a stock, specified with symbol variable.

        :return: Source code of bankier.pl website."""

        address = self.config['sources']['bankier'] + self.symbol
        raw_site = requests.get(address).text.encode("utf-8")
        parsed_site = BeautifulSoup(raw_site, features="html.parser")
        return parsed_site

    def get_values(self, parsed_site):
        """Scrapes bankier.pl site.

        :return: (stock_value, trade_time)"""

        trades = parsed_site.find_all("div", {'id': 'last-trade-' + self.symbol})

        stock_value = float(trades[0]['data-last'])
        trade_time_epoch = int(trades[0]['data-last-epoch'])
        trade_time = convert_epoch(trade_time_epoch)

        return stock_value, trade_time

