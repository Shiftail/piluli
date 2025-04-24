from sqlalchemy import Column, String, Integer,Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database import Base
class Drug(Base):
    __tablename__ = "drugs"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    dosage = Column(Float) #mg example 200mg 
    frequency = Column(Integer, default=0)
    interval = Column(Float, default=1)
    description = Column(String, default='')
