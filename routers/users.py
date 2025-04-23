from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models import User
from schemas import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
