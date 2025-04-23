from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from models import Medicine
from schemas import MedicineCreate

router = APIRouter(prefix="/medicines", tags=["Medicines"])

@router.post("/")
def create_medicine(medicine: MedicineCreate, session: Session = Depends(get_session)):
    new_med = Medicine(**medicine.dict())
    session.add(new_med)
    session.commit()
    session.refresh(new_med)
    return new_med

@router.get("/user/{user_id}")
def get_user_medicines(user_id: int, session: Session = Depends(get_session)):
    medicines = session.exec(select(Medicine).where(Medicine.user_id == user_id)).all()
    return medicines
