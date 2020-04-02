from app.stock_value import StockValue


def main():
    sv = StockValue()
    bankier = sv.get_bankier()
    stock_value, trade_time = sv.get_values(bankier)
    print('stock_value:', stock_value)
    print('trade_time:', trade_time)


if __name__ == '__main__':
    main()
