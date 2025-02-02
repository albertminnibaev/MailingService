from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi import status, HTTPException
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from celery.result import AsyncResult

from src.config import mail_settings, telegramm_settings
from src.mailing.crud import NotificationCRUD
from src.mailing.models import Notification
from src.mailing.schemas import NotificationUpdate

conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.MAIL_USERNAME,
    MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
    MAIL_FROM=mail_settings.MAIL_FROM,
    MAIL_PORT=mail_settings.MAIL_PORT,
    MAIL_SERVER=mail_settings.MAIL_SERVER,
    MAIL_FROM_NAME=mail_settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=mail_settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=mail_settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=mail_settings.USE_CREDENTIALS,
    VALIDATE_CERTS=mail_settings.VALIDATE_CERTS
)


async def send_mail(
        text_message: str,
        recipient: str
):
    try:
        message = MessageSchema(
            subject="New message",
            recipients=[recipient],
            body=text_message,
            subtype=MessageType.plain
        )

        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Error sending email: {ex}"
        ) from ex


async def send_telegram_base(
        text_message: str,
        recipient: str
):
    data = {
        "chat_id": recipient,
        "text": text_message
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"https://api.telegram.org/bot{telegramm_settings.TELEGRAMM_KEY}/sendMessage",
                                    data=data) as response:
                print(response.status)
        except aiohttp.ClientError as ex:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Не удалось отправить уведомление"
            ) from ex


async def update_notifications(
        db_session: AsyncSession,
        notification: Notification,
        result
) -> None:
    task_id = result.task_id
    res = AsyncResult(task_id)
    update_data = NotificationUpdate(sending_status=res.state, task_id=task_id)
    await NotificationCRUD.update(db_session=db_session, data_id=notification.id, data=update_data)
