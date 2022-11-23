import os
import pathlib
from pydantic import BaseSettings

ROOT_DIRECTORY = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    API_V1_NAME: str = "/api/v1"
    SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', default="sqlite:///db.sqlite3")

    MAIL_USERNAME = os.getenv('MAIL_USERNAME', default="example")
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', default="")
    MAIL_FROM = os.getenv('MAIL_FROM', default='example@mail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', default=587)
    MAIL_SERVER = os.getenv('MAIL_SERVER', default='smtp.gmail.com')
    MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME', default='FastAPI Backend')
    MAIL_TLS = os.getenv('MAIL_TLS', default=True)

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", default="secret_1234567899")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', default=30)
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY", default="secret_1234567899")  # should be kept secret

    class Config:
        case_sensitive = True


settings = Settings()
