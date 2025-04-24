import psycopg2
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

def get_due_notifications():
    logger.info("Получение уведомлений для текущего времени.")

    conn = psycopg2.connect(
        dbname="schedulingdb",
        user="schedulingdb",
        password="schedulingdb",
        host="Schedulingdb",
        port="5432"
    )
    cursor = conn.cursor()
    
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%dT%H:%M:%S")  # Приводим к формату ISO без миллисекунд
    logger.info(f"Текущее время: {now_str}. Проверка временных интервалов.")

    cursor.execute("""
        SELECT user_id, name_drug, schedule_times
        FROM schedules
        WHERE is_active = TRUE
    """)
    
    result = []
    
    for user_id, name_drug, schedule_times in cursor.fetchall():
        for day in schedule_times:  # schedule_times уже list, т.е. Python-список
            for appointment in day.get("appointments", []):
                start = appointment.get("start")
                end = appointment.get("end")

                if start <= now_str <= end:
                    logger.info(f"Подходящее время для {user_id} / {name_drug}: {start} - {end}")
                    result.append({"user_id": user_id, "name_drug": name_drug})
                    break
    
    cursor.close()
    conn.close()

    logger.info(f"Найдено {len(result)} уведомлений.")
    return result
