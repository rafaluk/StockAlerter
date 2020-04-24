from app.email_sender import send_email
from app.utils import Constants


def compose_email_body(calculator, current_value, currency='PLN'):
    return f'Current price: {current_value} {currency}, ' \
        f'current value: {current_value} {currency} * {calculator.number_of_stocks_buy} = ' \
        f'{current_value*calculator.number_of_stocks_buy} {currency}\n' \
        f'Your price: {calculator.price_buy} {currency}, ' \
        f'you paid: {calculator.price_buy} {currency} * {calculator.number_of_stocks_buy} = ' \
        f'{calculator.price_buy*calculator.number_of_stocks_buy} {currency}\n' \
        f'Price change: {calculator.change()}% ({calculator.price_buy} {currency} -> {current_value} {currency})\n' \
        f'Commissions: {calculator.commissions()[0] + calculator.commissions()[1]} {currency} = ' \
        f'{calculator.commissions()[0]} {currency} (buy) + ' \
        f'{calculator.commissions()[1]} {currency} (sell)\n' \
        f'Profits: {calculator.results_without_commission()[2]} {currency} (without commision), ' \
        f'{calculator.results_with_commission()[2]} {currency} (with commision), ' \
        f'{calculator.profit_after_tax()} {currency} (after 19% tax)\n'


def prepare_min_max_email(user, symbol, current_value, global_min, global_max, config, calculator):

    message = compose_email_body(calculator, current_value)
    print(message)

    if current_value > global_max:
        subject = f'[{symbol}] New Max. Profit: {calculator.profit_after_tax()}'
        send_email(login=Constants.LOGIN, password=Constants.PASSWORD, recipient=user,
                   subject=subject, message=message, config=config)

    elif current_value < global_min:
        subject = f'[{symbol}] New Min. Profit: {calculator.profit_after_tax()}'
        send_email(login=Constants.LOGIN, password=Constants.PASSWORD, recipient=user,
                   subject=subject, message=message, config=config)

    else:
        print("Email not sent.")


def prepare_daily_email(user, stocks, calculators, config):
    message = ''
    total_profit = 0
    for calculator in calculators:
        total_profit += calculator.profit_after_tax()
        message += compose_email_body(stocks, calculator) + '-'*30 + '\n'
    print(message)
    subject = f'[DAILY] Total profit: {total_profit}'
    send_email(login=Constants.LOGIN, password=Constants.PASSWORD, recipient=user,
               subject=subject, message=message, config=config)
