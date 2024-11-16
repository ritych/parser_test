# THIRDPARTY
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.dal.sales_data import SalesDAL
from app.models.model import SalesData
from app.schemas.schemas import SalesdataAllSchema
from app.services.http_exceptions import (
    exception_400_validation,
    exception_500_db_connection
)


class SalesdataService:
    def __init__(self, session: AsyncSession) -> None:
        self.__dal = SalesDAL(session=session)

    async def create_sales_data(
            self,
            sales_data: SalesdataAllSchema
    ) -> SalesData:
        try:
            new_sales_data = await self.__dal.create_sales_data(sales_data=sales_data)
            return new_sales_data
        except ConnectionError:
            raise exception_500_db_connection
        except ValueError:
            raise exception_400_validation
