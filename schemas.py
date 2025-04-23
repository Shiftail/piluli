from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum
from fastapi_users import schemas

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


# 📦 Пользователи

class UserCreate(schemas.BaseUserCreate):
    email: str
    username: Optional[str] = None
    weight_kg: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    medical_conditions: Optional[str] = None
    class Config:
        from_attributes = True


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: Optional[str]
    weight_kg: Optional[float]
    age: Optional[int]
    gender: Optional[Gender]
    medical_conditions: Optional[str]


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    weight_kg: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    medical_conditions: Optional[str] = None


# 📦 Лекарства

class MedicineCreate(BaseModel):
    name: str
    dosage: str
    unit: str
    dose_per_intake: float
    intake_interval_hours: int
    start_date: datetime
    end_date: Optional[datetime] = None
    user_id: int


class MedicineRead(BaseModel):
    id: int
    name: str
    dosage: str
    unit: str
    dose_per_intake: float
    intake_interval_hours: int
    start_date: datetime
    end_date: Optional[datetime]
    user_id: int

    class Config:
        from_attributes = True


# 📦 Приёмы

class IntakeCreate(BaseModel):
    medicine_id: int
    scheduled_time: datetime


class IntakeRead(BaseModel):
    id: int
    medicine_id: int
    scheduled_time: datetime
    taken: bool
    taken_time: Optional[datetime] = None

    class Config:
        from_attributes = True
