from database.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship


class Appointment_Model(Base):
    __tablename__ = "appointments"

    id = Column(Integer, autoincrement=True, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date_appointment = Column(DateTime, nullable=False)
    speciality = Column(String(50), nullable=False)
    address = Column(String(255), nullable=False)
    notes = Column(String(255), nullable=False)
    status_appointment = Column(Boolean, default=False, nullable=True)
    doctor = relationship('Doctor_Model', back_populates='appointments')
    patient = relationship('Pacient_Model', back_populates='appointments')

    def show_appointment(self):
        dict_appointment = {
            "id": self.id,
            "doctor_name": f"- Id:{self.doctor.id}-{self.doctor.first_name} {self.doctor.last_name} " if self.doctor else None,
            "patient_name": f"- Id:{self.patient.id}-{self.patient.first_name} {self.patient.last_name} " if self.patient else None,
            "date_appointment": self.date_appointment.strftime('%m/%d/%Y') if self.date_appointment else None,
            "speciality": self.speciality,
            "address": self.address,
            "notes": self.notes,
            "status_appointment": self.status_appointment
        }
        return dict_appointment
