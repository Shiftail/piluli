from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from fastapi_users import BaseUserManager
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class User(SQLModelBaseUserDB, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = None
    email: str
    hashed_password:str
    weight_kg: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    medical_conditions: Optional[str] = None  # например: "diabetes, hypertension"
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    medicines: List["Medicine"] = Relationship(back_populates="user")

    class Config:
        from_attributes = True


class Medicine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    dosage: str  # например: "500mg"
    unit: str  # например: "mg", "ml", "tablet"
    dose_per_intake: float  # например: 500
    intake_interval_hours: int  # например: каждые 8 часов
    start_date: datetime
    end_date: Optional[datetime] = None

    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="medicines")
    intakes: List["Intake"] = Relationship(back_populates="medicine")


class Intake(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    medicine_id: int = Field(foreign_key="medicine.id")
    scheduled_time: datetime
    taken: bool = False
    taken_time: Optional[datetime] = None

    medicine: Optional[Medicine] = Relationship(back_populates="intakes")
