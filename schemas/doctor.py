from schemas.person import Person
from schemas.user import User
from schemas.medical_speciality import MedicalSpeciality
from pydantic import Field, field_validator
from enum import Enum


class Doctor(Person, User):
    speciality: MedicalSpeciality
    npi: str = Field(default="3289643276486",min_length=8, max_length=18)


    def get_doctor_data(self):
        return {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "birthdate": self.birthdate,
            "speciality": self.speciality.value if isinstance(self.speciality, Enum) else self.speciality,
            "npi": self.npi,
            "role": "doctor"
        }

    def __init__(self, **data):
        super().__init__(**data)
        if not self.is_doctor():
            raise ValueError("Role must be 'doctor' for this class")
        self.speciality = MedicalSpeciality(data['speciality'])
        self.npi = data['npi']
    

