from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from .schemas import DrugCreate, DrugRead, DrugUpdate
from . import crud
from . import config
import typing
import uuid
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
cfg: config.Config = config.load_config()

# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))

# init app
app = FastAPI(
    version='0.0.1',
    title='Drugs Management Service'
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/drugs", status_code=201, response_model=DrugRead, summary='Добавляет лекарство')
async def create_drug(drug: DrugCreate, db: Session = Depends(get_db)) -> DrugRead:
    return crud.create_drug(db=db, drug=drug)

@app.get("/drugs", summary='Возвращает список лекарств', response_model=list[DrugRead])
async def get_all_drugs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> typing.List[DrugRead]:
    return crud.get_all_drugs(db, skip, limit)

@app.get("/drugs/{drug_id}", summary='Возвращает информацию о лекарстве', response_model=DrugRead)
async def get_drug_info(drug_id: uuid.UUID, db: Session = Depends(get_db)) -> DrugRead:
    drug = crud.get_drug(drug_id, db)
    if drug:
        return drug
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.patch("/drugs/{drug_id}", summary='Обновляет информацию о лекарстве', response_model=DrugRead)
async def update_drug(drug_id: uuid.UUID, drug: DrugUpdate, db: Session = Depends(get_db)) -> DrugRead:
    updated = crud.update_drug(drug_id, drug, db)
    if updated:
        return updated
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete("/drugs/{drug_id}", summary='Удаляет лекарство')
async def delete_drug(drug_id: uuid.UUID, db: Session = Depends(get_db)):
    if crud.delete_drug(drug_id, db):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})
