from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import User
from auth.auth_service import AuthService
from models.users_doctor import UserDoctor
from validation.micro_servicios import search_id
from schemas.doctor import Doctor
from schemas.pacient import Pacient
from services.Doctor_Services import Doctor_Services
from services.patient_services import Patient_Services
from database.database import Session


login_router = APIRouter()
auth_handler = AuthService()



@login_router.post("/login", tags=["login"])
async def login(role: str, form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends()):
    """
    Authenticates a user with the provided credentials and returns an access token if successful.

    Args:
        form_data (OAuth2PasswordRequestForm): The user's login credentials.
        auth_service (AuthService): An instance of the AuthService class.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    token = await auth_service.authenticate_user(form_data.username, form_data.password, role)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}
    
"""
This module contains the login routes for the medical appointments API.

It includes the following routes:
- POST /login: Authenticates a user and returns a JWT token.
- POST /register/patient: Registers a new patient user.
- POST /register/doctor: Registers a new doctor user.
"""

@login_router.post("/register/doctor", tags=["login"])
async def register(users_doctor: Doctor):
    """
    Registers a new doctor user in the system.

    Args:
        user (Doctor): The doctor user to register. Must be an instance of the `Doctor` class, which has the following attributes:
            - `speciality` (str): Doctor's specialty.
            - `npi` (int): National Provider Identifier (NPI) number of the doctor.
            - `first_name` (str): Doctor's first name.
            - `middle_name` (str, optional): Doctor's middle name. Defaults to None.
            - `last_name` (str): Doctor's last name.
            - `email` (EmailStr): Doctor's email address.
            - `phone_number` (str, optional): Doctor's phone number. Defaults to "7860000000".
            - `address` (str): Doctor's address.
            - `birthdate` (str, optional): Doctor's date of birth in "YYYY-MM-DD" format.
            - `gender` (str, optional): Doctor's gender. Must be one of "M", "F", "X" or "O".
            - `role` (List[str], optional): Doctor's role in the system. Must be "doctor". Defaults to ["doctor"].
        auth_service (AuthService, optional): The authentication service. Defaults to Depends().

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the username already exists in the database.
        HTTPException: If the date of birth is not in the correct format.
        HTTPException: If the gender is not one of the valid options.
        HTTPException: If the phone number does not contain only digits or does not have a length of 10 characters.
    """
    user_data = users_doctor.get_user_data()
    doctor_data = users_doctor.get_doctor_data()
    if auth_handler.validate_user_type(users_doctor):
        if await auth_handler.validate_existing_user(users_doctor.username, "doctor"):
            with Session() as db:
                doctor_services = Doctor_Services(db)
                id_doctor = doctor_services.add_doctor(doctor_data)
                if await auth_handler.register_user_doctor(user_data["username"], user_data["hashed_password"], id_doctor):
                    return {"message": "Doctor created successfully"}
    return {"Error": "Doctor not created"}

@login_router.post("/register/patient", tags=["login"])
async def register(user_patient: Pacient):
    """
    Registers a new patient user.

    Args:
        user (Pacient): The patient user to be registered.
        auth_service (AuthService, optional): The authentication service. Defaults to Depends().

    Returns:
        dict: A dictionary with a success message.
    """
    user_data = user_patient.get_user_data()
    patient_data = user_patient.get_patient_data()
    if auth_handler.validate_user_type(user_patient):
        if await auth_handler.validate_existing_user(user_patient.username, "patient"):
            print("Entry 1")
            with Session() as db:
                print("Entry 2")
                print(patient_data)
                id_patient = Patient_Services(db).add_patient(patient_data)
                print("Entry 3")
                print(id_patient)
                if await auth_handler.register_user_patient(user_data["username"], user_data["hashed_password"], id_patient):
                    return {"message": "Patient created successfully"}                
    return {"message": "Patient created successfully"}
