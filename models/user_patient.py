
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base

class UserPatient(Base):
    __tablename__ = 'user_patient'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    pacient_id = Column(Integer, ForeignKey('patients.id'))
    
    pacient = relationship("Pacient_Model", back_populates="user_patient")
