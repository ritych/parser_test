# THIRDPARTY
from datetime import timedelta
from celery import Celery
import asyncio

# FIRSTPARTY
from app.database.config import settings
from app.tasks.support import parse_sales_data, insert_data_to_db
from app.loggers.logger import logger

celery = Celery('tasks', broker='redis://redis:6379')
celery.conf.update(
    timezone='UTC',
    enable_utc=True,
    worker_hijack_root_logger=False,
    broker_connection_retry_on_startup=True,
)

celery.autodiscover_tasks()


async def async_task():
    """Таска для получения XML-файла, занесение данных в БД, составление промта и получение
    репорта от LLM
    """
    parsed_data = await parse_sales_data()
    session = settings.get_session()
    await insert_data_to_db(parsed_data, session)


@celery.task
def get_report():
    logger.info("Running task!")
    asyncio.run(async_task())
    logger.info("Finish task!")


celery.conf.beat_schedule = {
    'run-every-day': {
        'task': 'app.tasks.task.get_report',
        # 'schedule': crontab(hour=0, minute=0),  # Выполнять каждый день в полночь
        "schedule": timedelta(seconds=10),
    },
}
