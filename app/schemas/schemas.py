"""Pydantic schemas."""
# FIRSTPARTY
from app.schemas.base import BaseSchema


class SalesdataAllSchema(BaseSchema):
    """Схема полной записи данных о продаже
    Attributes:
        name (str)
        quantity (int)
        price (float)
        category (str)
        date (str)
    """
    name: str
    quantity: int
    price: float
    category: str
    date: str
