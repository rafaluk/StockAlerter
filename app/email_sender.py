import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.utils import calc_time
from app.calculator import Calculator


@calc_time
def send_email(login, password, recipient, subject, message, test=False):
    if test: return
    # setup and start a SMTP server
    # todo: extract SMTP details to config file
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(login, password)

    # create the message
    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = recipient
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message
    server.send_message(msg)
    # todo: print this only if no errors
    print('Email sent.')
    server.quit()

    del msg


def compose_message(calculator: Calculator, current_value, currency='PLN'):
    return f'Current_value: {current_value} {currency}\n ' \
        f'Commission buy: {calculator.commissions()[0]} {currency}\n' \
        f'Commission sell: {calculator.commissions()[1]} {currency}\n' \
        f'revenue_without_commission: {calculator.results_without_commission()[0]} {currency}\n' \
        f'cost_without_commission: {calculator.results_without_commission()[1]} {currency}\n' \
        f'profit_without_commission: {calculator.results_without_commission()[2]} {currency}\n' \
        f'revenue_with_commission: {calculator.results_with_commission()[0]} {currency}\n' \
        f'cost_with_commission: {calculator.results_with_commission()[1]} {currency}\n' \
        f'profit_with_commission: {calculator.results_with_commission()[2]} {currency}\n'


def compare_and_send(current_value, global_min, global_max):
    import os
    # todo: add some global counter, so every X times mail is sent anyway

    # import environment variables
    LOGIN = os.environ.get('STOCK_ALERTER_LOGIN')
    PASSWORD = os.environ.get('STOCK_ALERTER_PASSWORD')
    MY_EMAIL = os.environ.get('MY_GMAIL')

    # todo: extract these values
    c = Calculator(9, 271.1, 9, current_value)

    message = compose_message(c, current_value)
    print(message)

    if current_value > global_max:
        subject = f'New Max. Profit: {c.profit_after_tax()}'
        send_email(login=LOGIN, password=PASSWORD, recipient=MY_EMAIL,
                   subject=subject, message=message)

    elif current_value < global_min:
        subject = f'New Min. Profit: {c.profit_after_tax()}'
        send_email(login=LOGIN, password=PASSWORD, recipient=MY_EMAIL,
                   subject=subject, message=message)

    else:
        print("Email not sent.")
