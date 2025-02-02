from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.mailing.constants import SendingStatus
from src.models import Base


class Notification(Base):

    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    message: Mapped[str] = mapped_column(String, nullable=False)
    recipient: Mapped[str] = mapped_column(String, nullable=False)
    delay: Mapped[int] = mapped_column(Integer, nullable=False)
    sending_status: Mapped[Optional[SendingStatus]] = mapped_column(
        ENUM(
            SendingStatus
        ),
    )
    task_id = mapped_column(String)
