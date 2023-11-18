from database.database import Base
from sqlalchemy import Column, String, Integer, CHAR, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from schemas.pacient import Pacient


class Pacient_Model(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(10), unique=True, nullable=False)
    address = Column(String(255), nullable=False)
    birthdate = Column(DateTime, nullable=False)
    gender = Column(CHAR(1), CheckConstraint("gender IN('M','F','X','O')"), nullable= False)
    appointments = relationship("Appointment_Model", back_populates="patient")

    user_patient = relationship("UserPatient", back_populates="pacient")

    def update_with(self, patient: Pacient):

        self.first_name = patient.first_name
        if patient.middle_name is not None:
            self.middle_name = patient.middle_name
        self.last_name = patient.last_name
        self.email = patient.email
        self.phone_number = patient.phone_number
        self.address = patient.address
        self.birthdate = patient.birthdate
        self.gender = patient.gender
 

