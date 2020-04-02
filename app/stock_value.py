import requests
from bs4 import BeautifulSoup
from app.utils import convert_epoch


class StockValue:
    def __init__(self, symbol='CDPROJEKT'):
        self.symbol = str(symbol)

    # todo: decorator for printing time elapsed (sent in mail?)
    def get_bankier(self):
        address = 'https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=' + self.symbol
        raw_site = requests.get(address).text.encode("utf-8")
        parsed_site = BeautifulSoup(raw_site, features="html.parser")
        return parsed_site

    def get_values(self, parsed_site):
        """Return tuple (stock_value, trade_time)."""

        trades = parsed_site.find_all("div", {'id': 'last-trade-' + self.symbol})

        stock_value = float(trades[0]['data-last'])
        trade_time_epoch = int(trades[0]['data-last-epoch'])
        trade_time = convert_epoch(trade_time_epoch)

        return stock_value, trade_time

