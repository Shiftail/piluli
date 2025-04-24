from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime
import uuid

class ScheduleBase(BaseModel):
    user_id: UUID4  # Идентификатор пользователя
    name_drug: str  # Название лекарства
    dosage: float  # Дозировка в мг
    frequency: int  # Частота приёма в сутки
    interval: float  # Интервал между приёмами (в часах)
    description: Optional[str] = ""  # Описание (необязательное)
    start_datetime: datetime  # Дата начала приёма
    end_datetime: datetime  # Дата окончания приёма
    start_schedule: str  # Начало расписания (например, "08:30")
    is_active: bool = True  # Активность расписания
    schedule_times: Optional[List[dict]] = None  # JSON для хранения расписания, например, список времен начала и конца приёма

    class Config:
        from_attributes = True


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(ScheduleBase):
    pass


class ScheduleRead(ScheduleBase):
    id: UUID4 
    class Config:
        from_attributes = True
