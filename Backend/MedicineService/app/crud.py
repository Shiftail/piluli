import typing
import uuid
from sqlalchemy.orm import Session
from .models import Drug
from .schemas import DrugCreate, DrugRead, DrugUpdate
from datetime import datetime
from fastapi import HTTPException

def create_drug(db: Session, drug: DrugCreate) -> DrugRead:
    """
    Создание нового лекарства.
    """
    # Проверка: существует ли уже лекарство с таким именем
    existing = db.query(Drug).filter(Drug.name == drug.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Лекарство с таким именем уже существует")

    # Создание нового объекта
    db_drug = Drug(
        id=uuid.uuid4(),
        name=drug.name,
        dosage=drug.dosage,
        frequency=drug.frequency,
        interval=drug.interval,
        description=drug.description,
    )
    
    db.add(db_drug)
    db.commit()
    db.refresh(db_drug)
    return db_drug


def get_all_drugs(db: Session, skip: int = 0, limit: int = 100) -> typing.List[DrugRead]:
    """
    Получить все лекарства с пагинацией
    """
    return db.query(Drug).offset(skip).limit(limit).all()


def get_drug(drug_id: uuid.UUID, db: Session) -> typing.Optional[DrugRead]:
    """
    Получить конкретное лекарство по ID
    """
    return db.query(Drug).filter(Drug.id == drug_id).first()


def update_drug(drug_id: uuid.UUID, drug: DrugUpdate, db: Session) -> typing.Optional[DrugRead]:
    """
    Обновление информации о лекарстве
    """
    updated = db.query(Drug).filter(Drug.id == drug_id).update(drug.dict(exclude_unset=True))
    db.commit()
    if updated:
        return get_drug(drug_id, db)
    return None


def delete_drug(drug_id: uuid.UUID, db: Session) -> bool:
    """
    Удаление лекарства по ID
    """
    deleted = db.query(Drug).filter(Drug.id == drug_id).delete()
    db.commit()
    return deleted > 0
