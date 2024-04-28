from typing import Optional

from pydantic import BaseSettings, EmailStr

APP_TITLE = 'Благотворительный фонд'
DATABASE_URL = 'sqlite+aiosqlite:///./charity_fund.db'
DESCRIPTION = 'Сервис для поддержки!'
SECRET = 'SECRET'


class Settings(BaseSettings):
    app_title: str = APP_TITLE
    database_url: str = DATABASE_URL
    description: str = DESCRIPTION
    secret: str = SECRET
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
