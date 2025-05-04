import typing
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Schedule
from .schemas import ScheduleCreate,ScheduleUpdate,ScheduleRead
from datetime import datetime, timedelta
import re
from datetime import datetime, timedelta

from datetime import datetime, timedelta

def validate_time_format(time_str: str) -> bool:
    """Проверка, что время в правильном формате (HH:MM)"""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def generate_schedule(start_schedule: str, frequency: int, interval: float, start_datetime: datetime, end_datetime: datetime):
    if not validate_time_format(start_schedule):
        raise HTTPException(status_code=400, detail="Invalid time format for 'start_schedule'. Please enter time in 'HH:MM' format.")

    if frequency <= 0:
        raise HTTPException(status_code=400, detail="'frequency' must be greater than 0.")

    if interval <= 0:
        raise HTTPException(status_code=400, detail="'interval' must be greater than 0.")

    schedule = []
    start_time = datetime.strptime(start_schedule, "%H:%M")
    current_time = start_time

    current_day = start_datetime.date()
    end_day = end_datetime.date()

    while current_day <= end_day:
        day_schedule = []
        for _ in range(frequency):
            end_time = current_time + timedelta(minutes=15)
            day_schedule.append({
                "start": current_time.replace(year=current_day.year, month=current_day.month, day=current_day.day).strftime("%Y-%m-%dT%H:%M:%S"),
                "end": end_time.replace(year=current_day.year, month=current_day.month, day=current_day.day).strftime("%Y-%m-%dT%H:%M:%S"),
                "done": False
            })
            current_time = end_time + timedelta(hours=interval)

        schedule.append({
            "date": current_day.strftime("%Y-%m-%d"),
            "appointments": day_schedule
        })

        current_day += timedelta(days=1)
        current_time = start_time

    return schedule


def create_schedule(db: Session, schedule: ScheduleCreate) -> ScheduleRead:
    """Создание нового расписания для лекарства."""
    # Проверка на уникальность имени лекарства
    existing_schedule = db.query(Schedule).filter(Schedule.name_drug == schedule.name_drug).first()
    if existing_schedule:
        raise HTTPException(status_code=400, detail=f"Schedule for drug '{schedule.name_drug}' already exists.")

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
        schedule_times=schedule_times
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

