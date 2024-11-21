# THIRDPARTY
import os
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import xml.etree.ElementTree as ET

# FIRSTPARTY
from app.schemas.schemas import SalesdataAllSchema, ReportCreateSchema, ReportDataSchema
from app.services.services import SalesdataService, ReportService
from app.loggers.logger import logger


async def parse_sales_data() -> ReportDataSchema:
    """Парсинг XML файла"""
    load_dotenv()
    url = os.getenv('XML_FILE_URL')
    response = requests.get(url)
    if response.status_code == 200:
        xml_data = response.content
        products = []
        total_revenue = 0
        categories = {}
        # Парсинг XML
        root = ET.fromstring(xml_data)
        date = root.attrib['date']

        for product in root.findall('.//product'):
            name = product.find('name').text
            quantity = int(product.find('quantity').text)
            price = float(product.find('price').text)
            category = product.find('category').text
            if category in categories:
                categories[category] += quantity
            else:
                categories[category] = quantity
            products.append({
                "name": name,
                "quantity": quantity,
                "price": price,
                "category": category,
                "date": date,
            })
            revenue = quantity * price
            total_revenue += revenue

            logger.info(f"Product {name} has been parsed")

        logger.info(f"Parsed {len(products)} products")

    else:
        logger.info(f"Failed to fetch XML data")
        raise Exception("Failed to fetch XML data")

    return ReportDataSchema(
        products=products,
        date=date,
        total_revenue=total_revenue,
        categories=categories,
    )


async def insert_data_to_db(products, session: AsyncSession) -> None:
    """Добавление в БД данных о продаже"""
    if products:
        service = SalesdataService(session=session)
        for product in products:
            await service.create_sales_data(
                SalesdataAllSchema(
                    name=product.name,
                    quantity=product.quantity,
                    price=product.price,
                    category=product.category,
                    date=product.date,
                )
            )
    else:
        raise Exception("No products found")


async def generate_report(date, total_revenue, products, categories, session: AsyncSession):
    """Получение отчета от LLM и сохранение его в БД"""
    top_products = products[:3]
    prompt = f"""
    Проанализируй данные о продажах за {date}:
    1. Общая выручка: {total_revenue}
    2. Топ-3 товара по продажам: {top_products}
    3. Распределение по категориям: {categories}

    Составь краткий аналитический отчет с выводами и рекомендациями.
    """

    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        report = response['choices'][0]['message']['content']
    except Exception as e:
        report = str(e)

    # сохранеям report в БД
    service = ReportService(session=session)
    await service.create_report(
        ReportCreateSchema(
            date=date,
            report=report,
        )
    )
