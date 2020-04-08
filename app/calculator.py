from app.utils import Constants


class Calculator:

    def __init__(self, number_of_stocks_buy, price_buy, number_of_stocks_sell, price_sell):
        self.number_of_stocks_buy = number_of_stocks_buy
        self.price_buy = price_buy
        self.number_of_stocks_sell = number_of_stocks_sell
        self.price_sell = price_sell
        self.commission_sell = None
        self.commission_buy = None
        self.revenue_without_commission = None
        self.cost_without_commission = None
        self.profit_without_commission = None
        self.revenue_with_commission = None
        self.cost_with_commission = None
        self.profit_with_commission = None
        self.profit_with_commission_after_tax = None

        print('Calculator initiated with parameters:')
        print('\tnumber_of_stocks_buy:', self.number_of_stocks_buy)
        print('\tprice_buy:', self.price_buy)
        print('\tnumber_of_stocks_sell:', self.number_of_stocks_sell)
        print('\tprice_sell:', self.price_sell)

    def commissions(self):
        self.commission_buy = self.number_of_stocks_buy * self.price_buy * Constants.COMMISSION_RATE
        self.commission_sell = self.number_of_stocks_sell * self.price_sell * Constants.COMMISSION_RATE

        return round(self.commission_buy, 2), round(self.commission_sell, 2)

    def change(self):
        change = (self.price_sell - self.price_buy) / self.price_buy
        return round(change*100, 2)

    def results_without_commission(self):
        self.revenue_without_commission = self.number_of_stocks_sell * self.price_sell
        self.cost_without_commission = self.number_of_stocks_buy * self.price_buy
        self.profit_without_commission = round(self.revenue_without_commission - self.cost_without_commission, 4)

        return round(self.revenue_without_commission, 2), round(self.cost_without_commission, 2), round(self.profit_without_commission, 2)

    def results_with_commission(self):
        self.revenue_with_commission = self.revenue_without_commission - self.commission_sell
        self.cost_with_commission = self.cost_without_commission + self.commission_buy
        self.profit_with_commission = self.revenue_with_commission - self.cost_with_commission

        return round(self.revenue_with_commission, 2), round(self.cost_with_commission, 2), round(self.profit_with_commission, 2)

    def profit_after_tax(self):
        self.profit_with_commission_after_tax = self.profit_with_commission * (1 - Constants.CAPITAL_GAINS_TAX)

        return round(self.profit_with_commission_after_tax, 2)
