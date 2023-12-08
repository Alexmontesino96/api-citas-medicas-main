from enum import Enum
from fastapi import HTTPException
from models.user_patient import UserPatient
from models.users_doctor import UserDoctor
from database.database import Session

class UserRole(Enum):
    PACIENTE = 'patient'
    DOCTOR = 'doctor'

class Gender_User(Enum):
    MASCULINO = 'M'
    FEMENINO = 'F'
    NO_BINARIO = 'X'
    OTRO = 'O'

    
    

def search_user_with_role(role: str, username: str, db: Session) -> UserPatient or UserDoctor or None:
    """
    Search for a user with the specified role and username in the database.

    Args:
        role (UserRole): The role of the user (PACIENTE or DOCTOR).
        username (str): The username of the user.
        db (Session): The database session.

    Returns:
        UserPatient or UserDoctor or None: The user with the specified role and username, or None if not found.
    """
    model = UserPatient if role == UserRole.PACIENTE.value else UserDoctor
    user = db.query(model).filter(model.username == username).first()
    if not user:
        return None
    return user

def validate_existence_user_with_role(role: UserRole, username: str, db: Session) -> None:
    """
    Validates the existence of a user with a specific role and username in the database.

    Args:
        role (UserRole): The role of the user.
        username (str): The username of the user.
        db (Session): The database session.

    Raises:
        HTTPException: If the user already exists.

    Returns:
        None
    """
    user = search_user_with_role(role, username, db)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
