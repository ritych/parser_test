# THIRDPARTY
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.routers.dependencies import get_prod_session
from app.schemas.schemas import SalesdataAllSchema
from app.services.services import SalesdataService
from app.tasks import parse_sales_data, insert_data_to_db, get_report

router = APIRouter(
    prefix='/api/v1',
    tags=['XMLParser']
)


@router.get("/")
async def root():
    return {"message": "Sales Analysis Service"}


@router.post("/fetch-sales-data/")
async def fetch_sales_data(url: str, session: AsyncSession = Depends(get_prod_session)):
    # fetch_and_process_sales_data.delay(url, session)
    # parse_sales_data(url, session)
    parsed_data = await parse_sales_data(url)
    await insert_data_to_db(parsed_data, session)
    get_report.delay()
    # print(work.get(timeout=10))

    return {"message": f"{url} has been fetched"}


@router.delete("/fetch-sales-data/{id}")
async def fetch_sales_data(id: str):
    pass
