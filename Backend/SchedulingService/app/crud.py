import typing
import uuid
from sqlalchemy.orm import Session
from .models import Schedule
from .schemas import ScheduleCreate,ScheduleUpdate,ScheduleRead
from datetime import datetime, timedelta

from datetime import datetime, timedelta

from datetime import datetime, timedelta

def generate_schedule(start_schedule: str, frequency: int, interval: float, start_datetime: datetime, end_datetime: datetime):
    schedule = []
    start_time = datetime.strptime(start_schedule, "%H:%M")
    current_time = start_time

    # Период с начала до конца
    current_day = start_datetime.date()
    end_day = end_datetime.date()

    while current_day <= end_day:
        day_schedule = []
        for _ in range(frequency):
            # Рассчитываем время конца приёма
            end_time = current_time + timedelta(minutes=15)
            
            # Форматируем дату и время в ISO-формате с корректной датой для каждого интервала
            day_schedule.append({
                "start": current_time.replace(year=current_day.year, month=current_day.month, day=current_day.day).strftime("%Y-%m-%dT%H:%M:%S"),
                "end": end_time.replace(year=current_day.year, month=current_day.month, day=current_day.day).strftime("%Y-%m-%dT%H:%M:%S")
            })
            
            # Переход к следующему интервалу
            current_time = end_time + timedelta(hours=interval)

        schedule.append({
            "date": current_day.strftime("%Y-%m-%d"),
            "appointments": day_schedule
        })

        # Переход на следующий день
        current_day += timedelta(days=1)
        current_time = start_time

    return schedule



def create_schedule(db: Session, schedule: ScheduleCreate) -> ScheduleRead:
    """
    Создание нового расписания для лекарства.
    """
    # Генерация расписания
    schedule_times = generate_schedule(
        start_schedule=schedule.start_schedule,
        frequency=schedule.frequency,
        interval=schedule.interval,
        start_datetime=schedule.start_datetime,
        end_datetime=schedule.end_datetime
    )

    # Создание нового объекта расписания
    db_schedule = Schedule(
        id=uuid.uuid4(),
        user_id=schedule.user_id,
        name_drug=schedule.name_drug,
        dosage=schedule.dosage,
        frequency=schedule.frequency,
        interval=schedule.interval,
        description=schedule.description,
        start_datetime=schedule.start_datetime,
        end_datetime=schedule.end_datetime,
        start_schedule=schedule.start_schedule,
        is_active=schedule.is_active,
        schedule_times=schedule_times  # Добавляем сгенерированное расписание
    )
    
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule



def get_all_schedules(db: Session, skip: int = 0, limit: int = 100) -> typing.List[ScheduleRead]:
    """
    Получить все расписания с пагинацией
    """
    return db.query(Schedule).offset(skip).limit(limit).all()


def get_schedule(schedule_id: uuid.UUID, db: Session) -> typing.Optional[ScheduleRead]:
    """
    Получить конкретное расписание по ID
    """
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()

def get_schedules_by_user_id(user_id: uuid.UUID, db: Session) -> typing.List[ScheduleRead]:
    """
    Получить все расписания по ID пользователя
    """
    return db.query(Schedule).filter(Schedule.user_id == user_id).all()


def update_schedule(schedule_id: uuid.UUID, schedule: ScheduleUpdate, db: Session) -> typing.Optional[ScheduleRead]:
    """
    Обновление информации о расписании
    """
    updated = db.query(Schedule).filter(Schedule.id == schedule_id).update(schedule.dict(exclude_unset=True))
    db.commit()
    if updated:
        return get_schedule(schedule_id, db)
    return None


def delete_schedule(schedule_id: uuid.UUID, db: Session) -> bool:
    """
    Удаление расписания по ID
    """
    deleted = db.query(Schedule).filter(Schedule.id == schedule_id).delete()
    db.commit()
    return deleted > 0

