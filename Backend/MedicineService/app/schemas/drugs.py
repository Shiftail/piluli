from pydantic import BaseModel, UUID4
from typing import Optional
import uuid

class DrugBase(BaseModel):
    name: str
    dosage: float #mg
    frequency: int
    interval: float
    description: Optional[str] = ""

    class Config:
        from_attributes = True

class DrugCreate(DrugBase):
    pass

class DrugUpdate(DrugBase):
    pass

class DrugRead(DrugBase):
    id: UUID4
