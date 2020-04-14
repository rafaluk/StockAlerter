import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.utils import calc_time, Constants
from app.calculator import Calculator


@calc_time
def send_email(login, password, recipient, subject, message, config):

    server = smtplib.SMTP(host=config['smtp']['host'],
                          port=config['smtp']['port'])
    server.starttls()
    server.login(login, password)

    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server.send_message(msg)
    # todo: print this only if no errors
    print('Email sent.')
    server.quit()

    del msg


def compose_min_max_message(calculator, current_value, currency='PLN'):
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


def compose_daily_message(stocks, currency='PLN'):
    message = ''
    for key, value in stocks.items():
        message += key + ': ' + value + f' {currency}'
    return message


def prepare_min_max_email(user, symbol, current_value, global_min, global_max, config, calculator):

    message = compose_min_max_message(calculator, current_value)
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


def prepare_daily_email(user, stocks, config):
    message = compose_daily_message(stocks)
    send_email(login=Constants.LOGIN, password=Constants.PASSWORD, recipient=user,
               subject='Daily summary', message=message, config=config)
