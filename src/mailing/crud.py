from src.crud import BaseCRUD
from src.mailing.models import Notification


class NotificationCRUD(BaseCRUD):
    model = Notification
