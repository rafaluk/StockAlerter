# todo: @dataclass decorator would help
class Calculator:

    # constants
    COMISSION_THRESHOLD = 0.0039
    BELKA_TAX = 0.19

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
        self.commission_buy = self.number_of_stocks_buy * self.price_buy * self.COMISSION_THRESHOLD
        self.commission_sell = self.number_of_stocks_sell * self.price_sell * self.COMISSION_THRESHOLD

        print('commission_buy:', self.commission_buy)
        print('commission_sell:', self.commission_sell)

        return self.commission_buy, self.commission_sell

    def results_without_commission(self):
        self.revenue_without_commission = self.number_of_stocks_sell * self.price_sell
        self.cost_without_commission = self.number_of_stocks_buy * self.price_buy
        self.profit_without_commission = round(self.revenue_without_commission - self.cost_without_commission, 4)

        print('revenue_without_commission:', self.revenue_without_commission)
        print('cost_without_commission:', self.cost_without_commission)
        print('profit_without_commission:', self.profit_without_commission)

        return self.revenue_without_commission, self.cost_without_commission, self.profit_without_commission

    def results_with_commission(self):
        self.revenue_with_commission = self.revenue_without_commission - self.commission_sell
        self.cost_with_commission = self.cost_without_commission + self.commission_buy
        self.profit_with_commission = self.revenue_with_commission - self.cost_with_commission

        print('revenue_with_commission:', self.revenue_with_commission)
        print('cost_with_commission:', self.cost_with_commission)
        print('profit_with_commission:', self.profit_with_commission)

        return self.revenue_with_commission, self.cost_with_commission, self.profit_with_commission

    def results_after_tax(self):
        self.profit_with_commission_after_tax = self.profit_with_commission * (1 - self.BELKA_TAX)

        print('profit_with_commission_after_tax:', self.profit_with_commission_after_tax)

        return self.profit_with_commission_after_tax
