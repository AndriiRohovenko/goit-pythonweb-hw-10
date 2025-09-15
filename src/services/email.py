import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_verification_email(to_email: str, token: str):
    verification_link = f"{API_URL}/auth/verify-email?token={token}"
    subject = "Verify your email"
    body = f"Please click the link to verify your email: {verification_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "myApi_noReply@gmail.com"
    msg["To"] = to_email

    smtp_server = SMTP_HOST
    smtp_port = SMTP_PORT
    smtp_user = SMTP_USER
    smtp_password = SMTP_PASSWORD

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())
