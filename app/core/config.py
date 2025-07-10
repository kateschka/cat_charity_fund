from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = 'QRKot'
    app_description: str = (
        'QRKot - это сервис для пожертвований на благотворительные проекты.'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'root@admin.ru'
    first_superuser_password: Optional[str] = 'root'

    class Config:
        """Конфигурация Pydantic."""

        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
