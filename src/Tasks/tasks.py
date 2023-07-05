from src.Tasks.app_celery import celery
from src.config import SMTP_USER, SMTP_HOST, SMTP_PASS, SMTP_PORT
from src.Tasks.email_templates import create_verified_email
import smtplib
from typing import Annotated


@celery.task
def send_verified_email(email_to: str) -> None:
    email_from = SMTP_USER
    message = create_verified_email(email_to, email_from)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(message)

