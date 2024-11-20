# THIRDPARTY
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.dal.sales_data import SalesDAL
from app.dal.sales_report import ReportDAL
from app.models.model import SalesData, SalesReport
from app.schemas.schemas import SalesdataAllSchema, ReportCreateSchema
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


class ReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.__dal = ReportDAL(session=session)

    async def create_report(
            self,
            report_data: ReportCreateSchema
    ) -> SalesReport:
        try:
            new_report_data = await self.__dal.create_report(report_data=report_data)
            return new_report_data
        except ConnectionError:
            raise exception_500_db_connection
        except ValueError:
            raise exception_400_validation

    async def get_all_report(self):
        try:
            reports = await self.__dal.get_all_reports()
            return reports
        except ConnectionError:
            raise exception_500_db_connection
        except ValueError:
            raise exception_400_validation

    async def get_report_by_date(self, date: str):
        try:
            report = await self.__dal.get_report_by_date(date=date)
            return report
        except ConnectionError:
            raise exception_500_db_connection
        except ValueError:
            raise exception_400_validation
