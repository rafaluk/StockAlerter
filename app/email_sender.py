import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_email(login, password, email_from, email_to, subject, message):
    # setup and start a SMTP server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(login, password)

    # create the message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message
    server.send_message(msg)
    server.quit()

    del msg
