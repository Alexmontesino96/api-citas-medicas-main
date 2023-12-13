from pydantic import BaseModel, Field, FutureDatetime
from datetime import datetime
from schemas.medical_speciality import MedicalSpeciality
from typing import Optional
from pydantic.types import constr


class Appointment(BaseModel):
    date_appointment: FutureDatetime = Field(examples=["The format date is YYYY-MM-DD HH:MM:SS"])
    speciality: MedicalSpeciality
    patient_id: constr(min_length=1)
    doctor_id: constr(min_length=1)
    address: constr(min_length=1)
    notes: Optional[str]
    
    def model_dump(self):
        return {
            "date_appointment": self.date_appointment,
            "speciality": self.speciality.value,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "address": self.address,
            "notes": self.notes
        }

