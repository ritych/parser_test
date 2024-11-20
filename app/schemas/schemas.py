"""Pydantic schemas."""
# STDLIB
from typing import List

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


class ReportAllSchema(BaseSchema):
    id: int
    date: str
    report: str


class ReportCreateSchema(BaseSchema):
    date: str
    report: str


class ReportGetAllSchema(BaseSchema):
    reports: List[ReportAllSchema]
