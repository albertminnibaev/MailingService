import os
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent


class DatabaseSettings(BaseSettings):
    load_dotenv()
    db_name: str = os.getenv('POSTGRES_DB')
    db_user: str = os.getenv('POSTGRES_USER')
    db_pass: str = os.getenv('POSTGRES_PASSWORD')
    db_host: str = os.getenv('POSTGRES_HOST')
    db_port: int = os.getenv('POSTGRES_PORT')
    db_url: str = f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    db_echo: bool = os.getenv('DB_ECHO', False) == 'True'
    BASE_DIR: Path = Path(__file__).parent.parent


class MailSettings(BaseSettings):
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')
    MAIL_FROM: str = os.getenv('MAIL_FROM')
    MAIL_PORT: str = os.getenv('MAIL_PORT')
    MAIL_SERVER: str = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME: str = os.getenv('MAIL_FROM_NAME')
    MAIL_STARTTLS: bool = os.getenv('MAIL_STARTTLS')
    MAIL_SSL_TLS: bool = os.getenv('MAIL_SSL_TLS')
    USE_CREDENTIALS: bool = os.getenv('USE_CREDENTIALS')
    VALIDATE_CERTS: bool = os.getenv('VALIDATE_CERTS')


class TelegrammSettings(BaseSettings):
    TELEGRAMM_KEY: str = os.getenv('TELEGRAMM_KEY')


class RedisSetting(BaseSettings):
    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: int = os.getenv('REDIS_PORT')


class LoggingSettings(BaseSettings):
    log_dir: Path = BASE_DIR / 'logs'


database_settings = DatabaseSettings()
mail_settings = MailSettings()
telegramm_settings = TelegrammSettings()
redis_settings = RedisSetting()
logging_settings = LoggingSettings()
