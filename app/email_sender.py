import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.main import LOGIN, PASSWORD, MY_EMAIL
from app.utils import calc_time


@calc_time
def send_email(login, password, recipient, subject, message):
    # setup and start a SMTP server
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
    server.quit()

    del msg


def compare_and_send(current_value, global_min, global_max):
    if current_value > global_max:
        subject = 'New global maximum'
        message = f'Current_value: {current_value} > {global_max} (global_max)'
        print(message)
        send_email(login=LOGIN, password=PASSWORD, recipient=MY_EMAIL,
                   subject=subject, message=message)

    elif current_value < global_min:
        subject = 'New global minimum'
        message = f'Current_value: {current_value} < {global_min} (global_max)'
        print(message)
        send_email(login=LOGIN, password=PASSWORD, recipient=MY_EMAIL,
                   subject=subject, message=message)

    else:
        message = f'Current_value: {current_value}.'
        print(message + "; email not sent.")