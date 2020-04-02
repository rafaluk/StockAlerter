
# constant
COMISSION_THRESHOLD = 0.0039
BELKA_TAX = 0.19

# buy
number_of_stocks_buy = 9
price_buy = 272.16

# sell
number_of_stocks_sell = 9
price_sell = 279.9

# prowizje
commission_buy = number_of_stocks_buy * price_buy * COMISSION_THRESHOLD
commission_sell = number_of_stocks_sell * price_sell * COMISSION_THRESHOLD

print('commission_buy:', commission_buy)
print('commission_sell:', commission_sell)

# rezultaty bez prowizji
revenue_without_commission = number_of_stocks_sell * price_sell
cost_without_commission = number_of_stocks_buy * price_buy
profit_without_commission = round(revenue_without_commission - cost_without_commission, 4)


print('revenue_without_commission:', revenue_without_commission)
print('cost_without_commission:', cost_without_commission)
print('profit_without_commission:', profit_without_commission)

# rezultaty z prowizją
revenue_with_commission = revenue_without_commission - commission_sell
cost_with_commission = cost_without_commission + commission_buy

print('revenue_with_commission:', revenue_with_commission)
print('cost_with_commission:', cost_with_commission)

profit_with_commission = revenue_with_commission - cost_with_commission

profit_with_commission_after_tax = profit_with_commission * (1 - BELKA_TAX)

print('profit_with_commission:', profit_with_commission)
print('profit_with_commission_after_tax:', profit_with_commission_after_tax)

