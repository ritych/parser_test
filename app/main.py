"""Точка входа приложения."""
# THIRDPARTY
from fastapi import FastAPI
import uvicorn

# FIRSTPARTY
from app.routers.router import router as general_router


app = FastAPI(
    title='Sales Analysis Service',
    summary='XML Parser & AI Analyzer Service',
    version='0.1.0',
)

router_list = [
    general_router,
]

for router in router_list:
    app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )

