import re

from pydantic import BaseModel, field_validator, Field

from src.mailing.constants import SendingStatus


class NotificationIn(BaseModel):
    message: str
    recipient: str | list[str]
    delay: int

    @field_validator("delay")
    @classmethod
    def validate_delay(cls, values: int) -> int:
        if values not in [0, 1, 2]:
            raise ValueError('Неправильный формат задержки отправки.')
        return values

    @field_validator("recipient")
    @classmethod
    def validate_recipient(cls, values: str | list[str]) -> str | list[str]:
        if len(values) > 0:
            if isinstance(values, list):
                for recipient in values:
                    if re.match(r'^[\w\.-]+@[\w\.-]+$', recipient) or recipient.isdigit():
                        continue
                    else:
                        raise ValueError('Неправильный формат адреса получателя.')
                return values
            else:
                if re.match(r'^[\w\.-]+@[\w\.-]+$', values) or values.isdigit():
                    return values
                else:
                    raise ValueError('Неправильный формат адреса получателяm.')
        else:
            raise ValueError('Аадрес получателя не был передан.')


class NotificationCreate(BaseModel):
    message: str
    recipient: str
    delay: int

    class Config:
        model_config = True


class NotificationUpdate(BaseModel):
    message: str | None = Field(None)
    recipient: str | list[str] | None = Field(None)
    delay: int | None = Field(None)
    sending_status: SendingStatus | None = Field(None)
    task_id: str | None = Field(None)

    class Config:
        model_config = True
