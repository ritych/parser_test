# THIRDPARTY
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.models.model import SalesReport
from app.schemas.schemas import ReportCreateSchema


class ReportDAL:
    """Класс с функциями CRUD для таблицы репортов"""
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_report(self, report_data: ReportCreateSchema) -> SalesReport:
        """Создание отчета"""
        new_data = SalesReport(
            date=report_data.date,
            report=report_data.report,
        )
        self.session.add(new_data)
        await self.session.commit()
        return new_data

    async def get_all_reports(self):
        """Получить все отчеты"""
        result = await self.session.execute(
            select(SalesReport)
        )
        reports = result.scalars().all()
        await self.session.close()
        return reports

    async def get_report_by_date(self, date: str):
        """Получить отчет за указанную дату"""
        result = await self.session.execute(
            select(SalesReport).filter_by(date=date).limit(1)
        )
        report = result.scalar_one_or_none()
        await self.session.close()
        return report

    async def delete_report_by_id(self, id: int):
        """Удалить отчет по ID"""
        pass
