from email.message import EmailMessage

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from src.config import SMTP_USER


def create_verified_email(email_to, email_from, confirm_token):
    email = EmailMessage()
    environment = Environment(loader=FileSystemLoader("src/Templates/"))
    template = environment.get_template("email.html")
    email["Subject"] = "Верификация пользователя"
    email["From"] = SMTP_USER
    email["To"] = email_to
    email.set_content(template.render(token=confirm_token), subtype='html')
    return email

