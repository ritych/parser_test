"""Общие зависимости для всех роутеров."""
# THIRDPARTY
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.database.config import settings


async def get_prod_session() -> AsyncSession:
    async with settings.get_session() as session:
        yield session
