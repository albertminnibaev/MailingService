from fastapi import APIRouter, Depends, UploadFile, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.mailing.crud import NotificationCRUD
from src.mailing.schemas import NotificationCreate, NotificationIn
from src.tasks import send_email_task, send_telegram_task

router = APIRouter(
    prefix="/api",
    tags=["mailing"],
)


@router.post(
    path="/notify/",
    summary="Зарегистрировать уведомление",
    status_code=status.HTTP_200_OK
)
async def create_notification(
        notification_in: NotificationIn,
        db_session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if not isinstance(notification_in.recipient, list):
        list_of_recipients = [notification_in.recipient]
    else:
        list_of_recipients = notification_in.recipient

    if notification_in.delay == 1:
        delay_in_sending = 60 * 60
    elif notification_in.delay == 2:
        delay_in_sending = 24 * 60 * 60
    else:
        delay_in_sending = 0

    try:
        for recipient in list_of_recipients:
            notification_data = NotificationCreate(
                message=notification_in.message,
                recipient=recipient,
                delay=notification_in.delay
            )
            notification = await NotificationCRUD.add(db_session=db_session, data=notification_data)
            if notification.recipient.isdigit():
                result = send_telegram_task.apply_async(args=(notification.message, notification.recipient,), countdown=delay_in_sending)
            else:
                result = send_email_task.apply_async(args=(notification.message, notification.recipient,), countdown=delay_in_sending)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Не удалось отправить уведомление"
        ) from ex
    else:
        return {'message': 'Уведомление успешно отправлено!'}
