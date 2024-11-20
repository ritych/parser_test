# THIRDPARTY
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.models.model import SalesData
from app.schemas.schemas import SalesdataAllSchema


class SalesDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_sales_data(self, sales_data: SalesdataAllSchema) -> SalesData:
        new_data = SalesData(
            name=sales_data.name,
            quantity=sales_data.quantity,
            price=sales_data.price,
            category=sales_data.category,
            date=sales_data.date,
        )
        self.session.add(new_data)
        await self.session.commit()
        return new_data

    async def delete_sales_data(self, id: int) -> SalesData:
        pass
