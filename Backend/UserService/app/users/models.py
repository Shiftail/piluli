from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID,SQLAlchemyUserDatabase
from sqlalchemy import Column, Boolean, String,Integer
from sqlalchemy.ext.asyncio import AsyncSession
from app.users import database

class User(SQLAlchemyBaseUserTableUUID, database.BASE):
    tg_id = Column(Integer)
    gender = Column(Boolean)
    age = Column(Integer)
    email =  Column(String, nullable=False)
    username = Column(String, nullable=False)
    time_zone = Column(Integer, default=0)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.initializer.async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)