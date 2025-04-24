import psycopg2
import logging

# Получаем логгер
logger = logging.getLogger(__name__)

def get_user_by_id(user_id):
    logger.info(f"Получение данных пользователя с id {user_id} из базы данных.")
    conn = psycopg2.connect(
        dbname="userdb",
        user="userdb",
        password="userdb",
        host="Userdb",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id, username FROM \"user\" WHERE id = %s", (str(user_id),))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        logger.info(f"Пользователь найден: {result[1]} (tg_id: {result[0]})")  # Логируем, если пользователь найден
        return {"tg_id": result[0], "username": result[1]}
    else:
        logger.warning(f"Пользователь с id {user_id} не найден в базе данных.")  # Логируем, если пользователь не найден
    return None
