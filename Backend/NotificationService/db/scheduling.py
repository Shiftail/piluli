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
    now_str = now.strftime("%Y-%m-%dT%H:%M:%S")  # ISO без миллисекунд
    logger.info(f"Текущее время: {now_str}. Проверка временных интервалов.")

    cursor.execute("""
        SELECT user_id, name_drug, schedule_times
        FROM schedules
        WHERE is_active = TRUE
    """)
    
    result = []

    for user_id, name_drug, schedule_times in cursor.fetchall():
        if isinstance(schedule_times, str):
            schedule_times = json.loads(schedule_times)  # на случай, если строка
        for day in schedule_times:
            for appointment in day.get("appointments", []):
                start = appointment.get("start")
                end = appointment.get("end")
                done = appointment.get("done", False)

                if not done and start <= now_str <= end:
                    logger.info(f"Подходящее и не выполненное уведомление: {user_id} / {name_drug} в {start} - {end}")
                    result.append({
                        "user_id": user_id,
                        "name_drug": name_drug,
                        "start": start,
                        "end": end
                    })
                    break  # Можно прервать проверку текущего дня, если нашли хотя бы одно актуальное

    cursor.close()
    conn.close()

    logger.info(f"Найдено {len(result)} уведомлений.")
    return result
def mark_appointment_done(user_id, name_drug, start_time):
    conn = psycopg2.connect(
        dbname="schedulingdb",
        user="schedulingdb",
        password="schedulingdb",
        host="Schedulingdb",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, schedule_times
        FROM schedules
        WHERE user_id = %s AND name_drug = %s AND is_active = TRUE
    """, (user_id, name_drug))

    row = cursor.fetchone()
    if not row:
        logger.warning("⛔ Расписание не найдено.")
        cursor.close()
        conn.close()
        return

    schedule_id, schedule_times = row

    # Вдруг строка — парсим
    if isinstance(schedule_times, str):
        schedule_times = json.loads(schedule_times)

    modified = False
    for day in schedule_times:
        for appointment in day.get("appointments", []):
            if appointment.get("start") == start_time:
                appointment["done"] = True
                modified = True
                break
        if modified:
            break

    if modified:
        cursor.execute("""
            UPDATE schedules
            SET schedule_times = %s
            WHERE id = %s
        """, (json.dumps(schedule_times), schedule_id))
        conn.commit()
        logger.info(f"✅ Помечено как выполнено: {user_id} / {name_drug} / {start_time}")
    else:
        logger.warning(f"⚠ Не найдено совпадение по времени {start_time}.")

    cursor.close()
    conn.close()