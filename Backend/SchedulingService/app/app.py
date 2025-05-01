from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from .schemas import ScheduleCreate,ScheduleUpdate,ScheduleRead
from . import crud
from . import config
import typing
import uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger

cfg: config.Config = config.load_config()

# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))

# init app
app = FastAPI(
    version='0.0.1',
    title='Schedules Management Service'
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/schedules", status_code=201, response_model=ScheduleRead, summary='Добавляет расписание для лекарства')
async def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)) -> ScheduleRead:
    return crud.create_schedule(db=db, schedule=schedule)

@app.get("/schedules", summary='Возвращает список расписаний', response_model=list[ScheduleRead])
async def get_all_schedules(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> typing.List[ScheduleRead]:
    return crud.get_all_schedules(db, skip, limit)

@app.get("/schedules/{schedule_id}", summary='Возвращает информацию о расписании', response_model=ScheduleRead)
async def get_schedule_info(schedule_id: uuid.UUID, db: Session = Depends(get_db)) -> ScheduleRead:
    schedule = crud.get_schedule(schedule_id, db)
    if schedule:
        return schedule
    return JSONResponse(status_code=404, content={"message": "Schedule not found"})

@app.get("/schedules/user/{user_id}", summary="Получить все расписания пользователя", response_model=list[ScheduleRead])
async def get_user_schedules(user_id: uuid.UUID, db: Session = Depends(get_db)) -> typing.List[ScheduleRead]:
    schedules = crud.get_schedules_by_user_id(user_id, db)
    if schedules:
        return schedules
    return JSONResponse(status_code=404, content={"message": "Schedules not found for this user"})

@app.patch("/schedules/{schedule_id}", summary='Обновляет информацию о расписании', response_model=ScheduleRead)
async def update_schedule(schedule_id: uuid.UUID, schedule: ScheduleUpdate, db: Session = Depends(get_db)) -> ScheduleRead:
    updated = crud.update_schedule(schedule_id, schedule, db)
    if updated:
        return updated
    return JSONResponse(status_code=404, content={"message": "Schedule not found"})

@app.delete("/schedules/{schedule_id}", summary='Удаляет расписание')
async def delete_schedule(schedule_id: uuid.UUID, db: Session = Depends(get_db)):
    if crud.delete_schedule(schedule_id, db):
        return JSONResponse(status_code=200, content={"message": "Schedule successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Schedule not found"})

