import os
from typing import Any, Dict

import emails
from emails.template import JinjaTemplate

from app.core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {
        "host": settings.SMTP_HOST,
        "port": settings.SMTP_PORT,
        "tls": settings.SMTP_TLS,
        "user": settings.SMTP_USER,
        "password": settings.SMTP_PASSWORD,
    }

    message.send(to=email_to, render=environment, smtp=smtp_options)


def send_token(email_to: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Sign in."
    link = f"{settings.FRONTEND_HOST}/callback/email?token={token}"

    with open(os.path.abspath(path=settings.EMAIL_TEMPLATES_DIR + "sign_in.html")) as f:
        template_str = f.read()

    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "link": link,
        },
    )
