from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import Intake
from schemas import IntakeCreate
from datetime import datetime

router = APIRouter(prefix="/intakes", tags=["Intakes"])

@router.post("/")
def schedule_intake(intake: IntakeCreate, session: Session = Depends(get_session)):
    new_intake = Intake(**intake.dict())
    session.add(new_intake)
    session.commit()
    session.refresh(new_intake)
    return new_intake

@router.post("/{intake_id}/take")
def mark_taken(intake_id: int, session: Session = Depends(get_session)):
    intake = session.get(Intake, intake_id)
    if not intake:
        return {"error": "Intake not found"}
    intake.taken = True
    intake.taken_time = datetime.utcnow()
    session.add(intake)
    session.commit()
    return intake
