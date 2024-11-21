# THIRDPARTY
from hamcrest import assert_that, equal_to, is_not, none
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.dal.sales_data import SalesDAL
from app.schemas.schemas import SalesdataAllSchema


@pytest.mark.asyncio
@pytest.mark.integtest
class TestSalesDAL:
    """Класс интеграционных тестов для Data Access Layer данных о продаже."""
    async def test_create_sales_data(
            self,
            get_test_db: AsyncSession
    ) -> None:
        """Тест создания нового направления в базе данных.

        Этот тест проверяет, что метод `create_sales_data` в `SalesDAL` корректно
        создаёт запись в базе данных с указанными полями. После создания записи
        выполняется проверка на соответствие значений полей записи с ожидаемыми
        данными
        """
        dal = SalesDAL(session=get_test_db)

        sales_data = SalesdataAllSchema(
            name='Test SalesData',
            quantity=100,
            price=2.5,
            category='Car',
            date='2024-11-20',
        )

        new_sales_data = await dal.create_sales_data(sales_data=sales_data)

        assert_that(
            actual_or_assertion=new_sales_data,
            matcher=is_not(none())
        )

        assert_that(
            actual_or_assertion=new_sales_data.name,
            matcher=equal_to('Test SalesData')
        )
        assert_that(
            actual_or_assertion=new_sales_data.category,
            matcher=equal_to('Car')
        )
        assert_that(
            actual_or_assertion=new_sales_data.quantity,
            matcher=equal_to(100)
        )
        assert_that(
            actual_or_assertion=new_sales_data.price,
            matcher=equal_to(2.5)
        )
        assert_that(
            actual_or_assertion=new_sales_data.date,
            matcher=equal_to('2024-11-20')
        )
