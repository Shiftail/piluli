import uuid
from pydantic import Field, EmailStr, field_validator
from fastapi_users import schemas
from typing import Optional, Annotated


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    email: EmailStr
    gender: bool
    age: Annotated[int, Field(gt=0, description="Возраст должен быть больше 0")]
    tg_id: int
    time_zone: Annotated[int, Field(ge=-12, le=14, description="Часовой пояс от -12 до 14")]
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    gender: bool
    age: Annotated[int, Field(gt=0, description="Возраст должен быть больше 0")]
    tg_id: int
    time_zone: Annotated[int, Field(ge=-12, le=14, description="Часовой пояс от -12 до 14")]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        if not any(char in "!@#$%^&*()_+-=[]{}|;':\",.<>/?`~" for char in v):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")
        return v


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    gender: Optional[bool] = None
    age: Optional[int] = Field(default=None, gt=0)
    tg_id: Optional[int] = None
    time_zone: Optional[int] = Field(default=None, ge=-12, le=14)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        if not any(char in "!@#$%^&*()_+-=[]{}|;':\",.<>/?`~" for char in v):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")
        return v
