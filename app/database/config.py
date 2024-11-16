"""Этот модуль содержит базовый класс настроек сессии."""

# THIRDPARTY
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.pool import NullPool

ASYNC_DRIVER = 'postgresql+asyncpg'
ENV_FILENAME = '../.env'


class Settings(BaseSettings):
    """Класс для настройки переменных окружения для подключения к БД>."""
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    model_config = SettingsConfigDict(extra='ignore')

    def get_db_url(self) -> URL:
        """Формирует URL подключения к базе данных."""
        return URL.create(
            drivername=ASYNC_DRIVER,
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db
        )

    def get_engine(self, use_null_pool: bool = False) -> AsyncEngine:
        """Создает движок асинхронной сессии с выбором типа пула."""
        pool_class = NullPool if use_null_pool else None
        return create_async_engine(url=self.get_db_url(), poolclass=pool_class)

    def get_sessionmaker(self) -> async_sessionmaker:
        """Создает и возвращает асинхронную сессию."""
        return async_sessionmaker(
            bind=self.get_engine(),
            expire_on_commit=False,
            class_=AsyncSession
        )

    def get_session(self) -> AsyncSession:
        """Возвращает сессию подключения к БД."""
        return self.get_sessionmaker()()


class SettingsProdEnvironment(Settings):
    """Класс для настройки подключения к основной базе данных."""
    model_config = ConfigDict(env_file=ENV_FILENAME)


settings = SettingsProdEnvironment()
