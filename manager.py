from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users_db_sqlmodel import SQLModelUserDatabase
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from models import User
from database import engine, get_session
from sqlmodel import Session
from typing import AsyncGenerator
from fastapi_users import BaseUserManager
import uuid
import os

SECRET = os.getenv("SECRET", "1")

class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        print(f"Пользователь {user.id} зарегистрирован.")

async def get_user_db() -> AsyncGenerator:
    with Session(engine) as session:
        yield SQLModelUserDatabase(session=session,user_model=User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
