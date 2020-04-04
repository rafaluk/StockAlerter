import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
