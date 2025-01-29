from fastapi import APIRouter, Depends, UploadFile, status, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.mailing.crud import NotificationCRUD
from src.mailing.schemas import NotificationCreate, NotificationIn
from src.mailing.services import send_telegram, send_mail

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
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    try:
        if not isinstance(notification_in.recipient, list):
            list_of_recipients = [notification_in.recipient]
        else:
            list_of_recipients = notification_in.recipient
        for recipient in list_of_recipients:
            notification_data = NotificationCreate(
                message=notification_in.message,
                recipient=recipient,
                delay=notification_in.delay
            )
            notification = await NotificationCRUD.add(db_session=db_session, data=notification_data)
            if notification.recipient.isdigit():
                await send_telegram(notification=notification, background_tasks=background_tasks)
            else:
                await send_mail(notification=notification, background_tasks=background_tasks)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Не удалось отправить уведомление"
        ) from ex
    else:
        return {'message': 'Уведомление успешно отправлено!'}