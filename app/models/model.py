from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass


class SalesReport(Base):
    __tablename__ = "sales_report"

    id_: Mapped[int] = mapped_column(name='id', primary_key=True)
    date: Mapped[str] = mapped_column(nullable=False)
    report: Mapped[str] = mapped_column(nullable=False)


class SalesData(Base):
    __tablename__ = "sales_data"

    id_: Mapped[int] = mapped_column(name='id', primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=True, default=0)
    price: Mapped[float] = mapped_column(nullable=True, default=0)
    category: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
