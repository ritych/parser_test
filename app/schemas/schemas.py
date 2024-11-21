"""Pydantic schemas."""
# STDLIB
from typing import List, Dict

# FIRSTPARTY
from app.schemas.base import BaseSchema


class SalesdataAllSchema(BaseSchema):
    """Схема полной записи данных о продаже"""
    name: str
    quantity: int
    price: float
    category: str
    date: str


class ReportAllSchema(BaseSchema):
    """Схема полной информации о репорте"""
    id: int
    date: str
    report: str


class ReportCreateSchema(BaseSchema):
    """Схема для добавления репорта в БД"""
    date: str
    report: str


class ReportDataSchema(BaseSchema):
    """Схема результат парсинга для генерации репорта"""
    products: List[SalesdataAllSchema]
    date: str
    total_revenue: float
    categories: Dict


class DateByPostSchema(BaseSchema):
    date: str
