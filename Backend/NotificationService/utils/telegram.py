import aiohttp
import logging

# Настроим логирование
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (можно изменить на DEBUG для более подробных логов)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Получаем логгер
logger = logging.getLogger(__name__)

BOT_TOKEN = "8173705098:AAHZHXWIIw9k_CaO6SR57KDVUz6KARsPWuM"

async def send_telegram_message(chat_id, text):
    logger.info(f"Попытка отправки сообщения пользователю с chat_id {chat_id}: {text}")  # Логируем попытку отправки

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"chat_id": chat_id, "text": text}) as resp:
                response_text = await resp.text()
                if resp.status == 200:
                    logger.info(f"Сообщение успешно отправлено пользователю с chat_id {chat_id}")  # Логируем успешную отправку
                else:
                    logger.error(f"Ошибка при отправке сообщения пользователю {chat_id}. Статус: {resp.status}, Ответ: {response_text}")  # Логируем ошибку
                return response_text
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения пользователю {chat_id}: {e}")  # Логируем исключение в случае ошибки
        return str(e)
