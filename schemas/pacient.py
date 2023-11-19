from datetime import datetime
from schemas.person import Person
from pydantic import field_validator
from typing import Optional, List
from schemas.user import User


class Pacient(Person, User):

    def get_patient_data(self):
        return {
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "role": "patient"
        }

    def __init__(self, **data):
        super().__init__(**data)
        if not self.is_patient():
            raise ValueError("Role must be 'patient' for this class")
        