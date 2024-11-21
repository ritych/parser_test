# THIRDPARTY
from fastapi import status
from hamcrest import assert_that, contains_string, equal_to
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.main import app
from app.schemas.schemas import DateByPostSchema


@pytest.mark.asyncio
@pytest.mark.integtest
class TestRouters:
    """Класс для тестирования API"""
    async def test_get(self, get_test_db: AsyncSession) -> None:
        async with AsyncClient(
                transport=ASGITransport(app=app), base_url='http://test'
        ) as client:
            response = await client.get(
                '/api/v1/'
            )

        assert_that(
            actual_or_assertion=response.status_code,
            matcher=equal_to(status.HTTP_200_OK)
        )

    async def test_post(self, get_test_db: AsyncSession) -> None:
        date = DateByPostSchema(date="2024-11-20")

        async with AsyncClient(
                transport=ASGITransport(app=app), base_url='http://test'
        ) as client:
            response = await client.post(
                '/api/v1/',
                json=date.model_dump()
            )

        assert_that(
            actual_or_assertion=response.status_code,
            matcher=equal_to(status.HTTP_422_UNPROCESSABLE_ENTITY)
        )

    async def test_healthcheck(self, get_test_db: AsyncSession) -> None:
        pass
