# THIRDPARTY
from hamcrest import assert_that, equal_to, is_not, none
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.dal.sales_report import ReportDAL
from app.models.model import SalesReport
from app.schemas.schemas import ReportCreateSchema


@pytest.mark.asyncio
@pytest.mark.integtest
class TestSalesDAL:
    """Класс интеграционных тестов для Data Access Layer данных о репортах."""
    async def test_create_report(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест создания нового репорта в базе данных."""
        dal = ReportDAL(session=get_test_db)

        report = ReportCreateSchema(
            date='2024-11-20',
            report='This is report'
        )

        new_report = await dal.create_report(report_data=report)

        assert_that(
            actual_or_assertion=new_report,
            matcher=is_not(none())
        )

        assert_that(
            actual_or_assertion=new_report.date,
            matcher=equal_to('2024-11-20')
        )
        assert_that(
            actual_or_assertion=new_report.report,
            matcher=equal_to('This is report')
        )

    async def test_get_all_reports(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест получения всех отчетов."""
        async with get_test_db as session:
            dal = ReportDAL(session=session)
            # Очистка таблицы направлений перед тестом
            await get_test_db.execute(statement=text('DELETE FROM sales_report'))
            await get_test_db.commit()

            # Добавляем тестовые данные для репортов
            test_reports = [
                SalesReport(date='2024-11-20', report='Report 1'),
                SalesReport(date='2024-11-19', report='Report 2')
            ]
            session.add_all(test_reports)
            await session.commit()

            # Получение всех репортов
            reports = await dal.get_all_reports()

            # Проверка количества репортов в базе
            assert_that(
                actual_or_assertion=len(reports),
                matcher=equal_to(2)
            )

            # Проверка данных каждого репорта
            assert_that(
                actual_or_assertion=reports[0].date,
                matcher=equal_to('2024-11-20')
            )
            assert_that(
                actual_or_assertion=reports[0].report,
                matcher=equal_to('Report 1')
            )
            assert_that(
                actual_or_assertion=reports[1].date,
                matcher=equal_to('2024-11-19')
            )
            assert_that(
                actual_or_assertion=reports[1].report,
                matcher=equal_to('Report 2')
            )

    async def test_get_report_by_date(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест получения отчета по дате."""
        dal = ReportDAL(session=get_test_db)
        new_report = SalesReport(
            date='2024-11-20',
            report='Test report'
        )
        get_test_db.add(new_report)
        await get_test_db.commit()

        result_report = await dal.get_report_by_date(date='2024-11-20')

        assert_that(
            actual_or_assertion=result_report.date,
            matcher=equal_to('2024-11-20')
        )
