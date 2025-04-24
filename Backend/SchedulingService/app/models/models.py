from sqlalchemy import Column, String, Integer,Float,DateTime, Boolean,JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name_drug = Column(String, unique=True, index=True, nullable=False)
    dosage = Column(Float) #mg example 200mg 
    frequency = Column(Integer, default=0) #Частота приема в сутки
    interval = Column(Float, default=1) #например каждый час 
    description = Column(String, default='')
    start_datetime = Column(DateTime, nullable=False)  # дата начала приёма
    end_datetime = Column(DateTime, nullable=False)     # дата окончания приёма 
    start_schedule = Column(String, nullable=False)        # начало расписания например "08:30"
    is_active = Column(Boolean, default=True)
    schedule_times = Column(JSON, nullable=True)  # JSON поле для хранения расписания