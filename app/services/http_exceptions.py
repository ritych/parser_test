# THIRDPARTY
from fastapi import HTTPException

# FIRSTPARTY
from app.schemas.error_response import ErrorResponse


exception_400_validation = HTTPException(
    status_code=400,
    detail=ErrorResponse(
        code=400,
        type_='ValidationError',
        message='Неверный формат данных'
    ).model_dump()
)

exception_500_db_connection = HTTPException(
    status_code=500,
    detail=ErrorResponse(
        code=500,
        type_='ConnectionRefusedError',
        message='Нет подключения к БД'
    ).model_dump()
)
