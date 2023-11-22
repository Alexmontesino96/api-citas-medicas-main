from enum import Enum
from fastapi import HTTPException
from models.user_patient import UserPatient
from models.users_doctor import UserDoctor
from database.database import Session

class UserRole(Enum):
    PACIENTE = 'paciente'
    DOCTOR = 'doctor'

async def search_user_with_role(role: UserRole, username: str):
    with Session() as db:
        model = UserPatient if role == UserRole.PACIENTE else UserDoctor
        user = db.query(model).filter(model.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="No user found with the provided username.")
        return user
