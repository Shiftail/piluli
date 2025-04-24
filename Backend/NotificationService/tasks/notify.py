from celery_app import celery_app
from db.scheduling import get_due_notifications
from db.users import get_user_by_id
from utils.telegram import send_telegram_message
import asyncio
import logging
logger = logging.getLogger(__name__)

@celery_app.task
def check_and_notify():
    logger.info("🔔 Запуск задачи check_and_notify")
    due_items = get_due_notifications()
    for item in due_items:
        user = get_user_by_id(item["user_id"])
        if user:
            text = f"{user['username']}, Вы должны принять препарат {item['name_drug']}"
            logger.info(f"📨 Отправка уведомления: {text}")
            asyncio.run(send_telegram_message(user["tg_id"], text))
