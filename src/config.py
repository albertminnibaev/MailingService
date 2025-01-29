import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    load_dotenv()
    db_name: str = os.getenv('POSTGRES_DB')
    db_user: str = os.getenv('POSTGRES_USER')
    db_pass: str = os.getenv('POSTGRES_PASSWORD')
    db_host: str = os.getenv('POSTGRES_HOST')
    db_port: int = os.getenv('POSTGRES_PORT')
    db_url: str = f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    db_echo: bool = os.getenv('DB_ECHO', False) == 'True'
    # SECRET_KEY: str = os.getenv('SECRET_KEY')
    BASE_DIR: Path = Path(__file__).parent.parent
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
    TELEGRAMM_KEY: str = os.getenv('TELEGRAMM_KEY')
    # log_dir: Path = BASE_DIR / 'logs'


settings = Settings()
