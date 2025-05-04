from celery_app import celery_app
from db.scheduling import get_due_notifications, mark_appointment_done
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
            try:
                asyncio.run(send_telegram_message(user["tg_id"], text))
                # Если не упало — помечаем как done
                mark_appointment_done(
                    user_id=item["user_id"],
                    name_drug=item["name_drug"],
                    start_time=item["start"]
                )
            except Exception as e:
                logger.error(f"Ошибка при отправке уведомления: {e}")
