from src.mailing.services import send_mail, send_telegram_base
from src.mailing.utilities import run_async
from src.project_celery import celery_app


@celery_app.task
def send_email_task(
    text_message: str,
    recipient: str
):
    run_async(send_mail(text_message=text_message, recipient=recipient))
    return "Уведомление по email отправлено"


@celery_app.task
def send_telegram_task(
    text_message: str,
    recipient: str
):
    run_async(send_telegram_base(text_message=text_message, recipient=recipient))
    return "Уведомление в телеграмм отправлено"
