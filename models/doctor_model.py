from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from database.database import Base
from schemas.doctor import Doctor
from sqlalchemy import Column, Integer, DateTime, String, Enum
from sqlalchemy.orm import relationship

class Doctor_Model(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(50), unique=True, nullable=False)
    address = Column(String(255), nullable=False)
    birthdate = Column(DateTime, nullable=False)
    speciality = Column(String(50), nullable=False)
    npi = Column(String(255), unique=True, nullable=False)
    role = Column(Enum("doctor", name="doctor_role"), nullable=False, default="doctor")
    appointments = relationship("Appointment_Model", back_populates="doctor")
    users_doctor = relationship("UserDoctor", back_populates="doctor")

    def update_with(self, new_doctor: Doctor):

        self.first_name = new_doctor.first_name
        self.middle_name = new_doctor.middle_name
        self.last_name = new_doctor.last_name
        self.email = new_doctor.email
        self.phone_number = new_doctor.phone_number
        self.address = new_doctor.address
        self.birthdate = new_doctor.birthdate
        self.speciality = new_doctor.speciality.name if new_doctor.speciality else None
        if self.npi != new_doctor.npi:
            self.npi = new_doctor.npi

