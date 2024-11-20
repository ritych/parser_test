# THIRDPARTY
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.routers.dependencies import get_prod_session
from app.services.services import ReportService
from app.loggers.logger import logger

router = APIRouter(
    prefix='/api/v1',
    tags=['XMLParser']
)


@router.get("/")
async def get_all_report(session: AsyncSession = Depends(get_prod_session)):
    service = ReportService(session=session)
    result = await service.get_all_report()
    logger.info("Call @get_all_report()")
    return result


@router.post("/")
async def get_report_by_date(date: str, session: AsyncSession = Depends(get_prod_session)):
    service = ReportService(session=session)
    result = await service.get_report_by_date(date)
    logger.info(f"Call @get_report_by_date(date={date})")
    return result


@router.get("/healthcheck")
async def get_healthcheck():
    pass
