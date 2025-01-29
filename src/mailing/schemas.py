from pydantic import BaseModel


class NotificationIn(BaseModel):
    message: str
    recipient: str | list[str]
    delay: int


class NotificationCreate(BaseModel):
    message: str
    recipient: str
    delay: int

    class Config:
        model_config = True
