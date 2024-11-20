# THIRDPARTY
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import xml.etree.ElementTree as ET
import openai

# FIRSTPARTY
from app.schemas.schemas import SalesdataAllSchema, ReportCreateSchema
from app.services.services import SalesdataService, ReportService
from app.main import logger


async def parse_sales_data() -> list:
    load_dotenv()
    url = os.getenv('XML_FILE_URL')
    response = requests.get(url)
    if response.status_code == 200:
        xml_data = response.content
        products = []
        # Парсинг XML
        root = ET.fromstring(xml_data)
        date = root.attrib['date']

        for product in root.findall('.//product'):
            name = product.find('name').text
            quantity = int(product.find('quantity').text)
            price = float(product.find('price').text)
            category = product.find('category').text
            products.append({
                "name": name,
                "quantity": quantity,
                "price": price,
                "category": category,
                "date": date,
            })
            logger.info(f"Product {name} has been parsed")

        logger.info(f"Parsed {len(products)} products")

    else:
        raise Exception("Failed to fetch XML data")

    return products


async def insert_data_to_db(products, session: AsyncSession) -> None:
    if products:
        service = SalesdataService(session=session)
        for result in products:
            await service.create_sales_data(
                SalesdataAllSchema(**result)
            )
    else:
        raise Exception("No products found")


async def generate_report(date, total_revenue, products, categories, session: AsyncSession):
    top_products = sorted(products, key=lambda x: x['quantity'], reverse=True)[:3]
    prompt = f"""
    Проанализируй данные о продажах за {date}:
    1. Общая выручка: {total_revenue}
    2. Топ-3 товара по продажам: {top_products}
    3. Распределение по категориям: {categories}

    Составь краткий аналитический отчет с выводами и рекомендациями.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # сохранеям report в БД
    service = ReportService(session=session)
    await service.create_report(
        ReportCreateSchema(
            date=date,
            report=response['choices'][0]['message']['content'],
        )
    )

    return True
