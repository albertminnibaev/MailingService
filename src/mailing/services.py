from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi import BackgroundTasks, status, HTTPException
import aiohttp

from src.config import settings

from src.mailing.models import Notification

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)


async def send_mail(
        background_tasks: BackgroundTasks,
        notification: Notification,
):
    text_message = notification.message

    try:
        message = MessageSchema(
            subject="New message",
            recipients=[notification.recipient],
            body=text_message,
            subtype=MessageType.plain
        )

        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Error sending email: {ex}"
        ) from ex


async def send_telegram_base(
        notification: Notification,
):
    data = {
        "chat_id": notification.recipient,
        "text": notification.message
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"https://api.telegram.org/bot{settings.TELEGRAMM_KEY}/sendMessage",
                                    data=data) as response:
                print(response.status)
        except aiohttp.ClientError as ex:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Не удалось отправить уведомление"
            ) from ex


async def send_telegram(
        notification: Notification,
        background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_telegram_base, notification)
