from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
from datetime import datetime
from schemas.medical_speciality import MedicalSpeciality
from validation import validation


class Appointment(BaseModel):
    date_appointment: Optional[str]
    speciality: Optional[str]
    patient_id: str
    doctor_id: str
    address: str
    notes: Optional[str]

    @field_validator("date_appointment")
    def validate_appointment(cls, value):
        return validation.validation_date(value)

    @field_validator("speciality")
    def validate_speciality(cls, value):
        if value not in [e.value for e in MedicalSpeciality]:
            raise ValueError(
                f"Speciality not found. Valid specialties are: {', '.join([e.value for e in MedicalSpeciality])}")
        return value

