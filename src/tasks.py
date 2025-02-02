from src.database import get_async_session
from src.mailing.constants import SendingStatus
from src.mailing.crud import NotificationCRUD
from src.mailing.schemas import NotificationUpdate
from src.mailing.services import send_mail, send_telegram_base
from src.mailing.utilities import run_async
from src.project_celery import celery_app
from celery.result import AsyncResult


@celery_app.task(bind=True, track_started=True)
def send_email_task(
    self,
    text_message: str,
    recipient: str
):
    run_async(send_mail(text_message=text_message, recipient=recipient))
    return self.AsyncResult(self.request.id).state


@celery_app.task(bind=True, track_started=True)
def send_telegram_task(
    self,
    text_message: str,
    recipient: str
):
    run_async(send_telegram_base(text_message=text_message, recipient=recipient))
    return self.AsyncResult(self.request.id).state


@celery_app.task
def update_sending_status_for_notifications(
):
    async def update_notifications(
    ):
        async for db in get_async_session():
            notifications = await NotificationCRUD.get_all(db_session=db)
            for notification in notifications:
                if notification.sending_status not in (SendingStatus.SUCCESS, SendingStatus.FAILURE):
                    res = AsyncResult(notification.task_id)
                    print(res)
                    update_data = NotificationUpdate(sending_status=res.state)
                    await NotificationCRUD.update(db_session=db, data_id=notification.id, data=update_data)
    run_async(update_notifications())
