# THIRDPARTY
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.main import app
from app.models.model import Base
from app.routers.dependencies import get_prod_session

from tests.config import (
    SettingsTestPostgresEnvironment,
    settings
)


@pytest.fixture(scope='session', autouse=True)
async def setup_database() -> None:
    """Фикстура для подготовки тестовой базы данных."""
    test_engine = SettingsTestPostgresEnvironment().get_engine(
        use_null_pool=True
    )
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def get_test_db() -> AsyncSession:
    """Фикстура для создания экземпляра сессии базы данных для тестов."""
    test_session = SettingsTestPostgresEnvironment().get_sessionmaker()
    async with test_session() as session:
        yield session


async def override_get_session() -> AsyncSession:
    yield settings.get_session()


app.dependency_overrides[get_prod_session] = override_get_session
