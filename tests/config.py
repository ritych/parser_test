# THIRDPARTY
from pydantic_settings import SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# FIRSTPARTY
from app.database.config import Settings as PostgresSettings

ENV_FILENAME = '.test.env'


class SettingsTestPostgresEnvironment(PostgresSettings):
    """Класс для настройки подключения к тестовой базе данных."""
    model_config = SettingsConfigDict(env_file=ENV_FILENAME)

    def get_sessionmaker(self) -> async_sessionmaker:
        """Создает и возвращает асинхронную сессию с использованием NullPool.

        Returns:
            session(AsyncSession).
        """
        return async_sessionmaker(
            self.get_engine(use_null_pool=True),
            expire_on_commit=False,
            class_=AsyncSession
        )


settings = SettingsTestPostgresEnvironment()
