import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = "127.0.0.1"
SMTP_PORT = 1025
MAIL_DEFAULT_SENDER = "quiz-admin@donotreply.in"

def send_email(to, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = MAIL_DEFAULT_SENDER
    msg["To"] = to

    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.send_message(msg)
