import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_MAIL, SMTP_HOST, SMTP_PORT
from utils.logger import getLogger


def send_scholar_rapport_by_mail(digest: str):
    logger = getLogger(__name__)
    logger.info("Logging to SMTP server...")
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    message_body = digest

    msg = MIMEMultipart()
    msg['From'] = 'Andrea Joly <andrea@andrea-joly.fr>'
    msg['To'] = RECIPIENT_MAIL
    msg['Subject'] = "☕️ Daily Article Suggestions" + date.today().strftime(" %d/%m/%Y")
    msg.attach(MIMEText(message_body, 'plain'))

    server.sendmail('andrea@andrea-joly.fr', RECIPIENT_MAIL, msg.as_string())

    server.quit()
    logger.info("Mail sent successfully.")
