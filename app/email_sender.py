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
    # todo: add last value of given stock
    return f'Current_value:\t\t\t{current_value} {currency}\n' \
        f'Change:\t\t\t\t{calculator.change()}%\n' \
        f'Commission buy:\t\t\t{calculator.commissions()[0]} {currency}\n' \
        f'Commission sell:\t\t{calculator.commissions()[1]} {currency}\n' \
        f'Revenue without commission:\t{calculator.results_without_commission()[0]} {currency}\n' \
        f'Cost without commission:\t{calculator.results_without_commission()[1]} {currency}\n' \
        f'Profit without commission:\t{calculator.results_without_commission()[2]} {currency}\n' \
        f'Revenue with commission:\t{calculator.results_with_commission()[0]} {currency}\n' \
        f'Cost with commission:\t\t{calculator.results_with_commission()[1]} {currency}\n' \
        f'Profit with commission:\t\t{calculator.results_with_commission()[2]} {currency}\n' \
        f'Profit after tax (19%):\t\t{calculator.profit_after_tax()} {currency}\n'


def prepare_min_max_email(symbol, current_value, global_min, global_max, config, calculator):

    message = compose_min_max_message(calculator, current_value)
    print(message)

    if current_value > global_max:
        subject = f'[{symbol}] New Max. Profit: {calculator.profit_after_tax()}'
        send_email(login=Constants.LOGIN, password=Constants.PASSWORD, recipient=Constants.MY_EMAIL,
                   subject=subject, message=message, config=config)

    elif current_value < global_min:
        subject = f'[{symbol}] New Min. Profit: {calculator.profit_after_tax()}'
        send_email(login=Constants.LOGIN, password=Constants.PASSWORD, recipient=Constants.MY_EMAIL,
                   subject=subject, message=message, config=config)

    else:
        print("Email not sent.")


def prepare_daily_email(user, current_value, config):
    send_email(login=Constants.LOGIN, password=Constants.PASSWORD, recipient=Constants.MY_EMAIL,
               subject='DAILY TEST', message='', config=config)
