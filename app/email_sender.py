import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.utils import calculate_time


@calculate_time
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
    # todo: print this only if no errors (try/except)
    print('Email sent.')
    server.quit()

    del msg

