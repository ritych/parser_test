# THIRDPARTY
from hamcrest import assert_that, equal_to, is_, none
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.models.model import SalesReport


class TestSalesReport:
    """Интеграционные тесты для таблицы SalesReport."""
    @pytest.mark.integtest
    @pytest.mark.asyncio
    async def test_create_sales_report(
            self,
            get_test_db: AsyncSession,
    ) -> None:
        """Тест создания новой записи в таблице SalesReport."""
        await get_test_db.execute(
            text('TRUNCATE TABLE sales_report RESTART IDENTITY CASCADE')
        )
        await get_test_db.commit()

        sales_report = SalesReport(
            date='2024-11-20',
            report='This is report',
        )
        get_test_db.add(sales_report)
        await get_test_db.commit()

        assert_that(
            actual_or_assertion=sales_report.date,
            matcher=equal_to('2024-11-20')
        )
        assert_that(
            actual_or_assertion=sales_report.report,
            matcher=equal_to('This is report')
        )

    @pytest.mark.integtest
    @pytest.mark.asyncio
    async def test_read_sales_report(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест чтения записи из таблицы SalesReport из базы данных."""
        sales_report = SalesReport(
            date='2024-11-20',
            report='This is report',
        )
        get_test_db.add(sales_report)
        await get_test_db.commit()

        fetched_sales_report = await get_test_db.get(
            SalesReport, sales_report.id_
        )

        assert_that(
            actual_or_assertion=fetched_sales_report.id_,
            matcher=equal_to(sales_report.id_)
        )
        assert_that(
            actual_or_assertion=fetched_sales_report.date,
            matcher=equal_to(sales_report.date)
        )
        assert_that(
            actual_or_assertion=fetched_sales_report.report,
            matcher=equal_to(sales_report.report)
        )

    @pytest.mark.integtest
    @pytest.mark.asyncio
    async def test_update_sales_report(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест обновления записи в таблице SalesReport."""
        sales_report = SalesReport(
            date='2024-11-20',
            report='This is report',
        )
        get_test_db.add(sales_report)
        await get_test_db.commit()

        new_report = 'Updated report'
        sales_report.report = new_report
        get_test_db.add(sales_report)
        await get_test_db.commit()

        assert_that(
            actual_or_assertion=sales_report.report,
            matcher=equal_to(new_report)
        )

    @pytest.mark.integtest
    @pytest.mark.asyncio
    async def test_delete_sales_report(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест удаления записи из таблицы SalesReport."""
        sales_report = SalesReport(
            date='2024-11-20',
            report='This is report',
        )
        get_test_db.add(sales_report)
        await get_test_db.commit()

        await get_test_db.delete(sales_report)
        await get_test_db.commit()

        fetched_sales_report = await get_test_db.get(
            SalesReport, sales_report.id_
        )
        assert_that(
            actual_or_assertion=fetched_sales_report,
            matcher=is_(none())
        )
