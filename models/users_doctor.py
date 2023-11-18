
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

# Crear modelo de usuario y contraseña para doctor
class UserDoctor(Base):
    __tablename__ = 'users_doctor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    hashed_password = Column(String)
    id_doctor = Column(Integer, ForeignKey('doctors.id'))
    doctor = relationship("Doctor_Model", back_populates="users_doctor")
