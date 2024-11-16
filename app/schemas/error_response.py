"""Pydantic schemas for errors."""
# THIRDPARTY
from pydantic import Field

# FIRSTPARTY
from app.schemas.base import BaseSchema


class ErrorResponse(BaseSchema):
    """Pydantic модель для ответа во время ошибки."""
    code: int
    type_: str = Field(alias='type')
    message: str
