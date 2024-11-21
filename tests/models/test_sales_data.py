# THIRDPARTY
from hamcrest import assert_that, equal_to, is_, none
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.models.model import SalesData


class TestSalesData:
    """Интеграционные тесты для таблицы SalesData."""
    @pytest.mark.integtest
    @pytest.mark.asyncio
    async def test_create_sales_data(
            self,
            get_test_db: AsyncSession,
    ) -> None:
        """Тест создания новой записи в таблице SalesData."""
        await get_test_db.execute(
            text('TRUNCATE TABLE sales_data RESTART IDENTITY CASCADE')
        )
        await get_test_db.commit()

        sales_data = SalesData(
            name='Test SalesData',
            quantity=100,
            price=2.5,
            category='Car',
            date='2024-11-20',
        )
        get_test_db.add(sales_data)
        await get_test_db.commit()

        assert_that(
            actual_or_assertion=sales_data.name,
            matcher=equal_to('Test SalesData')
        )
        assert_that(
            actual_or_assertion=sales_data.category,
            matcher=equal_to('Car')
        )

    @pytest.mark.integtest
    @pytest.mark.asyncio
    async def test_read_sales_data(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест чтения записи из таблицы SalesData из базы данных."""
        sales_data = SalesData(
            name='Test SalesData',
            quantity=100,
            price=2.5,
            category='Car',
            date='2024-11-20',
        )
        get_test_db.add(sales_data)
        await get_test_db.commit()

        fetched_sales_data = await get_test_db.get(
            SalesData, sales_data.id_
        )

        assert_that(
            actual_or_assertion=fetched_sales_data.id_,
            matcher=equal_to(sales_data.id_)
        )
        assert_that(
            actual_or_assertion=fetched_sales_data.name,
            matcher=equal_to(sales_data.name)
        )
        assert_that(
            actual_or_assertion=fetched_sales_data.category,
            matcher=equal_to(sales_data.category)
        )

    @pytest.mark.integtest
    @pytest.mark.asyncio
    async def test_update_sales_data(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест обновления записи в таблице SalesData."""
        sales_data = SalesData(
            name='Test SalesData',
            quantity=100,
            price=2.5,
            category='Car',
            date='2024-11-20',
        )
        get_test_db.add(sales_data)
        await get_test_db.commit()

        new_name = 'Updated SalesData'
        sales_data.name = new_name
        get_test_db.add(sales_data)
        await get_test_db.commit()

        assert_that(
            actual_or_assertion=sales_data.name,
            matcher=equal_to(new_name)
        )

    @pytest.mark.integtest
    @pytest.mark.asyncio
    async def test_delete_sales_data(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест удаления записи из таблицы SalesData."""
        sales_data = SalesData(
            name='Test SalesData',
            quantity=100,
            price=2.5,
            category='Car',
            date='2024-11-20',
        )
        get_test_db.add(sales_data)
        await get_test_db.commit()

        await get_test_db.delete(sales_data)
        await get_test_db.commit()

        fetched_sales_data = await get_test_db.get(
            SalesData, sales_data.id_
        )
        assert_that(
            actual_or_assertion=fetched_sales_data,
            matcher=is_(none())
        )
