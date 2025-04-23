import uvicorn
from fastapi import FastAPI,Depends
from database import init_db
from models import User
from fastapi_users import schemas as user_schemas
from fastapi_users.router import get_auth_router, get_register_router,get_users_router
from fastapi_users.authentication import BearerTransport

from routers import medicines, intake
from manager import fastapi_users, auth_backend
from schemas import UserCreate,UserRead,UserUpdate

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(medicines.router)
app.include_router(intake.router)

app.include_router(
    get_auth_router(backend=auth_backend,get_user_manager=fastapi_users.get_user_manager,authenticator=fastapi_users.authenticator),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    get_register_router(get_user_manager=fastapi_users.get_user_manager,user_schema=UserRead,user_create_schema=UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    get_users_router(get_user_manager=fastapi_users.get_user_manager,user_schema=UserRead,user_update_schema=UserUpdate,authenticator=fastapi_users.authenticator),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)