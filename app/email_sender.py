import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.utils import calc_time, Constants
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


def compare_and_send(current_value, global_min, global_max):
    # todo: add some global counter, so every X times mail is sent anyway
    # todo: extract these values
    c = Calculator(9, 271.1, 9, current_value)

    message = compose_message(c, current_value)
    print(message)

    if current_value > global_max:
        subject = f'New Max. Profit: {c.profit_after_tax()}'
        send_email(login=Constants.LOGIN, password=Constants.PASSWORD, recipient=Constants.MY_EMAIL,
                   subject=subject, message=message)

    elif current_value < global_min:
        subject = f'New Min. Profit: {c.profit_after_tax()}'
        send_email(login=Constants.LOGIN, password=Constants.PASSWORD, recipient=Constants.MY_EMAIL,
                   subject=subject, message=message)

    else:
        print("Email not sent.")
