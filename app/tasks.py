# THIRDPARTY
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import xml.etree.ElementTree as ET
from celery import Celery
import openai

# FIRSTPARTY
from app.schemas.schemas import SalesdataAllSchema
from app.services.services import SalesdataService

celery = Celery('tasks', broker='redis://redis:6379')


async def parse_sales_data(url: str):
    uri = 'https://zandrlab.ru/1.xml'
    response = requests.get(uri)
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

    else:
        raise Exception("Failed to fetch XML data")

    return products


async def insert_data_to_db(products, session: AsyncSession):
    if products:
        service = SalesdataService(session=session)
        for result in products:
            await service.create_sales_data(
                SalesdataAllSchema(**result)
            )
    else:
        raise Exception("No products found")


@celery.task
def get_report():
    my_file = open("log.txt", "a+")
    my_file.write("Report done!")
    my_file.close()
    return 'This is report'


def generate_report(date, total_revenue, products, categories):
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

    return response['choices'][0]['message']['content']
