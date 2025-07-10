from typing import Optional
from pydantic import EmailStr, Field
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = None
    app_description: str = None
    database_url: str = Field(
        default='sqlite+aiosqlite:///./fastapi.db', env='DATABASE_URL')
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'root@admin.ru'
    first_superuser_password: Optional[str] = 'root'

    class Config:
        """Конфигурация Pydantic."""

        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
